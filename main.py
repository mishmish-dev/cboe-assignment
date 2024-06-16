import gzip
import sqlite3
import sys
from argparse import ArgumentParser
from io import RawIOBase
from typing import Any

from pitch import parse_message, AddOrder, OrderCancel, OrderExecuted, Trade
from pitch import ExecutionID, OrderID, Shares, Symbol


def init_tables(conn: sqlite3.Connection):
    conn.execute("""
        CREATE TABLE open_orders
        (order_id INTEGER PRIMARY KEY, symbol TEXT, shares INTEGER)
    """)
    conn.execute("""
        CREATE TABLE traded
        (execution_id INTEGER, order_id INTEGER, symbol TEXT, shares INTEGER)
    """)


def place_order(conn: sqlite3.Connection, order_id: OrderID, symbol: Symbol, shares: Shares):
    data = (order_id, symbol, shares)
    conn.execute("INSERT INTO open_orders (order_id, symbol, shares) VALUES (?, ?, ?)", data)


def get_symbol(conn: sqlite3.Connection, order_id: OrderID):
    res = conn.execute("SELECT symbol FROM open_orders WHERE order_id = ?", (order_id,))
    return next(res)[0]


def subtract_shares_from_order(conn: sqlite3.Connection, order_id: OrderID, shares: Shares):
    conn.execute("UPDATE open_orders SET shares = shares - ? WHERE order_id = ?", (shares, order_id))
    conn.execute("DELETE FROM open_orders WHERE shares = 0 and order_id = ?", (order_id,))


def record_trade(conn: sqlite3.Connection, execution_id: ExecutionID, order_id: OrderID, symbol: Symbol, shares: Shares):
    data = (execution_id, order_id, symbol, shares)
    conn.execute("INSERT INTO traded (execution_id, order_id, symbol, shares) VALUES (?, ?, ?, ?)", data)


def record_execution(conn: sqlite3.Connection, execution_id: ExecutionID, order_id: OrderID, shares: Shares):
    conn.execute(f"""
        INSERT INTO traded
        (execution_id, order_id, symbol, shares)
        SELECT
            {execution_id} as execution_id,
            {order_id} as order_id,
            symbol,
            {shares} as shares
        FROM open_orders o
        WHERE o.order_id = order_id
    """)


def process_messages(conn: sqlite3.Connection, stream: RawIOBase):
    while msg := parse_message(stream, pre=b"S", post=b"\n"):
        if isinstance(msg, AddOrder):
            place_order(conn, msg.order_id, msg.symbol, msg.shares)

        if isinstance(msg, OrderCancel):
            subtract_shares_from_order(conn, msg.order_id, msg.shares)

        if isinstance(msg, OrderExecuted):
            record_execution(conn, msg.execution_id, msg.order_id, msg.shares)
            subtract_shares_from_order(conn, msg.order_id, msg.shares)

        if isinstance(msg, Trade):
            record_trade(conn, msg.execution_id, msg.order_id, msg.symbol, msg.shares)


def get_top_symbols(conn: sqlite3.Connection, top_symbols_count: int) -> list[tuple[str, int]]:
    res = conn.execute(f"""
        SELECT symbol, SUM(shares) AS volume
        FROM traded GROUP BY symbol
        ORDER BY volume DESC LIMIT {top_symbols_count}
    """)
    return list(res)


def render_table(table: list[tuple[Any, Any]]) -> str:
    if not table:
        return "[the table is empty]"

    w1 = max(len(str(c)) for c, _ in table)
    w2 = max(len(str(c)) for _, c in table)

    return "\n".join(
        "{c1:<{w1}} {c2:>{w2}}".format(c1=c1, c2=c2, w1=w1, w2=w2)
        for c1, c2 in table
    )


def main(*, input: str | None, db_file: str | None, gzipped: bool, top_symbols_count: int) -> None:
    if db_file is None:
        db_file = ":memory:"

    if input is None:
        with sqlite3.connect(db_file) as conn:
            top_symbols = solution(conn, sys.stdin.buffer, top_symbols_count)
    elif gzipped:
        with sqlite3.connect(db_file) as conn, gzip.open(input, "rb") as stream:
            top_symbols = solution(conn, stream, top_symbols_count)
    else:
        with sqlite3.connect(db_file) as conn, open(input, "rb") as stream:
            top_symbols = solution(conn, stream, top_symbols_count)

    print(render_table(top_symbols))


def solution(conn: sqlite3.Connection, stream: RawIOBase, top_symbols_count: int) -> list[tuple[str, int]]:
    init_tables(conn)
    process_messages(conn, stream)
    return get_top_symbols(conn, top_symbols_count)


def parse_args():
    parser = ArgumentParser()
    parser.add_argument("-i", "--input", help="Input file. If omitted, will read from standard input")
    parser.add_argument("-f", "--db-file", help="SQLite database file. If omitted, use in-memory DB")
    parser.add_argument("-g", "--gzipped", action="store_true", help="Consume gzipped input")
    parser.add_argument("-n", "--top-symbols-count", type=int, default=10, help="Number of rows in the output table")

    return vars(parser.parse_args())


if __name__ == "__main__":
    main(**parse_args())
