from enum import Enum
from io import RawIOBase
from typing import Self


DIGIT_RANGE = range(ord(b"0"), ord(b"9") + 1)
LETTER_RANGE = range(ord(b"A"), ord(b"Z") + 1)
WHITESPACE_BYTES = b" "


def is_alphanum(byte: int) -> bool:
    return byte in DIGIT_RANGE or byte in LETTER_RANGE


def parse_number(stream: RawIOBase, *, length: int, base: int) -> int | None:
    read = stream.read(length)
    if len(read) != length or not all(map(is_alphanum, read)):
        return None
    
    try:
        return int(read, base=base)
    except ValueError:
        return None


def parse_alphabetic(stream: RawIOBase, *, length: int) -> str | None:
    read = stream.read(length)
    if len(read) != length:
        return None
    
    read = read.split(WHITESPACE_BYTES, maxsplit=1)[0]
    if all(byte in LETTER_RANGE for byte in read):
        return read.decode()


def create_alphabetic_type(name: str, *, length: int):
    @classmethod
    def parse(cls: type, stream: RawIOBase) -> Self | None:
        value = parse_alphabetic(stream, length=length)
        if value is not None:
            return cls(value)

    return type(name, (str,), dict(parse=parse))


def create_numeric_type(name: str, *, length: int, base: int):
    @classmethod
    def parse(cls: type, stream: RawIOBase) -> Self | None:
        value = parse_number(stream, length=length, base=base)
        if value is not None:
            return cls(value)
        
    return type(name, (int,), dict(parse=parse))


class ParsedEnum(Enum):
    def __init_subclass__(cls, *, length: int, **kwargs) -> None:
        super().__init_subclass__(**kwargs)
        
        @classmethod
        def parse(target, stream: RawIOBase) -> Self | None:
            raw_str = parse_alphabetic(stream, length=length)
            try:
                return target(raw_str)
            except ValueError:
                return None
        
        cls.parse = parse
