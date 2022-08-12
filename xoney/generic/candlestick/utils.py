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
# WITHOUT WARRANTIES OR CONDITIONS OF ANY KIND, either express or implied.
# See the License for the specific language governing permissions and
# limitations under the License.
# =============================================================================

from __future__ import annotations

import datetime as dt

from xoney.generic.timeframes import TimeFrame


def start_from_end(delta: dt.timedelta,
                   period: int,
                   end: dt.datetime) -> dt.datetime:
    start: dt.datetime = end - delta * period
    return start


def date_range(timeframe: TimeFrame,
               length: int,
               start: dt.datetime | None = None) -> list[dt.datetime]:
    delta: dt.timedelta = timeframe.timedelta
    index: list[dt.datetime]
    candle: int

    if start is None:
        start = start_from_end(delta=delta,
                               period=length,
                               end=dt.datetime.now())
    index = [start + delta * candle for candle in range(length)]

    return index


def default_volume(length: int) -> list[float]:
    if not isinstance(length, int):
        raise TypeError("<length> parameter must be of type <int>, "
                        f"but received: {type(length)}")

    _: int
    return [1.0 for _ in range(length)]

def _index_from_timestamp_index(index, timestamp: list) -> int:
    if not isinstance(index, int):
        index = timestamp.index(index)
    return index

def _slice_from_timestamp_slice(slice_: slice, timestamp: list) -> slice:
    result_slice_args: list = []
    for index in (slice_.start, slice_.stop):
        if index is not None:
            index = _index_from_timestamp_index(index=index,
                                                timestamp=timestamp)
        result_slice_args.append(index)
    return slice(*result_slice_args, slice_.step)

def to_int_index(item, timestamp: list) -> int | slice:
    if isinstance(item, slice):
        return _slice_from_timestamp_slice(slice_=item, timestamp=timestamp)
    return _index_from_timestamp_index(index=item, timestamp=timestamp)
