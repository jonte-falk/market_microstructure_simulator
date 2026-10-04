from dataclasses import dataclass
from .trade import Trade


@dataclass(order=True)
class Event:
    timestamp: float


@dataclass
class WakeUpEvent(Event):
    agent_id: int


@dataclass
class TradeEvent(Event):
    trade: Trade


@dataclass
class MarketOpenEvent(Event):
    timestamp: float


@dataclass
class MarketCloseEvent(Event):
    timestamp: float
