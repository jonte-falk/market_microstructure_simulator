from dataclasses import dataclass

@dataclass
class Trade:
    taker_id: int
    maker_id: int
    taker_side: str
    maker_side: str
    price: float
    quantity: int
    buy_order: int
    sell_order: int
    timestamp: int

    def __str__(self):
        
        total = self.quantity * self.price

        return (
            f"[{self.timestamp}] "
            f"{self.quantity:>3} @ ${self.price:<6.2f} | "
            f"${total:<8.2f} | "
            f"Taker:{self.taker_id} ({self.taker_side}) | "
            f"Maker:{self.maker_id} ({self.maker_side})"
        )
