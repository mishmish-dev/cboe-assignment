import sqlite3
import sys

from pitch import parse_message, AddOrder, OrderCancel, OrderExecuted, Trade
from pitch import OrderID, Shares, Symbol


def init_tables(conn: sqlite3.Connection):
    conn.execute("CREATE TABLE orders (order_id INTEGER PRIMARY KEY, symbol TEXT, shares INTEGER)")
    conn.execute("CREATE TABLE traded (order_id INTEGER, symbol TEXT, shares INTEGER)")


def place_order(conn: sqlite3.Connection, order_id: OrderID, symbol: Symbol, shares: Shares):
    data = (order_id, symbol, shares)
    conn.execute("INSERT INTO orders (order_id, symbol, shares) VALUES (?, ?, ?)", data)


def get_symbol(conn: sqlite3.Connection, order_id: OrderID):
    res = conn.execute("SELECT symbol FROM orders WHERE order_id = ?", (order_id,))
    return next(res)[0]


def subtract_shares_from_order(conn: sqlite3.Connection, order_id: OrderID, shares: Shares):
    conn.execute("UPDATE orders SET shares = shares - ? WHERE order_id = ?", (shares, order_id))
    conn.execute("DELETE FROM orders WHERE shares = 0 and order_id = ?", (order_id,))


def record_trade(conn: sqlite3.Connection, order_id: OrderID, symbol: Symbol, shares: Shares):
    data = (order_id, symbol, shares)
    conn.execute("INSERT INTO traded (order_id, symbol, shares) VALUES (?, ?, ?)", data)


def process_messages(conn: sqlite3.Connection, file):
    while msg := parse_message(file, pre=b"S", post=b"\n"):
        if isinstance(msg, AddOrder):
            place_order(conn, msg.order_id, msg.symbol, msg.shares)

        if isinstance(msg, OrderCancel):
            subtract_shares_from_order(conn, msg.order_id, msg.shares)

        if isinstance(msg, OrderExecuted):
            symbol = get_symbol(conn, msg.order_id)
            subtract_shares_from_order(conn, msg.order_id, msg.shares)
            record_trade(conn, msg.order_id, symbol, msg.shares)

        if isinstance(msg, Trade):
            subtract_shares_from_order(conn, msg.order_id, msg.shares)
            record_trade(conn, msg.order_id, msg.symbol, msg.shares)


def get_top_symbols(conn: sqlite3.Connection) -> list[tuple[str, int]]:
    res = conn.execute("""
        SELECT symbol, SUM(shares) AS volume
        FROM traded GROUP BY symbol
        ORDER BY volume DESC LIMIT 10
    """)
    return list(res)


def main():
    with sqlite3.connect(":memory:") as conn:
        init_tables(conn)
        process_messages(conn, sys.stdin.buffer)
        top_symbols = get_top_symbols(conn)

    for symbol, volume in top_symbols:
        print(f"{symbol:<6} {volume:>4}")


if __name__ == "__main__":
    main()
