from dataclasses import dataclass

@dataclass
class Order:
    order_id: int
    agent_id: int
    side: str
    price: float
    quantity: int
    initial_quantity: int
    timestamp: int