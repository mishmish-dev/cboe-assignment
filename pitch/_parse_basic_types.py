from enum import Enum
from io import RawIOBase
from typing import Self


def parse_number(stream: RawIOBase, *, length: int, base: int) -> int | None:
    raw = stream.read(length)
    if len(raw) != length or not raw.isalnum():
        return None
    
    try:
        return int(raw, base=base)
    except ValueError:
        return None


def parse_alphanumeric(stream: RawIOBase, *, length: int) -> str | None:
    raw = stream.read(length)
    if len(raw) != length:
        return None
    
    raw = raw.rstrip()
    if raw.isalnum():
        return raw.decode()


def create_alphanumeric_type(name: str, *, length: int):
    @classmethod
    def parse(cls: type, stream: RawIOBase) -> Self | None:
        value = parse_alphanumeric(stream, length=length)
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
            raw_str = parse_alphanumeric(stream, length=length)
            try:
                return target(raw_str)
            except ValueError:
                return None
        
        cls.parse = parse
