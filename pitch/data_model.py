from dataclasses import dataclass

from ._message import Message
from ._primitive_fields import (
    create_alpha_field,
    create_enum_field,
    create_numeric_field,
    MessageType,
    ReservedFlag,
    Side,
)

OrderID = create_numeric_field("OrderID", length=12, base=36)
ExecutionID = create_numeric_field("ExecutionID", length=12, base=36)

StockSymbol = create_alpha_field("StockSymbol", length=6)
SharesQuantity = create_numeric_field("SharesQuantity", length=6, base=10)
Price = create_numeric_field("Price", length=10, base=10)
SideIndicator = create_enum_field("SideIndicator", length=1, enum=Side)
ReservedIndicator = create_enum_field("ReservedIndicator", length=1, enum=ReservedFlag)


@dataclass
class AddOrder(Message):
    __message_type__ = MessageType.ADD_ORDER

    order_id: OrderID
    side: SideIndicator
    shares: SharesQuantity
    symbol: StockSymbol
    price: Price
    reserved: ReservedIndicator


@dataclass
class OrderExecuted(Message):
    __message_type__ = MessageType.ORDER_EXECUTED

    order_id: OrderID
    shares: SharesQuantity
    execution_id: ExecutionID


@dataclass
class OrderCancel(Message):
    __message_type__ = MessageType.ORDER_CANCEL

    order_id: OrderID
    shares: SharesQuantity


@dataclass
class Trade(Message):
    __message_type__ = MessageType.TRADE

    order_id: OrderID
    side: SideIndicator
    shares: SharesQuantity
    symbol: StockSymbol
    price: Price
    execution_id: ExecutionID


