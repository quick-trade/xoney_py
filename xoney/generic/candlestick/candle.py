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

from typing import Any

import copy
from numbers import Number

import numpy as np

from xoney.generic.candlestick._validation import validate_ohlc


class Candle:
    open: int | float
    high: int | float
    low: int | float
    close: int | float

    volume: float | None
    timestamp: Any


    @property
    def _array(self):
        return np.array([self.open,
                         self.high,
                         self.low,
                         self.close])

    def __init__(self,
                 open: int | float,
                 high: int | float,
                 low: int | float,
                 close: int | float,
                 timestamp: Any = None,
                 volume: float | None = None):
        validate_ohlc(open=open,
                      high=high,
                      low=low,
                      close=close)
        self.open = open
        self.high = high
        self.low = low
        self.close = close
        self.volume = volume
        self.timestamp = timestamp

    def as_array(self) -> np.ndarray:
        return self._array

    def __array_to_candle(self, array: np.ndarray):
        return self.__class__(*array,
                              timestamp=self.timestamp,
                              volume=self.volume)

    def __neg__(self):
        return self.__array_to_candle(-self._array)

    def __pos__(self):
        return copy.deepcopy(self)

    def __abs__(self):
        return self.__array_to_candle(abs(self._array))

    def __add__(self, other):
        if isinstance(other, Candle):
            other = other.as_array()
        elif not isinstance(other, (np.ndarray, Number)):
            raise TypeError("To add something to a candle, the "
                            "object must be of type <Candle>, "
                            "<numpy.ndarray> or <Number>")
        return self.__array_to_candle(self._array + other)

    def __sub__(self, other):
        if isinstance(other, Candle):
            other = other.as_array()
        elif not isinstance(other, (np.ndarray, Number)):
            raise TypeError("To subtract something from a candle, the "
                            "object must be of type <Candle>, "
                            "<numpy.ndarray> or <Number>")
        return self.__array_to_candle(self._array - other)

    def __mul__(self, other):
        if isinstance(other, Candle):
            other = other.as_array()
        elif not isinstance(other, (np.ndarray, Number)):
            raise TypeError("To multiply candle by something, the "
                            "object must be of type <Candle>, "
                            "<numpy.ndarray> or <Number>")
        return self.__array_to_candle(self._array * other)

    def __truediv__(self, other):
        if isinstance(other, Candle):
            candle: Candle = copy.deepcopy(other)
            candle.high = other.low
            candle.low = other.high
            # Rearranging low and high to account for
            # intra-candle price fluctuations:
            #   - new high = this high / other low
            #       as maximum possible price.
            #   - new low = this low / other high
            #       as minimum possible price.
            divider = candle.as_array()
        elif not isinstance(other, (np.ndarray, Number)):
            raise TypeError("To divide candle by something, the "
                            "object must be of type <Candle>, "
                            "<numpy.ndarray> or <Number>")
        else:
            divider = other
        return self.__array_to_candle(self._array / divider)

    def __eq__(self, other):
        if isinstance(other, Candle):
            matches = self._array == other.as_array()
            return matches.all()
        raise TypeError(f"Object is not candle: {other}")

    def __lt__(self, other):
        if isinstance(other, Candle):
            other = other.low
        return self.high < other

    def __gt__(self, other):
        if isinstance(other, Candle):
            other = other.high
        return self.low > other

    def __ge__(self, other):
        if isinstance(other, Candle):
            other = other.high
        return self.low >= other

    def __le__(self, other):
        if isinstance(other, Candle):
            other = other.low
        return self.high <= other

    def __contains__(self, item):
        return self.low <= item <= self.high
