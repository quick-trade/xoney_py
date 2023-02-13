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

from xoney import math
from xoney.analysis.regression import ExponentialRegression


class Metric(ABC):
    @property
    def positive(self):
        return self._positive

    @property
    def value(self):
        return self._value

    @abstractmethod
    def calculate(self, equity):  # pragma: no cover
        ...


class YearProfit(Metric):
    _positive = True

    def __init__(self):
        self.__model = ExponentialRegression()

    def calculate(self, equity):
        self.__model.fit(array=equity.as_array())

        regression = self.__model.curve

        profit_per_candle = regression[1] / regression[0]
        candles_per_year = equity.timeframe.candles_in_year

        profit_per_year = profit_per_candle ** candles_per_year

        self._value = profit_per_year


class MaxDrawDown(Metric):
    _positive = False

    def calculate(self, equity):
        array = equity.as_array()
        accumulation = np.maximum.accumulate(array)
        max_dd = -np.min(array / accumulation - 1)

        self._value = max_dd


class CalmarRatio(Metric):
    _positive = True

    def calculate(self, equity):
        profit = equity.evaluate(YearProfit)
        drawdown = equity.evaluate(MaxDrawDown)

        self._value = math.divide(profit, drawdown)


class __ProfitStdMetric(Metric, ABC):
    _positive = True

    def __init__(self, risk_free=0):
        self._risk_free = risk_free

    def _calculate_profit(self):
        self._candles = self._equity.timeframe.candles_in_year
        self._returns = self._equity.change().as_array()

        mean = self._returns.mean()
        profit = mean * self._candles - self._risk_free

        return profit

    @abstractmethod
    def _calculate_standard_deviation(self):  # pragma: no cover
        ...

    def calculate(self, equity):
        self._equity = equity
        profit = self._calculate_profit()
        std = self._calculate_standard_deviation()

        self._value = math.divide(profit, std)


class SharpeRatio(__ProfitStdMetric):
    def _calculate_standard_deviation(self):
        return self._returns.std() * np.sqrt(self._candles)


class SortinoRatio(__ProfitStdMetric):
    def _calculate_standard_deviation(self):
        neg_ret = self._returns[self._returns < 0]

        sd = neg_ret.std()
        return sd * np.sqrt(self._candles)


def evaluate_metric(metric, equity):
    if isinstance(metric, type):
        metric = metric()
    metric.calculate(equity=equity)
    return metric.value
