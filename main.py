import gzip
from io import BytesIO

from pitch import AddOrder, OrderExecuted, Trade, parse_message

from collections import Counter



def main():
    traded_quantity_by_symbol = Counter()
    order_id_to_symbol = {}

    with gzip.open("pitch_example_data.gz") as f:
        for line in f:
            buffer = BytesIO(line[1:])
            msg = parse_message(buffer)

            if isinstance(msg, AddOrder):
                order_id_to_symbol[msg.order_id] = msg.symbol
            
            if isinstance(msg, OrderExecuted):
                symbol = order_id_to_symbol[msg.order_id]
                traded_quantity_by_symbol[symbol] += msg.shares
                
            if isinstance(msg, Trade):
                traded_quantity_by_symbol[msg.symbol] += msg.shares


    top_symbols = traded_quantity_by_symbol.most_common(10)

    for symbol, quantity in top_symbols:
        print(f"{symbol:<6} {quantity:>5}")


if __name__ == "__main__":
    main()