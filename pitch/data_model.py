from dataclasses import dataclass

from ._base_message import BaseMessage
from .basic_types import (
    MessageType,
    Side,
    ReservedFlag,
    Timestamp,
    OrderID,
    ExecutionID,
    Symbol,
    Shares,
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
    shares: Shares
    symbol: Symbol
    price: Price
    reserved: ReservedFlag


@dataclass
class OrderExecuted(Message):
    __message_type__ = MessageType.ORDER_EXECUTED

    order_id: OrderID
    shares: Shares
    execution_id: ExecutionID


@dataclass
class OrderCancel(Message):
    __message_type__ = MessageType.ORDER_CANCEL

    order_id: OrderID
    shares: Shares


@dataclass
class Trade(Message):
    __message_type__ = MessageType.TRADE

    order_id: OrderID
    side: Side
    shares: Shares
    symbol: Symbol
    price: Price
    execution_id: ExecutionID
