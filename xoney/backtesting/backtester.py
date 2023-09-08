# Copyright 2022 Vladyslav Kochetov. All Rights Reserved.
#
# Licensed under the Apache License, Version 2.0 (the "License");
# you may not use this file except in compliance with the License.
# You may obtain a copy of the License at
#
#     http://www.apache.org/licenses/LICENSE-2.0
#
# Unless required by applicable law or agreed to in writing, software
# distributed under the License is distributed on an "AS IS" BASIS,
# WITHOUT WARRANTIES OR CONDITIONS OF ANY KIND either express or implied.
# See the License for the specific language governing permissions and
# limitations under the License.
# =============================================================================
from __future__ import annotations
from datetime import timedelta

from xoney.generic.candlestick import Chart, Candle
from xoney.generic.routes import Instrument, TradingSystem, ChartContainer
from xoney.generic.symbol import Symbol
from xoney.generic.timeframes.template import TimeFrame
from xoney.generic.workers import EquityWorker
from xoney.generic.trades import TradeHeap, Trade
from xoney.generic.events import Event
from xoney.generic.equity import Equity

from typing import Iterable

from xoney.strategy import Strategy
from xoney.backtesting import _utils



class Backtester(EquityWorker):  # TODO: stats support
    _equity: Equity
    _initial_depo: float
    _time_adj: float | TimeFrame | timedelta

    @property
    def equity(self) -> Equity:
        return self._equity

    @property
    def free_balance(self) -> float:
        return self._free_balance

    def __init__(self,
                 initial_depo: float = 100.0,
                 commission: float = 0.1 * 0.01,
                 time_adjustment: float | TimeFrame | timedelta = 0.5):
        super().__init__()
        self.commission = commission
        self._time_adj = time_adjustment
        self._initial_depo = initial_depo

    def run(self,
            trading_system: TradingSystem,
            charts: dict[Instrument, Chart] | ChartContainer,
            **kwargs) -> None:
        if not isinstance(charts, ChartContainer):
            charts = ChartContainer(charts=charts)
        self._trading_system = trading_system
        self.max_trades = trading_system.max_trades
        self._free_balance = self._initial_depo
        self._trades = TradeHeap()

        equity_timeframe: TimeFrame = _utils.min_timeframe(charts.values)
        adj: timedelta = _utils.time_adjustment(
            adj=self._time_adj,
            timeframe=equity_timeframe
        )

        timestamp = _utils.equity_timestamp(charts=charts.values,
                                            timeframe=equity_timeframe)

        self._equity = Equity([],
                              timeframe=equity_timeframe,
                              timestamp=timestamp)

        candle: Candle
        instrument: Instrument
        strategy: Strategy
        chart: Chart

        for curr_time in timestamp + adj:
            self.__handle_closed_trades()
            for strategy, instrument in self._trading_system.items:
                chart = charts[instrument]
                chart = chart[:curr_time]
                candle = chart.latest_before(curr_time)
                self._run_strategy(chart=chart,
                                   candle=candle,
                                   strategy=strategy,
                                   instrument=instrument)
            self._equity.append(self.total_balance)

    def _run_strategy(self,
                      strategy: Strategy,
                      chart: Chart,
                      candle: Candle,
                      instrument: Instrument):
        self._set_symbol(instrument.symbol)
        self._handle_chart(strategy=strategy,
                           candle=candle,
                           chart=chart)

    def __handle_closed_trades(self) -> None:
        self._free_balance += self._trades.closed.profit
        self._trades.cleanup_closed()

    def _handle_event(self, event: Event) -> None:
        event.set_worker(self)
        event.handle_trades(self._trades)

    def _handle_events(self, events: Iterable[Event]) -> None:
        event: Event
        for event in events:
            self._handle_event(event=event)

    def _update_symbol_trades(self, symbol: Symbol, candle: Candle) -> None:
        # Here we update trades by symbol (but not by instrument),
        # because we want to account for price changes

        trade: Trade
        for trade in self._trades:
            if trade._symbol == symbol:
                trade.update(candle=candle)

    def _handle_chart(self,
                      strategy: Strategy,
                      candle: Candle,
                      chart: Chart) -> None:
        events: Iterable[Event]

        strategy.run(chart)
        events = strategy.fetch_events()
        self._handle_events(events=events)
        self._update_symbol_trades(candle=candle,
                                   symbol=self._current_symbol)
