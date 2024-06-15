import gzip
from io import BytesIO

from pitch.data_model import Message, AddOrder, OrderExecuted, Trade

from collections import Counter

traded_volume = Counter()
alive_order_ids_to_symbol = {}

if __name__ == "__main__":
    with gzip.open("pitch_example_data.gz") as f:
        for line in f:
            buf = BytesIO(line[1:])
            msg = Message.parse(buf)
            if isinstance(msg, AddOrder):
                alive_order_ids_to_symbol[msg.order_id.data] = msg.symbol.data
            
            if isinstance(msg, OrderExecuted):
                symbol = alive_order_ids_to_symbol[msg.order_id.data]
                traded_volume[symbol] += msg.shares.data
                
            if isinstance(msg, Trade):
                traded_volume[msg.symbol.data] += msg.shares.data


    top_symbols = traded_volume.most_common(10)

    for symbol, volume in top_symbols:
        print(f"{symbol:<6} {volume}")