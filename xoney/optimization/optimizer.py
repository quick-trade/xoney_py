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

import copy
from abc import ABC, abstractmethod

from xoney.analysis.metrics import Metric
from xoney.generic.routes import TradingSystem, Instrument, ChartContainer
from xoney.generic.workers import Worker
from xoney.generic.candlestick import Chart
from xoney.backtesting import Backtester
from xoney.generic.equity import Equity
from xoney.strategy import IntParameter


class Optimizer(Worker, ABC):
    _backtester: Backtester
    _charts: ChartContainer
    _metric: Metric
    _trading_system: TradingSystem
    __max_trades_param: IntParameter | None

    def __init__(self,
                 backtester: Backtester,
                 metric: Metric | type,
                 max_trades: IntParameter | None = None):
        self._backtester = backtester
        self.set_metric(metric=metric)
        self.__max_trades_param = max_trades

    def _initialize_max_trades(self):
        # During the optimization process, the parameter of the maximum
        # number of open trades can change, but if it is not specified,
        # then the strategy has 1 trade for 1 strategy.
        n_strategies = self._trading_system.n_strategies
        if self.__max_trades_param is None:
            min = max = n_strategies
            self._max_trades = IntParameter(min=min,
                                            max=max)
        else:
            self._max_trades = self.__max_trades_param

    def __initialize_metric(self, metric: Metric | type) -> None:
        if isinstance(metric, type):
            metric = metric()
        self._metric = metric

    def set_metric(self, metric: Metric) -> None:
        self.__initialize_metric(metric=metric)

    def _backtest(self, trading_system: TradingSystem) -> Equity:
        tester: Backtester = copy.deepcopy(self._backtester)
        tester.run(charts=self._charts,
                   trading_system=trading_system)
        return tester.equity


    def _system_score(self, trading_system: TradingSystem) -> float:
        return self._backtest(trading_system).evaluate(self._metric)

    @abstractmethod
    def best_systems(self,
                     n: int = 1) -> list[TradingSystem]:  # pragma: no cover
        ...

    @abstractmethod
    def run(self,
            trading_system: TradingSystem,
            charts: dict[Instrument, Chart] | ChartContainer,
            **kwargs) -> None:  # pragma: no cover
        ...
