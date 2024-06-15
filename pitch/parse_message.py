from dataclasses import astuple
from io import RawIOBase

from .data_model import Message


def parse_message(stream: RawIOBase) -> Message | None:
    msg = Message.parse_specific_type(stream)
    if msg is None:
        return None
    
    msg_class = Message.__message_type_to_class__[msg.type]
    return msg_class.parse_specific_type(stream, astuple(msg))