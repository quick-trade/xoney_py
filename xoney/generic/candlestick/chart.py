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

import operator
import datetime as dt
from typing import Collection

import numpy as np

from xoney.generic.candlestick import _validation
from xoney.generic.candlestick import utils
from xoney.generic.candlestick import Candle


class Chart:
    _open: np.ndarray
    _high: np.ndarray
    _low: np.ndarray
    _close: np.ndarray
    _volume: np.ndarray
    _timestamp: list[None | dt.datetime]

    @property
    def open(self) -> np.ndarray:
        return self._open

    @property
    def high(self) -> np.ndarray:
        return self._high

    @property
    def low(self) -> np.ndarray:
        return self._low

    @property
    def close(self) -> np.ndarray:
        return self._close

    @property
    def timestamp(self) -> list[dt.datetime | None]:
        return self._timestamp

    @property
    def volume(self) -> np.ndarray[float]:
        return self._volume

    def __init__(self,
                 open: Collection[float] | None = None,
                 high: Collection[float] | None = None,
                 low: Collection[float] | None = None,
                 close: Collection[float] | None = None,
                 volume: Collection[float] | None = None,
                 timestamp: Collection[dt.datetime | None] | None = None):
        if open is None:
            open = []
        if high is None:
            high = []
        if low is None:
            low = []
        if close is None:
            close = []
        if volume is None:
            volume = utils.default_volume(length=len(close))
        if timestamp is None:
            timestamp = [None for _ in close]

        _validation.validate_chart_length(open,
                                          high,
                                          low,
                                          close,
                                          volume,
                                          timestamp)

        self._open = np.array(open)
        self._high = np.array(high)
        self._low = np.array(low)
        self._close = np.array(close)
        self._volume = np.array(volume)
        self._timestamp = list(timestamp)

    def __operation(self, other, func):
        if isinstance(other, Chart):
            open = other._open
            high = other._high
            low = other._low
            close = other._close
        else:
            open = high = low = close = other
        return self.__class__(open=func(self._open, open),
                              high=func(self._high, high),
                              low=func(self._low, low),
                              close=func(self._close, close))

    def __truediv__(self, other):
        # Rearranging low and high to account for
        # intra-candle price fluctuations:
        #   - new high = this high / other low
        #       as maximum possible price.
        #   - new low = this low / other high
        #       as minimum possible price.
        if isinstance(other, Chart):
            other = self.__class__(open=other._open,
                                   high=other._low,
                                   low=other._high,
                                   close=other._close,
                                   volume=other._volume,
                                   timestamp=other._timestamp)
        return self.__operation(other=other, func=operator.truediv)

    def __getitem__(self, item):
        dict_init_params: dict = dict(
            open=self._open[item],
            high=self._high[item],
            low=self._low[item],
            close=self._close[item],
            timestamp=self._timestamp[item],
            volume=self._volume[item])
        if isinstance(item, slice):
            return Chart(**dict_init_params)
        return Candle(**dict_init_params)

    def __iter__(self):
        for o, h, l, c, v, t in zip(self._open,
                                    self._high,
                                    self._low,
                                    self._close,
                                    self._volume,
                                    self._timestamp):
            yield Candle(open=o,
                         high=h,
                         low=l,
                         close=c,
                         timestamp=t,
                         volume=v)

    def __len__(self) -> int:
        return len(self._close)
