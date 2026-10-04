from dataclasses import dataclass


@dataclass
class Request:
    agent_id: int


@dataclass
class SubmitOrderRequest(Request):
    side: str
    price: float
    quantity: int


@dataclass
class CancelOrderRequest(Request):
    order_id: int