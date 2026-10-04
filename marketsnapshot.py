from dataclasses import dataclass

@dataclass
class MarketSnapshot:
    timestamp: int
    best_bid: float | None
    best_ask: float | None
    spread: float | None
    mid_price: float | None
    bid_volume: int
    ask_volume: int
    trade_count: int
    traded_volume: int

    def __str__(self):
        return (
            f"t={self.timestamp:>5} | "
            f"Bid={self.best_bid} | "
            f"Ask={self.best_ask} | "
            f"Mid={self.mid_price} | "
            f"Spread={self.spread} | "
            f"BidVol={self.bid_volume} | "
            f"AskVol={self.ask_volume} | "
            f"Trades={self.trade_count} | "
            f"Volume={self.traded_volume}"
        )