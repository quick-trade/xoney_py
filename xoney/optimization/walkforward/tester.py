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

from xoney.generic.workers import Worker
from xoney.generic.equity import Equity
from xoney import TradingSystem, Instrument, Chart
from xoney.config import n_processes
from xoney.optimization import Optimizer
from xoney.optimization.walkforward.sampling import OutOfSample, InSample


class WalkForward(Worker):  # TODO
    _optimizer: Optimizer
    _charts: dict[Instrument, Chart]

    __IS: list[InSample]
    __OOS: list[OutOfSample]


    def __init__(self, charts: dict[Instrument, Chart]) -> None:
        super().__init__()
        self._charts = charts
        self.__split_samples()

    def __split_samples(self) -> None:
        self.__IS = ...
        self.__OOS = ...

    def run(self,
            optimizer: Optimizer,
            trading_system: TradingSystem,
            n_jobs: int | None = None,
            *args,
            **kwargs) -> None:
        if n_jobs is None:
            n_jobs = n_processes
        self.__optimize_IS()
        self.__backtest_OOS()

    @property
    def equities(self) -> list[Equity]:
        return [oos.equity for oos in self.__OOS]

    @property
    def out_of_samples(self) -> list[OutOfSample]:
        return self.__OOS
