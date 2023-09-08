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

from multiprocessing import Pool
from xoney.config import cpu_count

from xoney import ChartContainer, TradingSystem
from xoney.optimization.validation.sampling import Sampler, SamplePair
from xoney.generic.equity import Equity


class Validator:
    _pairs: list[SamplePair]
    _equities: list[Equity]

    def __init__(self,
                 charts: ChartContainer,
                 sampler: Sampler) -> None:
        self._pairs = sampler.samples(charts=charts)

    def test(self,
             system: TradingSystem,
             n_jobs: int | None = None):
        pool = Pool(n_jobs if n_jobs is not None else cpu_count)
        def test(pair: SamplePair) -> Equity:
            pair.training.optimize(system=system)
            best = pair.training.best_system()
            return pair.validation.backtest(best)
        self._equities = pool.map(test, self._pairs)

    @property
    def equities(self) -> list[Equity]:
        return self._equities
