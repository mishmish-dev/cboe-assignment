import gzip
import sqlite3
from io import BytesIO

from pitch import AddOrder, OrderCancel, OrderExecuted, parse_message, Trade


def init_tables(conn: sqlite3.Connection):
    conn.execute("CREATE TABLE orders (order_id INTEGER PRIMARY KEY, symbol TEXT, shares INTEGER)")
    conn.execute("CREATE TABLE traded (order_id INTEGER, symbol TEXT, shares INTEGER)")


def add_order(order: AddOrder, conn: sqlite3.Connection):
    data = (order.order_id, order.symbol, order.shares)
    conn.execute("INSERT INTO orders (order_id, symbol, shares) VALUES (?, ?, ?)", data)


def cancel_order(order: OrderExecuted, conn: sqlite3.Connection):
    conn.execute("UPDATE orders SET shares = shares - ? WHERE order_id = ?", (order.shares, order.order_id))
    conn.execute("DELETE FROM orders WHERE shares = 0 and order_id = ?", (order.order_id,))


def execute_order(order: OrderExecuted, conn: sqlite3.Connection):
    res = conn.execute("UPDATE orders SET shares = shares - ? WHERE order_id = ? RETURNING symbol", (order.shares, order.order_id))
    symbol = list(res)[0][0]
    conn.execute("DELETE FROM orders WHERE shares = 0 and order_id = ?", (order.order_id,))

    data = (order.order_id, symbol, order.shares)
    conn.execute("INSERT INTO traded (order_id, symbol, shares) VALUES (?, ?, ?)", data)


def execute_trade(trade: Trade, conn: sqlite3.Connection):
    conn.execute("UPDATE orders SET shares = shares - ? WHERE order_id = ?", (trade.shares, trade.order_id))
    conn.execute("DELETE FROM orders WHERE shares = 0 and order_id = ?", (trade.order_id,))

    data = (trade.order_id, trade.symbol, trade.shares)
    conn.execute("INSERT INTO traded (order_id, symbol, shares) VALUES (?, ?, ?)", data)


def process_messages(conn: sqlite3.Connection, filename: str):
    with gzip.open(filename) as f:      
        for line in f:
            buffer = BytesIO(line[1:])
            msg = parse_message(buffer)

            if isinstance(msg, AddOrder):
                add_order(msg, conn)
            if isinstance(msg, OrderCancel):
                cancel_order(msg, conn)
            if isinstance(msg, OrderExecuted):
                execute_order(msg, conn)
            if isinstance(msg, Trade):
                execute_trade(msg, conn)


def get_top_symbols(conn: sqlite3.Connection) -> list[tuple[str, int]]:
    res = conn.execute("""
        SELECT symbol, SUM(shares) AS volume
        FROM traded GROUP BY symbol ORDER BY volume DESC LIMIT 10
    """)
    return list(res)


def main():
    with sqlite3.connect(":memory:") as conn:
        init_tables(conn)
        process_messages(conn, "pitch_example_data.gz")
        top_symbols = get_top_symbols(conn)

    for symbol, volume in top_symbols:
        print(f"{symbol:<6} {volume:>4}")


if __name__ == "__main__":
    main()