from dataclasses import dataclass, make_dataclass
from enum import Enum
from io import RawIOBase
from typing import Callable, Self


DIGIT_RANGE = range(ord(b"0"), ord(b"9") + 1)
LETTER_RANGE = range(ord(b"A"), ord(b"Z") + 1)
PRINTABLE_RANGE = range(0x20, 0x7e + 1)
UNDERLYING_ATTR_NAME = "data"
WHITESPACE_BYTES = b" "


class MessageType(Enum):
    ADD_ORDER = "A"
    ORDER_EXECUTED = "E"
    ORDER_CANCEL = "X"
    TRADE = "P"


class Side(Enum):
    BUY = "B"
    SELL = "S"


class ReservedFlag(Enum):
    YES = "Y"



def is_alphanum(byte: int) -> bool:
    return byte in DIGIT_RANGE or byte in LETTER_RANGE


def parse_number(stream: RawIOBase, *, length: int, base: int) -> int | None:
    read = stream.read(length)
    if not all(map(is_alphanum, read)):
        return None 
    
    try:
        return int(read, base=base)
    except ValueError:
        return None


def parse_alpha(stream: RawIOBase, *, length: int) -> str | None:
    read = stream.read(length)
    read = read.split(WHITESPACE_BYTES, maxsplit=1)[0]
    if not all(byte in LETTER_RANGE for byte in read):
        return None
    return read.decode()


def parse_printable(stream: RawIOBase, *, length: int) -> str | None:
    read = stream.read(length)
    if not all(byte in PRINTABLE_RANGE for byte in read):
        return None
    return read.decode()


def create_string_field(name: str, *, length: int, parse_str: Callable[[RawIOBase, int], str | None]):
    @classmethod
    def parse(cls: type, stream: RawIOBase) -> Self | None:
        value = parse_str(stream, length=cls.length)
        if value is None:
            return None
        
        return cls(value)

    return make_dataclass(
        cls_name=name,
        fields=[(UNDERLYING_ATTR_NAME, str)],
        namespace=dict(length=length, parse=parse)
    )


def create_enum_field(name: str, *, length: int, enum: Enum):
    @classmethod
    def parse(cls: type, stream: RawIOBase) -> Self | None:
        raw_str = parse_printable(stream, length=cls.length)
        try:
            value = enum(raw_str)
        except ValueError:
            return None
        
        return cls(value)

    return make_dataclass(
        cls_name=name,
        fields=[(UNDERLYING_ATTR_NAME, enum)],
        namespace=dict(length=length, parse=parse)
    )


def create_numeric_field(name: str, *, length: int, base: int):
    @classmethod
    def parse(cls: type, stream: RawIOBase) -> Self | None:
        value = parse_number(stream, length=cls.length, base=cls.base)
        if value is None:
            return None
        
        return cls(value)

    return make_dataclass(
        cls_name=name,
        fields=[(UNDERLYING_ATTR_NAME, int)],
        namespace=dict(length=length, base=base, parse=parse)
    )


def create_alpha_field(name: str, *, length: int):
    return create_string_field(name, length=length, parse_str=parse_alpha)


def create_printable_field(name: str, *, length: int):
    return create_string_field(name, length=length, parse_str=parse_printable)
