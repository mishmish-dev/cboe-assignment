from dataclasses import dataclass, fields
from io import RawIOBase
from typing import Any, ClassVar, Iterable, Self

from ._primitive_fields import (
    create_enum_field,
    create_numeric_field,
    MessageType,
)


Timestamp = create_numeric_field("Timestamp", length=8, base=10)
MessageTypeIndicator = create_enum_field("MessageTypeIndicator", length=1, enum=MessageType)


def shallow_astuple(dataclass_obj) -> tuple:
    return tuple(getattr(dataclass_obj, field.name) for field in fields(dataclass_obj))


@dataclass
class Message:
    __message_type_to_class__: ClassVar[dict[MessageType, type[Self]]] = {}

    timestamp: Timestamp
    type: MessageTypeIndicator

    def __init_subclass__(cls, **kwargs) -> None:
        super().__init_subclass__(**kwargs)
        msg_type = getattr(cls, "__message_type__", None)
        if msg_type is not None:
            cls.__message_type_to_class__[msg_type] = cls

    @classmethod
    def parse_specific_type(cls, stream: RawIOBase, pre_filled_values: Iterable[Any] = ()) -> Self | None:
        values = list(pre_filled_values)
        skip_first = len(values)
        for field in fields(cls)[skip_first:]:
            parsed_value = field.type.parse(stream)
            if parsed_value is None:
                return None
            
            values.append(parsed_value)
            
        return cls(*values)
                
    @staticmethod
    def parse(stream: RawIOBase) -> Self | None:
        msg = Message.parse_specific_type(stream)
        if msg is None:
            return None
        
        msg_class = Message.__message_type_to_class__[msg.type.data]
        return msg_class.parse_specific_type(stream, shallow_astuple(msg))
