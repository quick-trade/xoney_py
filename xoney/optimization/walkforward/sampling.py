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
from abc import ABC
from datetime import datetime, timedelta

from xoney import Instrument, Chart, TradingSystem
from xoney.generic.routes import ChartContainer
from xoney.backtesting import Backtester
from xoney.generic.equity import Equity
from xoney.generic.timeframes.template import TimeFrame
from xoney.optimization import Optimizer

import copy


class Sample(ABC):
    charts: ChartContainer
    _deepcopy: bool


    def __init__(self,
                 charts: dict[Instrument, Chart] | ChartContainer,
                 deepcopy: bool = True,
                 *args,
                 **kwargs) -> None:
        if not isinstance(charts, ChartContainer):
            charts = ChartContainer(charts=charts)
        self.charts = charts
        self._deepcopy = deepcopy


class InSample(Sample):
    _optimizer: Optimizer
    _opt_params: dict[str, Any]

    def optimize(self,
                 trading_system: TradingSystem,
                 optimizer: Optimizer,
                 opt_params: dict[str, Any] | None = None) -> None:
        if self._deepcopy:
            optimizer = copy.deepcopy(optimizer)
        self._optimizer = optimizer
        if opt_params is None:
            opt_params = dict()
        self._opt_params = opt_params
        self._optimizer.run(trading_system=trading_system,
                            charts=self.charts,
                            **self._opt_params)

    def select_system(self) -> TradingSystem:
        return self._optimizer.best_systems(n=1)[0]


class OutOfSample(Sample):
    bt_params: dict[str, Any]
    _backtester: Backtester
    __equity: Equity
    __trading_system: TradingSystem


    @property
    def equity(self):
        return self.__equity

    @property
    def trading_system(self) -> TradingSystem:
        return self.__trading_system

    def backtest(self,
                 trading_system: TradingSystem,
                 backtester: Backtester,
                 bt_kwargs: dict[str, Any] | None = None):
        if self._deepcopy:
            backtester = copy.deepcopy(backtester)
        self._backtester = backtester
        if bt_kwargs is None:
            bt_kwargs = dict()
        self.bt_params = bt_kwargs

        self._backtester.run(trading_system=trading_system,
                             charts=self.charts,
                             **self.bt_params)
        self.__equity = self._backtester.equity
        self.__trading_system = trading_system


def _to_timedelta(value) -> timedelta:
    if isinstance(value, timedelta):
        return value
    if isinstance(value, TimeFrame):
        return value.timedelta
    raise ValueError(f"{value} is not of type <TimeFrame> or <timedelta>")


# TODO: Make allowance for the minimum number of candles for the trading system.
def walk_forward_timestamp(start_time: datetime,
                           end_time: datetime,
                           IS_len: TimeFrame | timedelta,
                           OOS_len: TimeFrame | timedelta,
                           step: TimeFrame | timedelta | None = None) -> tuple[list[slice], list[slice]]:
    if step is None:
        step = timedelta(0, 0, 0, 0, 0, 0, 0)
    else:
        step = _to_timedelta(step)

    IS_len = _to_timedelta(IS_len)
    OOS_len = _to_timedelta(IS_len)

    IS_ranges = []
    OOS_ranges = []
    current_time = start_time

    while current_time + IS_len + OOS_len <= end_time:
        IS_end = current_time + IS_len
        OOS_end = IS_end + OOS_len

        IS_ranges.append(slice(current_time, IS_end))
        OOS_ranges.append(slice(IS_end, OOS_end))

        current_time += step

    return IS_ranges, OOS_ranges
