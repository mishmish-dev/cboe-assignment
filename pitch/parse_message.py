from dataclasses import astuple
from io import RawIOBase

from .data_model import Message


def parse_message(stream: RawIOBase, *, pre: bytes = b"", post: bytes = b"") -> Message | None:
    if pre != stream.read(len(pre)):
        return None
    
    msg = Message.parse_specific_type(stream)
    if msg is None:
        return None
    
    msg_class = Message.__message_type_to_class__[msg.type]
    result = msg_class.parse_specific_type(stream, astuple(msg))

    if post != stream.read(len(post)):
        return None
    
    return result
