from io import BytesIO

import pytest

from pitch.data_model import *
from pitch import parse_message


CORRECTNESS_TEST_CASES = [
    (
        b"28800011AAK27GA0000DTS000100SH    0000619200Y",
        AddOrder(
            timestamp=Timestamp(28800011),
            type=MessageType.ADD_ORDER,
            order_id=OrderID(1389564350501069297),
            side=Side.SELL,
            shares=Shares(100),
            symbol=Symbol("SH"),
            price=Price(619200),
            reserved=ReservedFlag.YES,
        ),
    ),
    (
        b"28800168X1K27GA00000Y000100",
        OrderCancel(
            timestamp=Timestamp(28800168),
            type=MessageType.ORDER_CANCEL,
            order_id=OrderID(204969015920664610),
            shares=Shares(100),
        ),
    ),
    (
        b"28800318E1K27GA00000X00010000001AQ00001",
        OrderExecuted(
            timestamp=Timestamp(28800318),
            type=MessageType.ORDER_EXECUTED,
            order_id=OrderID(204969015920664609),
            shares=Shares(100),
            execution_id=ExecutionID(101704108033),
        ),
    ),
    (
        b"28803240P4K27GA00003PB000100DXD   0000499600000N4AQ00003",
        Trade(
            timestamp=Timestamp(28803240),
            type=MessageType.TRADE,
            order_id=OrderID(599834127447466117),
            side=Side.BUY,
            shares=Shares(100),
            symbol=Symbol("DXD"),
            price=Price(499600),
            execution_id=ExecutionID(65222324471811),
        ),
    ),
]

BAD_INPUT_TEST_CASES = [
    b"111021000DKDKDDAAJAJ",
    b"28803240P4K27GA00003PB000100DXD   0000499600000N4AQ0000",
    b"",
]


@pytest.mark.parametrize("raw,expected", CORRECTNESS_TEST_CASES)
def test_correctness(raw: bytes, expected: Message):
    assert parse_message(BytesIO(raw)) == expected


@pytest.mark.parametrize("raw", BAD_INPUT_TEST_CASES)
def test_bad_input(raw: bytes):
    assert parse_message(BytesIO(raw)) is None
