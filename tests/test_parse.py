from io import BytesIO

from pitch.data_model import *
from pitch import parse_message


def test_parse_message():
    b = BytesIO(b"28800011AAK27GA0000DTS000100SH    0000619200Y")
    msg = AddOrder(
        timestamp=Timestamp(28800011),
        type=MessageType.ADD_ORDER,
        order_id=OrderID(1389564350501069297),
        side=Side.SELL,
        shares=SharesQuantity(100),
        symbol=StockSymbol("SH"),
        price=Price(619200),
        reserved=ReservedFlag.YES,
    )
    assert parse_message(b) == msg

    b = BytesIO(b"28800168X1K27GA00000Y000100")
    msg = OrderCancel(
        timestamp=Timestamp(28800168),
        type=MessageType.ORDER_CANCEL,
        order_id=OrderID(204969015920664610),
        shares=SharesQuantity(100),
    )
    assert parse_message(b) == msg

    b = BytesIO(b"28800318E1K27GA00000X00010000001AQ00001")
    msg = OrderExecuted(
        timestamp=Timestamp(28800318),
        type=MessageType.ORDER_EXECUTED,
        order_id=OrderID(204969015920664609),
        shares=SharesQuantity(100),
        execution_id=ExecutionID(101704108033),
    )
    assert parse_message(b) == msg

    b = BytesIO(b"28803240P4K27GA00003PB000100DXD   0000499600000N4AQ00003")
    msg = Trade(
        timestamp=Timestamp(28803240),
        type=MessageType.TRADE,
        order_id=OrderID(599834127447466117),
        side=Side.BUY,
        shares=SharesQuantity(100),
        symbol=StockSymbol("DXD"),
        price=Price(499600),
        execution_id=ExecutionID(65222324471811),
    )
    assert parse_message(b) == msg