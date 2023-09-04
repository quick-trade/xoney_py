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

import pandas as pd

from xoney.generic.timeframes import TimeFrame
from xoney import Chart

from typing import Collection, Iterable


def min_timeframe(charts: Iterable) -> TimeFrame:
    c: Chart
    timeframes: list[TimeFrame] = [c.timeframe for c in charts]
    return min(timeframes)


def time_adjustment(adj: float | TimeFrame | timedelta,
                    timeframe: TimeFrame) -> timedelta:
    if isinstance(adj, float):
        return timeframe.timedelta * adj
    elif isinstance(adj, TimeFrame):
        return adj.timedelta
    elif isinstance(adj, timedelta):
        return adj
    raise ValueError(
        "Invalid time adjustment. It should be "
        "a positive number, timeframe, or datetime.timedelta ")


def _equity_start_stop(timestamps: Collection[pd.Series]) -> tuple:
    latest_start = max(ts[0] for ts in timestamps)
    latest_end = max(ts[-1] for ts in timestamps)
    return latest_start, latest_end


def equity_timestamp(charts: Collection[Chart],
                     timeframe: TimeFrame) -> pd.Timestamp:
    start, stop = _equity_start_stop([c.timestamp for c in charts])
    return pd.date_range(start=start,
                         end=stop,
                         freq=timeframe.timedelta)
