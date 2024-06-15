from dataclasses import dataclass, fields
from io import RawIOBase
from typing import Any, ClassVar, Iterable, Self

from .basic_types import MessageType


@dataclass
class BaseMessage:
    __message_type_to_class__: ClassVar[dict[MessageType, type[Self]]] = {}

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
                
