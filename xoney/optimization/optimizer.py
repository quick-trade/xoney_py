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
from xoney.generic.routes import TradingSystem, Instrument
from xoney.generic.workers import Worker
from xoney.generic.candlestick import Chart
from xoney.backtesting import Backtester


class Optimizer(Worker, ABC):
    _backtester: Backtester
    _charts: dict[Instrument, Chart]
    _commission: float
    _metric: Metric

    def __init__(self,
                 backtester: Backtester):
        self._backtester = backtester

    def _system_score(self, trading_system: TradingSystem) -> float:
        tester: Backtester = copy.deepcopy(self._backtester)
        tester.run(charts=self._charts,
                   trading_system=trading_system,
                   commission=self._commission)
        return tester.equity.evaluate(self._metric)

    @abstractmethod
    def best_systems(self,
                     n: int = 1) -> list[TradingSystem]:  # pragma: no cover
        ...

    @abstractmethod
    def run(self,
            trading_system: TradingSystem,
            charts: dict[Instrument, Chart],
            metric: Metric | type,
            commission: float = 0.1 * 0.01,
            min_trades: int | None = None,
            max_trades: int | None = None,
            **kwargs) -> None:  # pragma: no cover
        ...
