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

import numpy as np
import pandas as pd

from xoney.generic.timeframes.template import TimeFrame
from xoney.config import DEFAULT_CURR_TIME


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


def equal_arrays(array_1: np.ndarray, array_2: np.ndarray) -> bool:
    if array_1.shape != array_2.shape:
        return False
    return all(array_1 == array_2)


def default_timestamp(length: int, timeframe: TimeFrame) -> pd.TimedeltaIndex:
    start = -timeframe.timedelta * (length-1)

    return DEFAULT_CURR_TIME + pd.timedelta_range(
        start=start,
        end=0,
        periods=length
    )


def auto_loc_iloc(df: pd.DataFrame, index):
    try:
        return df.loc[index]
    except:
        return df.iloc[index]
