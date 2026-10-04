from dataclasses import dataclass, field
from collections import deque
from .order import Order

@dataclass
class PriceLevel:
    price: int
    orders: deque = field(default_factory=deque)

    def add(self, order: Order):
        self.orders.append(order)

    def remove_first(self):
        return self.orders.popleft()
    
    def remove(self, order):
        self.orders.remove(order)

    @property
    def volume(self) -> int:
        return sum(order.quantity for order in self.orders)
    
    @property
    def first(self) -> Order:
        return self.orders[0] if self.orders else None
