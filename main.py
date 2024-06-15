import gzip
from io import BytesIO

from pitch import AddOrder, OrderExecuted, Trade, parse_message

from collections import Counter



def main():
    traded_volume = Counter()
    alive_order_ids_to_symbol = {}

    with gzip.open("pitch_example_data.gz") as f:
        for line in f:
            buf = BytesIO(line[1:])
            msg = parse_message(buf)

            if isinstance(msg, AddOrder):
                alive_order_ids_to_symbol[msg.order_id] = msg.symbol
            
            if isinstance(msg, OrderExecuted):
                symbol = alive_order_ids_to_symbol[msg.order_id]
                traded_volume[symbol] += msg.shares
                
            if isinstance(msg, Trade):
                traded_volume[msg.symbol] += msg.shares


    top_symbols = traded_volume.most_common(10)

    for symbol, volume in top_symbols:
        print(f"{symbol:<6} {volume}")


if __name__ == "__main__":
    main()