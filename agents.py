from abc import ABC, abstractmethod
from portfolio import Portfolio
from exchange import Exchange
from simple_classes import Order, Request, SubmitOrderRequest, CancelOrderRequest
import random

START_INVENTORY = 100  # Number of assets each agent starts with.
START_CASH = 10000
TICK = 0.01  # Minimum possible upward or downward price movement of an asset.

class Agent(ABC):

    def __init__(self, agent_id: int):
        self.agent_id = agent_id
        self.portfolio = Portfolio(agent_id=agent_id,
                                   inventory=START_INVENTORY,
                                   cash=START_CASH)

    @abstractmethod
    def update(self, exchange: Exchange) -> list[Request] | None:
        pass

    @abstractmethod
    def next_wait_time(self) -> float:
        pass

    @abstractmethod
    def fair_price(self, exchange: Exchange | None = None):
        pass

    def update_market_value(self, exchange: Exchange):

        if exchange.book.mid_price is None:
            return None

        return self.portfolio.update_market_value(exchange)


class NoiseTrader(Agent):

    def __init__(self, agent_id: int):
        super().__init__(agent_id)

    def update(self, exchange: Exchange) -> list[Request] | None:

        rand = random.random()

        if rand < 0.2:
            side = "BUY" if rand < 0.1 else "SELL"

            requests = []

            price = self.fair_price()

            quantity = self.trade_quantity(side)

            if quantity != 0:

                requests.append(SubmitOrderRequest(
                    agent_id=self.agent_id,
                    side=side,
                    price=price,
                    quantity=quantity
                ))

                return requests

            else:
                return None
            
    def next_wait_time(self) -> float:
        return 20.0 #(s)

    def fair_price(self, exchange: Exchange | None = None):
        return random.randint(90, 110)

    def trade_quantity(self, side: str):
        if side == "BUY":
            quantity = 10
            self.inventory += quantity
        else:
            quantity = 10 if self.inventory >= 10 else self.inventory
            self.inventory -= quantity

        return quantity


class MarketMaker(Agent):

    def __init__(self, agent_id: int):
        super().__init__(agent_id)

    def update(self, exchange: Exchange) -> list[Request] | None:

        fair_price = self.fair_price(exchange)

        if fair_price is None:
            return None
        
        bid_price = round(fair_price - TICK, 2)
        ask_price = round(fair_price + TICK, 2)

        requests = []

        requests.extend(self._refresh_orders(exchange, "BUY", bid_price, 20))
        requests.extend(self._refresh_orders(exchange, "SELL", ask_price, 20))

        return requests


    def current_orders(self, exchange: Exchange, side: str) -> list[Order]:
        return [
            order
            for order in exchange.book.order_map.values()
            if order.agent_id == self.agent_id and order.side == side
        ]

    def _refresh_orders(self,
            exchange: Exchange,
            side: str,
            price: float,
            target_quantity: int
        ) -> list[Request] | None:

        current_orders = self.current_orders(exchange, side)
        matching_orders = []
        requests = []

        for order in current_orders:

            if order.price != price:

                requests.append(CancelOrderRequest(
                    agent_id=self.agent_id,
                    order_id=order.order_id
                ))

            else:
                matching_orders.append(order)

        current_volume = sum(order.quantity for order in matching_orders)

        if current_volume != target_quantity:

            for order in matching_orders:

                requests.append(CancelOrderRequest(
                    agent_id=self.agent_id,
                    order_id=order.order_id
                ))

            requests.append(SubmitOrderRequest(
                agent_id=self.agent_id,
                side=side,
                price=price,
                quantity=target_quantity
            ))

        return requests
        
    def next_wait_time(self) -> float:
        return 0.2 #(s)

    def fair_price(self, exchange: Exchange | None = None) -> float | None:
        return exchange.book.mid_price if exchange is not None else None

