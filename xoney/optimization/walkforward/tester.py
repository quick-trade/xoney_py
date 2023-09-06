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

from typing import Any
from datetime import timedelta
from xoney.generic.timeframes import TimeFrame

from xoney.generic.workers import Worker
from xoney.generic.equity import Equity
from xoney import TradingSystem, Instrument, Chart
from xoney.generic.routes import ChartContainer
from xoney.config import n_processes
from xoney.optimization import Optimizer
from xoney.optimization.walkforward.sampling import OutOfSample, InSample, walk_forward_timestamp


class WalkForward(Worker):  # TODO
    _optimizer: Optimizer
    _charts: ChartContainer

    __IS: list[InSample]
    __OOS: list[OutOfSample]

    __OOS_len: TimeFrame | timedelta
    __IS_len: TimeFrame | timedelta

    _opt_params: dict[str, Any]
    _bt_params: dict[str, Any]


    def __init__(self,
                 charts: dict[Instrument, Chart] | ChartContainer,
                 IS_len: TimeFrame | timedelta,
                 OOS_len: TimeFrame | timedelta) -> None:
        if not isinstance(charts, ChartContainer):
            charts = ChartContainer(charts=charts)
        super().__init__()
        self._charts = charts
        self.__IS_len = IS_len
        self.__OOS_len = OOS_len

    def __split_samples(self) -> None:
        IS_time, OOS_time = walk_forward_timestamp(
            start_time=self._charts.start,
            end_time=self._charts.end,
            OOS_len=self.__OOS_len,
            IS_len=self.__IS_len,
            step=self.__OOS_len
        )
        self.__IS = [InSample(charts=self._charts[idx]) for idx in IS_time]
        self.__OOS = [OutOfSample(charts=self._charts[idx]) for idx in OOS_time]

    # TODO: edit metric function (evaluate only representative data)
    def run(self,
            optimizer: Optimizer,
            trading_system: TradingSystem,
            opt_params: dict[str, Any] | None = None,
            bt_params: dict[str, Any] | None = None,
            n_jobs: int | None = None,
            *args,
            **kwargs) -> None:
        if n_jobs is None:
            n_jobs = n_processes
        self.__split_samples()
        self._trading_system = trading_system
        self._optimizer = optimizer
        self._opt_params = opt_params
        self._bt_params = bt_params
        self.__optimize_IS()
        self.__backtest_OOS()

    def __optimize_IS(self) -> None:
        IS: InSample

        for IS in self.__IS:
            IS.optimize(self._trading_system,
                        optimizer=self._optimizer,
                        opt_params=self._opt_params)

    def __backtest_OOS(self) -> None:
        IS: InSample
        OOS: OutOfSample

        for IS, OOS in zip(self.__IS, self.__OOS):
            OOS.backtest(trading_system=IS.select_system(),
                         backtester=self._optimizer._backtester,
                         bt_kwargs=self._bt_params)

    @property
    def equities(self) -> list[Equity]:
        return [oos.equity for oos in self.__OOS]

    @property
    def out_of_samples(self) -> list[OutOfSample]:
        return self.__OOS
