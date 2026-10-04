from dataclasses import field, dataclass
from collections import deque
from .positionlot import PositionLot


@dataclass
class OpenLots:
    lots: deque[PositionLot] = field(default_factory=deque)

    def add(self, lot: PositionLot):
        self.lots.append(lot)

    def remove_first(self):
        return self.lots.popleft()

    def remove(self, lot: PositionLot):
        self.lots.remove(lot)

    @property
    def first(self) -> PositionLot | None:
        return self.lots[0] if self.lots else None
