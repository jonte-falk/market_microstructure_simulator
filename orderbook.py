from simple_classes import Order, PriceLevel, Trade

class OrderBook:
    
    def __init__(self):
        self.bids = {}
        self.asks = {}
        self.order_map = {}

    def submit_to_book(self, order: Order) -> list[Trade]:
        """
        Submits an order to the orderbook.

        Matches order against any resting orders and returns the trades
        executed immeditaly as a result of the submission.

        Args:
            Order (order): The order being submitted to the orderbook.

        Returns:
            list[Trade]: A list of trades executed immediately after submission.
        """
        if order.side == "BUY":
            return self._match_buy(order)
        else:
            return self._match_sell(order)

    def cancel(self, order_id: int):
        """ 
        Cancels a resting order in the orderbook.

        Args:
            int (order_id): The order identification number.
        """
        order = self.order_map[order_id]

        book_side: dict = self.bids if order.side == "BUY" else self.asks

        level = book_side[order.price]

        level.remove(order)

        if not level.orders:
            book_side.pop(order.price)

        self.order_map.pop(order.order_id)

    def _add(self, order: Order):
        """
        Adds a resting order to the orderbook.

        Args:
            Order (order): The resting order being added to the orderbook.
        """
        book_side: dict = self.bids if order.side == "BUY" else self.asks

        if order.price not in book_side:
            book_side[order.price] = PriceLevel(order.price)
        
        book_side[order.price].add(order)

        self.order_map[order.order_id] = order

    def _execute(self, incoming: Order, resting: Order) -> Trade:
        """
        Executes a trade between two matching orders.

        Takes an incoming order and a resting order and creates the trade object between
        the two orders.

        Args:
            Order (incoming): The incoming order submitted to the orderbook.
            Order (resting): The resting order in the orderbook.

        Returns:
            Trade: A trade between two agents.
        """
        qty = min(incoming.quantity, resting.quantity)

        incoming.quantity -= qty
        resting.quantity -= qty

        trade = Trade(
            taker_id=incoming.agent_id,
            maker_id=resting.agent_id,
            taker_side=incoming.side,
            maker_side=resting.side,
            price=resting.price,
            quantity=qty,
            buy_order=incoming.order_id if incoming.side == "BUY" else resting.order_id,
            sell_order=resting.order_id if incoming.side == "BUY" else incoming.order_id,
            timestamp=incoming.timestamp
        )

        return trade
    
    def _match_buy(self, order: Order) -> list[Trade]:
        """
        Match an incoming buy order against existing resting sell orders (asks).

        This method iterates through available ask price levels that satisfy the
        buy order's price. It executes trades sequentially until either the
        buy order is completely filled or no more matching ask orders remain. If
        the buy order is partially filled, any remaining quantity is added to the
        order book as a resting buy order.

        Args:
            Order (order): The incoming buy order.

        Returns:
            list[Trade]: A list of execution trade objects generated during the matching process.
            Returns an empty list if no matching sell orders are available.
        """
        trades = []

        while(
            order.quantity > 0
            and self.asks
            and self.best_ask <= order.price
        ):
            
            level = self.asks[self.best_ask]

            resting = level.first

            trade = self._execute(order, resting)

            trades.append(trade)

            if resting.quantity == 0:

                level.remove_first()
                self.order_map.pop(resting.order_id)

                if not level.orders:
                    self.asks.pop(level.price)
        
        if order.quantity > 0:
            self._add(order)

        return trades

    def _match_sell(self, order: Order) -> list[Trade]:
        """
        Match an incoming sell order against existing resting buy orders (bids).

        This method iterates through available bid price levels that satisfy the
        sell order's price. It executes trades sequentially until either the
        sell order is completely filled or no more matching bid orders remain. If
        the sell order is partially filled, any remaining quantity is added to the
        order book as a resting sell order.

        Args:
            Order (order): The incoming sell order.

        Returns:
            list[Trade]: A list of execution trade objects generated during the matching process.
            Returns an empty list if no matching buy orders are available.
        """
        trades = []

        while(
            order.quantity > 0
            and self.bids
            and self.best_bid >= order.price
        ):
            
            level = self.bids[self.best_bid]

            resting = level.first

            trade = self._execute(order, resting)

            trades.append(trade)

            if resting.quantity == 0:

                level.remove_first()
                self.order_map.pop(resting.order_id)

                if not level.orders:
                    self.bids.pop(level.price)
        
        if order.quantity > 0:
            self._add(order)

        return(trades)

    @property
    def best_bid(self) -> float:
        """The best bid among the resting order."""
        return max(self.bids) if self.bids else None

    @property
    def best_ask(self) -> float:
        """The best ask among the resting order."""
        return min(self.asks) if self.asks else None
    
    @property
    def spread(self) -> float:
        """The difference between the best bid and the best ask."""
        if self.best_ask is None or self.best_bid is None:
            return None
        return self.best_ask - self.best_bid
    
    @property
    def mid_price(self) -> float:
        """The price in the middle between the best bid and the best ask."""
        spread = self.spread
        best_bid = self.best_bid

        if spread and best_bid is not None:
            return round(spread / 2 + best_bid, 2)

        return None

    def __str__(self) -> str:
        """Returns a table of all resting orders currently in the orderbook."""
        lines = []

        lines.append("ASKS")
        
        for price in sorted(self.asks, reverse=True):
            level = self.asks[price]
            lines.append(f"{price} | {level.volume}")

        lines.append("-------------")

        lines.append("BIDS")

        for price in sorted(self.bids, reverse=True):
            level = self.bids[price]
            lines.append(f"{price} | {level.volume}")

        return "\n".join(lines)