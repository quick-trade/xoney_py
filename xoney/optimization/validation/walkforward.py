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

from datetime import timedelta, datetime
from copy import deepcopy

from xoney import ChartContainer, TradingSystem
from xoney.backtesting import Backtester
from xoney.generic import Equity
from xoney.generic.timeframes import TimeFrame
from xoney.optimization import Optimizer
from xoney.optimization.validation.sampling import SamplePair, Sampler, ValidationSample, TrainingSample


class InSample(TrainingSample):
    _source_charts: ChartContainer
    _period: slice

    def __init__(self,
                 charts: ChartContainer,
                 period: slice,
                 optimizer: Optimizer) -> None:
        self._source_charts = charts
        self._period = period
        self._optimizer = deepcopy(optimizer)

    def optimize(self, system: TradingSystem) -> None:
        # TODO: optimize for small datasets
        self._charts = self._source_charts[self._period]
        return super().optimize(system)


class OutOfSample(ValidationSample):
    _source_charts: ChartContainer
    _period: slice

    def __init__(self,
                 charts: ChartContainer,
                 period: slice,
                 backtester: Backtester) -> None:
        self._source_charts = charts
        self._period = period
        self._backtester = deepcopy(backtester)

    def backtest(self, system: TradingSystem) -> Equity:
        idx = slice(
            self._period.start - system.min_duration,
            self._period.stop
        )
        self._charts = self._source_charts[idx]
        return self._backtester.run(trading_system=system, charts=self._charts)


class WFSampler(Sampler):
    _IS_len: TimeFrame | timedelta
    _OOS_len: TimeFrame | timedelta

    __backtester: Backtester
    __optimizer: Optimizer

    def __init__(self,
                 IS_len: TimeFrame | timedelta,
                 OOS_len: TimeFrame | timedelta,
                 optimizer: Optimizer,
                 backtester: Backtester) -> None:
        self.__backtester = backtester
        self.__optimizer = optimizer
        self._IS_len = IS_len
        self._OOS_len = OOS_len


    def samples(self, charts: ChartContainer) -> list[SamplePair]:
        IS_time, OOS_time = walk_forward_timestamp(
            start_time=charts.start,
            end_time=charts.end,
            OOS_len=self._OOS_len,
            IS_len=self._IS_len,
            step=self._OOS_len
        )
        IS = [InSample(charts=charts,
                       period=idx,
                       optimizer=self.__optimizer)
              for idx in IS_time]
        OOS = [OutOfSample(charts=charts,
                           period=idx,
                           backtester=self.__backtester)
               for idx in OOS_time]
        return [SamplePair(training=in_sample, validation=out_of_sample)
                for in_sample, out_of_sample in zip(IS, OOS)]

def _to_timedelta(value) -> timedelta:
    if isinstance(value, timedelta):
        return value
    if isinstance(value, TimeFrame):
        return value.timedelta
    raise ValueError(f"{value} is not of type <TimeFrame> or <timedelta>")


def walk_forward_timestamp(start_time: datetime,
                           end_time: datetime,
                           IS_len: TimeFrame | timedelta,
                           OOS_len: TimeFrame | timedelta,
                           step: TimeFrame | timedelta | None = None) -> tuple[list[slice], list[slice]]:
    IS_len = _to_timedelta(IS_len)
    OOS_len = _to_timedelta(IS_len)
    if step is None:
        step = OOS_len
    else:
        step = _to_timedelta(step)

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
