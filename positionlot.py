from dataclasses import dataclass


@dataclass
class PositionLot:
    lot_id: int
    agent_id: int
    entry_price: float
    entry_time: float
    quantity: int
    remaining_quantity: int