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
from typing import Collection

import pandas as pd
from pandas.api.types import is_numeric_dtype

from xoney.generic._series import TimeSeries
from xoney.generic.candlestick import _validation
from xoney.generic.candlestick import _utils
from xoney.generic.candlestick import Candle
from xoney.generic.timeframes import TimeFrame, DAY_1


class Chart(TimeSeries):
    _df: pd.DataFrame
    timeframe: TimeFrame

    @property
    def close(self) -> pd.Series:
        return self._df["Close"]

    @property
    def open(self) -> pd.Series:
        return self._df["Open"]

    @property
    def high(self) -> pd.Series:
        return self._df["High"]

    @property
    def low(self) -> pd.Series:
        return self._df["Low"]

    @property
    def volume(self) -> pd.Series:
        return self._df["Volume"]

    @property
    def timestamp(self) -> pd.Series:
        return self._df.index

    def __init__(self,
                 open: Collection[float] | None = None,
                 high: Collection[float] | None = None,
                 low: Collection[float] | None = None,
                 close: Collection[float] | None = None,
                 volume: Collection[float] | None = None,
                 timestamp: Collection | None = None,
                 timeframe: TimeFrame = DAY_1):
        if open is None:
            open = []
        if high is None:
            high = []
        if low is None:
            low = []
        if close is None:
            close = []
        if volume is None:
            volume = _utils.default_volume(length=len(close))
        if timestamp is None:
            timestamp = _utils.default_timestamp(length=len(close),
                                                 timeframe=timeframe)

        _params: tuple = (open,
                          high,
                          low,
                          close,
                          volume,
                          timestamp)

        _validation.validate_chart_parameters(*_params)
        _validation.validate_chart_length(*_params)

        self.timeframe = timeframe
        self._df = pd.DataFrame({'Open': open,
                                 'High': high,
                                 'Low': low,
                                 'Close': close,
                                 'Volume': volume,
                                 'Timestamp': timestamp})
        self._df.set_index('Timestamp', inplace=True)

    def __operation(self, other, func):
        if isinstance(other, Chart):
            df = other._df
        else:
            df = pd.DataFrame({'Open': other,
                               'High': other,
                               'Low': other,
                               'Close': other,
                               'Volume': other},
                              index=self._df.index)
        result = self._df.copy()
        for col in ['Open', 'High', 'Low', 'Close', 'Volume']:
            if is_numeric_dtype(result[col]) and is_numeric_dtype(df[col]):
                result[col] = func(result[col], df[col])
        return Chart(open=result['Open'],
                     high=result['High'],
                     low=result['Low'],
                     close=result['Close'],
                     volume=result['Volume'],
                     timestamp=result.index)

    def __add__(self, other):
        return self.__operation(other=other, func=operator.add)

    def __sub__(self, other):
        return self.__operation(other=other, func=operator.sub)

    def __mul__(self, other):
        return self.__operation(other=other, func=operator.mul)

    def __truediv__(self, other):
        # Rearranging low and high to account for
        # intra-candle price fluctuations:
        #   - new high = this high / other low
        #       as maximum possible price.
        #   - new low = this low / other high
        #       as minimum possible price.
        if isinstance(other, Chart):
            other = Chart(open=other._df['Open'],
                          high=other._df['Low'],
                          low=other._df['High'],
                          close=other._df['Close'],
                          volume=other._df['Volume'],
                          timestamp=other._df.index,
                          timeframe=self.timeframe)
        return self.__operation(other=other, func=operator.truediv)

    def __getitem__(self, item):
        result = _utils.auto_loc_iloc(self._df, item)
        if isinstance(result, pd.Series):
            timestamp = result.name
        else:
            timestamp = result.index
        init_params = dict(
            open=result['Open'],
            high=result['High'],
            low=result['Low'],
            close=result['Close'],
            volume=result['Volume'],
            timestamp=timestamp
        )
        if isinstance(item, slice):
            return Chart(**init_params, timeframe=self.timeframe)
        else:
            return Candle(**init_params)

    def __iter__(self):
        for row in self._df.itertuples():
            yield Candle(open=row.Open,
                         high=row.High,
                         low=row.Low,
                         close=row.Close,
                         timestamp=row.Index,
                         volume=row.Volume)

    def __len__(self) -> int:
        return len(self._df["Close"])

    def __eq__(self, other: Chart) -> bool:
        if not isinstance(other, Chart):
            raise TypeError(f"Object is not chart: {other}")

        should_eq: tuple[str, ...] = ("Open", "High", "Low", "Close")
        for attr in should_eq:
            if not _utils.equal_arrays(self._df[attr].values,
                                       other._df[attr].values):
                return False

        if any(self.timestamp != other.timestamp):
            return False

        return True

    def append(self, candle: Candle) -> None:
        if isinstance(candle, Candle):
            self.df = self.df.append(
                {"open": candle.open,
                 "high": candle.high,
                 "low": candle.low,
                 "close": candle.close,
                 "volume": candle.volume,
                 "timestamp": candle.timestamp},
                ignore_index=False)
        else:
            raise TypeError(f"Object is not candle: {candle}")

    def latest_before(self, index) -> Candle:
        return self[:index][-1]
