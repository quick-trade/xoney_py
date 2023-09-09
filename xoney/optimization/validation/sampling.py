# Copyright 2023 Vladyslav Kochetov. All Rights Reserved.
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

from abc import ABC, abstractmethod
from dataclasses import dataclass

from xoney import ChartContainer, TradingSystem
from xoney.optimization import Optimizer
from xoney.backtesting import Backtester
from xoney.generic import Equity



class TrainingSample(ABC):
    _optimizer: Optimizer
    _charts: ChartContainer

    def optimize(self, system: TradingSystem) -> None:
        self._optimizer.run(trading_system=system,
                            charts=self._charts)

    def best_system(self) -> TradingSystem:
        return self._optimizer.best_systems(1)[0]


class ValidationSample(ABC):
    _backtester: Backtester

    @abstractmethod
    def backtest(self, system: TradingSystem) -> Equity:  # pragma: no cover
        ...


@dataclass
class SamplePair:
    training: TrainingSample
    validation: ValidationSample


class Sampler(ABC):
    @abstractmethod
    def samples(self, charts: ChartContainer) -> list[SamplePair]:  # pragma: no cover
        ...
