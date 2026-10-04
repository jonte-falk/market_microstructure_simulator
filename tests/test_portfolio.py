import unittest

from portfolio import Portfolio
from simple_classes import Trade


class PortfolioTests(unittest.TestCase):
    def test_buy_trade_creates_open_lot_and_updates_cash(self):
        portfolio = Portfolio(agent_id=1, inventory=0, cash=1000.0)
        trade = Trade(
            taker_id=1,
            maker_id=2,
            taker_side="BUY",
            maker_side="SELL",
            price=100.0,
            quantity=10,
            buy_order=1,
            sell_order=2,
            timestamp=1,
        )

        portfolio.register_trade(trade)

        self.assertEqual(portfolio.inventory, 10)
        self.assertEqual(portfolio.cash, 0.0)
        self.assertEqual(portfolio.cost_basis, 1000.0)
        self.assertEqual(len(portfolio.open_lots.lots), 1)
        self.assertEqual(portfolio.open_lots.first.lot_id, 1)

    def test_sell_trade_closes_open_lot_and_updates_performance(self):
        portfolio = Portfolio(agent_id=1, inventory=0, cash=1000.0)
        buy_trade = Trade(
            taker_id=1,
            maker_id=2,
            taker_side="BUY",
            maker_side="SELL",
            price=100.0,
            quantity=10,
            buy_order=1,
            sell_order=2,
            timestamp=1,
        )
        sell_trade = Trade(
            taker_id=1,
            maker_id=2,
            taker_side="SELL",
            maker_side="BUY",
            price=120.0,
            quantity=5,
            buy_order=3,
            sell_order=4,
            timestamp=2,
        )

        portfolio.register_trade(buy_trade)
        portfolio.register_trade(sell_trade)

        self.assertEqual(portfolio.inventory, 5)
        self.assertEqual(portfolio.cash, 600.0)
        self.assertEqual(portfolio.realized_pnl, 100.0)
        self.assertEqual(len(portfolio.closed_trades), 1)
        self.assertEqual(portfolio.open_lots.first.remaining_quantity, 5)


if __name__ == "__main__":
    unittest.main()
