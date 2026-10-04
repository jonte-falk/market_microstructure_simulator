from simple_classes import Trade, Order
from simple_classes.events import *
from simple_classes.requests import *
from exchange import Exchange
from statistics import Statistics
from agents import Agent
import heapq

class Simulation:

    def __init__(self, agents: list[Agent]):
        self.agents = agents
        self.exchange = Exchange()
        self.statistics = Statistics()

        self.current_time = 0.0
        self.events_queue = []
        self.handlers = {
            WakeUpEvent: self._handle_wakeup_event,
            TradeEvent: self._handle_trade_event,
            MarketOpenEvent: self._handle_market_open,
            MarketCloseEvent: self._handle_market_close,
        }
    
    def process_event(self, event: Event):
        handler = self.handlers[type(event)]
        handler(event)

    def schedule(self, event: Event):
        heapq.heappush(self.events_queue, event)

    def run(self):
        
        for agent in self.agents:

            self.schedule(WakeUpEvent(
                timestamp=agent.next_wait_time(),
                agent_id=agent.agent_id
            ))

        while self.events_queue:

            event = heapq.heappop(self.events_queue)

            self.current_time = event.timestamp

            self.process_event(event)

            self.statistics.record(self.current_time, self.exchange)

    def _handle_wakeup_event(self, event: WakeUpEvent):
        
        agent = self.agents[event.agent_id]

        requests = agent.update(self.exchange)

        if requests is None:
            return

        for request in requests:
            self._handle_request(request)
            
        wait = agent.next_wait_time()

        self.schedule(WakeUpEvent(
            timestamp=self.current_time + wait,
            agent_id=agent.agent_id
        ))

    def _handle_request(self, request: Request):

        match request:

            case SubmitOrderRequest():
                
                trades = self.exchange.submit_order(
                    request=request,
                    current_time=self.current_time
                )

                for trade in trades:
                    self.schedule(TradeEvent(trade))

            case CancelOrderRequest():

                self.exchange.cancel_order(request)

    def _handle_trade_event(self, event: TradeEvent):
        pass

    