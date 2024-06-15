from io import BytesIO

from pitch.data_model import *


def test_timestamp():
    b = BytesIO(b"00212163")
    assert Timestamp.parse(b).data == 212163


def test_symbol():
    b = BytesIO(b"MEX   ")
    assert StockSymbol.parse(b).data == "MEX   "


    b = BytesIO(b"S   ")
    assert SideIndicator.parse(b).data == Side.SELL