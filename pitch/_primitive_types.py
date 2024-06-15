from enum import Enum
from io import RawIOBase
from typing import Callable, Self


DIGIT_RANGE = range(ord(b"0"), ord(b"9") + 1)
LETTER_RANGE = range(ord(b"A"), ord(b"Z") + 1)
PRINTABLE_RANGE = range(0x20, 0x7e + 1)
UNDERLYING_ATTR_NAME = "data"
WHITESPACE_BYTES = b" "


class ParsedEnum(Enum):
    def __init_subclass__(cls, *, length: int, **kwargs) -> None:
        super().__init_subclass__(**kwargs)
        
        @classmethod
        def parse(target, stream: RawIOBase) -> Self | None:
            raw_str = parse_printable(stream, length=length)
            try:
                value = target(raw_str)
            except ValueError:
                return None
            
            return target(value)
        
        cls.parse = parse


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


def parse_alphabetic(stream: RawIOBase, *, length: int) -> str | None:
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


def create_string_type(name: str, *, length: int, parse_str: Callable[[RawIOBase, int], str | None]):
    @classmethod
    def parse(cls: type, stream: RawIOBase) -> Self | None:
        value = parse_str(stream, length=length)
        if value is None:
            return None
        
        return cls(value)

    return type(name, (str,), dict(parse=parse))


def create_numeric_type(name: str, *, length: int, base: int):
    @classmethod
    def parse(cls: type, stream: RawIOBase) -> Self | None:
        value = parse_number(stream, length=length, base=base)
        if value is None:
            return None
        
        return cls(value)

    return type(name, (int,), dict(parse=parse))


def create_alphabetic_type(name: str, *, length: int):
    return create_string_type(name, length=length, parse_str=parse_alphabetic)


def create_printable_type(name: str, *, length: int):
    return create_string_type(name, length=length, parse_str=parse_printable)
