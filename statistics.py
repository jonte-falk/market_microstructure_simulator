from simple_classes import MarketSnapshot
from exchange import Exchange
import matplotlib.pyplot as plt


class Statistics:

    def __init__(self):
        self.snapshots = []

    def record(self, timestamp: int, exchange: Exchange):
       
       snapshot = MarketSnapshot(
           timestamp=timestamp,
           best_bid=exchange.book.best_bid,
           best_ask=exchange.book.best_ask,
           spread=exchange.book.spread,
           mid_price=exchange.book.mid_price,
           bid_volume=sum(level.volume for level in exchange.book.bids.values()),
           ask_volume=sum(level.volume for level in exchange.book.asks.values()),
           trade_count=len(exchange.trades),
           traded_volume=sum(trade.quantity for trade in exchange.trades)
       )

       self.snapshots.append(snapshot)

    def plot_mid_price(self, filename: str | None = None, show: bool = True):
        valid_points = [
            (snapshot.timestamp, snapshot.mid_price)
            for snapshot in self.snapshots
            if snapshot.mid_price is not None
        ]

        if not valid_points:
            raise ValueError("No mid-price data available to plot.")

        timestamps = [timestamp for timestamp, _ in valid_points]
        mid_prices = [mid_price for _, mid_price in valid_points]

        plt.figure(figsize=(10, 4))
        plt.plot(timestamps, mid_prices, color="royalblue", linewidth=1.5)
        plt.xlabel("Timestamp")
        plt.ylabel("Mid Price")
        #plt.ylim(0, 120)
        plt.title("Mid Price Over Time")
        plt.grid(True, alpha=0.3)

        if filename:
            plt.savefig(filename, dpi=300, bbox_inches="tight")

        if show:
            plt.show()
        else:
            plt.close()
