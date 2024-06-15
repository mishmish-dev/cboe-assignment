from dataclasses import dataclass

from ._base_message import BaseMessage
from .basic_types import (
    MessageType,
    Side,
    ReservedFlag,
    Timestamp,
    OrderID,
    ExecutionID,
    StockSymbol,
    SharesQuantity,
    Price,
)


@dataclass
class Message(BaseMessage):
    timestamp: Timestamp
    type: MessageType
    

@dataclass
class AddOrder(Message):
    __message_type__ = MessageType.ADD_ORDER

    order_id: OrderID
    side: Side
    shares: SharesQuantity
    symbol: StockSymbol
    price: Price
    reserved: ReservedFlag


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
    side: Side
    shares: SharesQuantity
    symbol: StockSymbol
    price: Price
    execution_id: ExecutionID


