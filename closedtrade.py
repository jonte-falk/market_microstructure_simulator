from dataclasses import dataclass

@dataclass
class ClosedTrade:
    lot_id: int
    entry_price: float
    exit_price: float
    entry_time: int
    exit_time: int
    quantity: int
    realized_pnl: float