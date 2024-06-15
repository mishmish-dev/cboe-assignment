from ._primitive_types import (
    create_alphabetic_type,
    create_numeric_type,
    ParsedEnum,
)


class MessageType(ParsedEnum, length=1):
    ADD_ORDER = "A"
    ORDER_EXECUTED = "E"
    ORDER_CANCEL = "X"
    TRADE = "P"


class Side(ParsedEnum, length=1):
    BUY = "B"
    SELL = "S"


class ReservedFlag(ParsedEnum, length=1):
    YES = "Y"


Timestamp = create_numeric_type("Timestamp", length=8, base=10)
OrderID = create_numeric_type("OrderID", length=12, base=36)
ExecutionID = create_numeric_type("ExecutionID", length=12, base=36)

StockSymbol = create_alphabetic_type("StockSymbol", length=6)
SharesQuantity = create_numeric_type("SharesQuantity", length=6, base=10)
Price = create_numeric_type("Price", length=10, base=10)