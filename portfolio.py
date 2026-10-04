from simple_classes import Trade, ClosedTrade, PositionLot, OpenLots
from exchange import Exchange
from copy import deepcopy


class Portfolio:

    def __init__(self, agent_id: int, inventory: int, cash: float):
        self.agent_id: int = agent_id
        self.inventory: int = inventory
        self.cash: float = cash
        self.market_value: float = 0.0
        self.cost_basis: float = 0.0
        self.realized_pnl: float = 0.0
        self.unrealized_pnl: float = 0.0
        self.fees_paid: float = 0.0 # Transaction costs to be implemented at a later stage.

        self.lot_id = 1
        self.open_lots: OpenLots = OpenLots()
        self.closed_lots: list[PositionLot] = []
        self.closed_trades: list[ClosedTrade] = []

    def register_trade(self, trade: Trade):

        side = self._determine_trade_side(trade)
        if side is None:
            raise ValueError("Trade does not involve this portfolio")

        if side == "BUY":
            trade_value = trade.price * trade.quantity

            self.open_lots.add(PositionLot(
                lot_id=self.lot_id,
                agent_id=self.agent_id,
                entry_price=trade.price,
                entry_time=trade.timestamp,
                quantity=trade.quantity,
                remaining_quantity=trade.quantity
            ))

            self.inventory += trade.quantity
            self.cash -= trade_value
            self.cost_basis += trade_value

            self.lot_id += 1

        elif side == "SELL":
            trade_copy = deepcopy(trade)
            trades_before = len(self.closed_trades)
            executed_quantity = 0

            while (trade_copy.quantity > 0
                   and self.open_lots.first is not None
                   ):
                
                lot = self.open_lots.first
                qty_closed = self._close_trade(lot, trade_copy)
                executed_quantity += qty_closed

                if lot.remaining_quantity == 0:
                    self.closed_lots.append(lot)
                    self.open_lots.remove_first()

            self.inventory -= executed_quantity
            self.cash += trade.price * executed_quantity

            for closed_trade in self.closed_trades[trades_before:]:
                self._update_performance(closed_trade)

        else:
            raise ValueError(f"Unsupported trade side: {side}")
        
        self._update_unrealized_pnl()


    def _update_performance(self, closed_trade: ClosedTrade):
        self.realized_pnl += closed_trade.realized_pnl

    def _update_unrealized_pnl(self):
        self.unrealized_pnl = round(self.market_value - self.cost_basis, 2)

    def _close_trade(self, lot: PositionLot, trade: Trade):

        qty = min(lot.remaining_quantity, trade.quantity)

        lot.remaining_quantity -= qty
        trade.quantity -= qty

        closed_trade = ClosedTrade(
            lot_id=lot.lot_id,
            entry_price=lot.entry_price,
            exit_price=trade.price,
            entry_time=lot.entry_time,
            exit_time=trade.timestamp,
            quantity=qty,
            realized_pnl=(trade.price - lot.entry_price) * qty
        )

        self.cost_basis -= lot.entry_price * qty

        self.closed_trades.append(closed_trade)

        return qty

    def _determine_trade_side(self, trade: Trade) -> str:

        if trade.taker_id == self.agent_id:
            side = trade.taker_side

        elif trade.maker_id == self.agent_id:
            side = trade.maker_side

        else:
            return None # Not involved in trade. Return error instead,
                        # if involvement is checked before method?
        return side
    
    def update_market_value(self, exchange: Exchange):
        self.market_value = round(self.inventory * exchange.book.mid_price)
        # Change to last close price instead? Make into property also?
        
    
        

        