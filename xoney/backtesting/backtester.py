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

from xoney.generic.candlestick import Chart, Candle
from xoney.generic.routes import Instrument, TradingSystem
from xoney.generic.symbol import Symbol
from xoney.generic.workers import EquityWorker
from xoney.generic.trades import TradeHeap, Trade
from xoney.generic.events import Event
from xoney.generic.equity import Equity
from xoney.analysis.index_transform import charts_length, unify_series

from typing import Iterable

from xoney.strategy import Strategy

import numpy as np


def _unify_instruments_charts(
        charts: dict[Instrument, Chart]
) -> dict[Instrument, Chart]:
    instruments, charts = zip(*charts.items())
    charts = unify_series(charts)
    return {instrument: chart 
            for instrument, chart in 
            zip(instruments, charts)}

def _is_nan_candle(candle: Candle) -> bool:
    return candle.close == np.nan


def _drop_na_chart(chart: Chart) -> Chart:
    dropped: Chart = Chart(timeframe=chart.timeframe)
    for candle in chart:
        if not _is_nan_candle(candle=candle):
            dropped.append(candle)
    return dropped


class Backtester(EquityWorker):  # TODO
    _equity: Equity
    _initial_depo: float

    @property
    def equity(self) -> Equity:
        return self._equity

    @property
    def free_balance(self) -> float:
        return self._free_balance

    def __init__(self,
                 initial_depo: float = 100.0):
        self._initial_depo = initial_depo

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
        """
        Here we update trades by symbol (but not by instrument), 
        because we want to account for price changes
        
        """

        trade: Trade
        for trade in self._trades:
            if trade._symbol == symbol:
                trade.update(candle=candle)

    def _handle_chart(self,
                      strategy: Strategy,
                      candle: Candle,
                      chart: Chart) -> None:
        events: Iterable[Event]

        if not _is_nan_candle(candle=candle):
            self._update_symbol_trades(candle=candle,
                                       symbol=self._current_symbol)
            strategy.run(chart)
            events = strategy.fetch_events()
            self._handle_events(events=events)

    def _run_strategy(self,
                      strategy: Strategy,
                      chart: Chart,
                      candle: Candle,
                      instrument: Instrument):
        self.set_symbol(instrument.symbol)
        self._handle_chart(strategy=strategy,
                           candle=candle,
                           chart=chart)

    def run(self,
            trading_system: TradingSystem,
            charts: dict[Instrument, Chart],
            commission: float = 0.1 * 0.01,
            **kwargs) -> None:
        self._trading_system = trading_system
        self._free_balance = self._initial_depo
        self._trades = TradeHeap()
        self.commission = commission

        self._equity = Equity([],
                              timeframe=...,
                              timestamp=...)  # TODO

        candle: Candle
        instrument: Instrument
        strategy: Strategy
        na_chart: Chart
        chart: Chart

        unified_charts: dict[Instrument, Chart] = _unify_instruments_charts(
            charts=charts
        )
        chart_length: int = charts_length(unified=unified_charts)

        for curr_index in range(chart_length):
            self.__handle_closed_trades()
            for strategy, instrument in self._trading_system.items:
                na_chart = unified_charts[instrument]
                candle = na_chart[curr_index]
                chart = _drop_na_chart(chart=na_chart[:curr_index])
                self._run_strategy(chart=chart,
                                   candle=candle,
                                   strategy=strategy,
                                   instrument=instrument)
            self._equity.append(self.total_balance)
