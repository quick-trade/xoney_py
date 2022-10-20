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

from abc import ABC, abstractmethod

import numpy as np

from xoney.generic.equity import Equity
from xoney.analysis.regression import ExponentialRegression


class Metric(ABC):
    _value: float
    _positive: bool

    @property
    def positive(self) -> bool:
        return self._positive

    @property
    def value(self) -> float:
        return self._value

    @abstractmethod
    def calculate(self, equity: Equity) -> None:
        ...


class YearProfit(Metric):
    __model: ExponentialRegression
    _positive = True

    def __init__(self):
        self.__model = ExponentialRegression()

    def calculate(self, equity: Equity) -> None:
        self.__model.fit(array=equity.as_array())

        regression = self.__model.curve

        profit_per_candle: float = regression[1] / regression[0]
        candles_per_year: float = equity.timeframe.candles_in_year

        profit_per_year: float = profit_per_candle ** candles_per_year

        self._value = profit_per_year


class MaxDrawDown(Metric):
    _positive = False

    def calculate(self, equity: Equity) -> None:
        array: np.ndarray = equity.as_array()
        accumulation: np.ndarray = np.maximum.accumulate(array)
        max_dd: float = -np.min(array / accumulation - 1)

        self._value = max_dd


class CalmarRatio(Metric):
    _positive = True

    def calculate(self, equity: Equity) -> None:
        profit: float = evaluate_metric(YearProfit, equity)
        drawdown: float = evaluate_metric(MaxDrawDown, equity)

        self._value = profit / drawdown


class SharpeRatio(Metric):
    __risk_free: float
    _positive = True

    def __init__(self, risk_free: float = 0):
        self.__risk_free = risk_free

    def calculate(self, equity: Equity) -> None:
        candles_per_year: float = equity.timeframe.candles_in_year
        array: np.ndarray = equity.as_array()
        returns: np.ndarray = np.diff(array) / array[:-1]
        standard_deviation: float = returns.std() * np.sqrt(candles_per_year)
        mean: float = returns.mean() * candles_per_year

        self._value = (mean - self.__risk_free) / standard_deviation


class SortinoRatio(Metric):
    _positive = True
    __risk_free: float

    def __init__(self, risk_free: float = 0):
        self.__risk_free = risk_free

    def calculate(self, equity: Equity) -> None:
        candles_per_year: float = equity.timeframe.candles_in_year
        array: np.ndarray = equity.as_array()
        returns: np.ndarray = np.diff(array) / array[:-1]

        neg_ret: np.ndarray = returns[returns < 0]

        standard_deviation: float = neg_ret.std() * np.sqrt(candles_per_year)
        mean: float = returns.mean() * candles_per_year

        self._value = (mean - self.__risk_free) / standard_deviation


def evaluate_metric(metric: type | Metric, equity: Equity) -> float:
    if isinstance(metric, type):
        metric: Metric = metric()
    metric.calculate(equity=equity)
    return metric.value
