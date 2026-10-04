from simple_classes import Order, Trade, SubmitOrderRequest, CancelOrderRequest
from orderbook import OrderBook

class Exchange:

    def __init__(self):
        self.book = OrderBook()
        self.trades = []
        self.order_id = 1

    def submit_order(self, request: SubmitOrderRequest, current_time: float) -> list[Trade]:

        order = Order(
            order_id=self.order_id,
            agent_id=request.agent_id,
            side=request.side,
            price=request.price,
            quantity=request.quantity,
            initial_quantity=request.quantity,
            timestamp=current_time,
        )

        trades = self.book.submit_to_book(order)
        self.trades.extend(trades)

        self.order_id += 1

        return trades

    def cancel_order(self, request: CancelOrderRequest):
        self.book.cancel(request.order_id)


    """def _submit_to_exchange(self, order: Order) -> list[Trade]:
        trades = self.book.submit_to_book(order)

        self.trades.extend(trades)
        
        return trades
    
    def submit_to_exchange(
            self, 
            agent_id: int,
            side: str,
            price: float,
            quantity: int,
        ) -> list[Trade]:
        
        trades = self._submit_to_exchange(Order(
            order_id=self.order_id,
            agent_id=agent_id,
            side=side,
            price=round(price, 2),
            quantity=quantity,
            initial_quantity=quantity,
            timestamp=self.timestamp
        ))

        

        return trades"""