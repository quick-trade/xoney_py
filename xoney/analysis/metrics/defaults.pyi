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

    def __init__(self):
        ...

    def calculate(self, equity: Equity) -> None:
        profit_per_candle: float
        candles_per_year: float
        profit_per_year: float
        ...


class MaxDrawDown(Metric):
    def calculate(self, equity: Equity) -> None:
        array: np.ndarray
        accumulation: np.ndarray
        max_dd: float
        ...


class CalmarRatio(Metric):
    def calculate(self, equity: Equity) -> None:
        profit: float
        drawdown: float
        ...


class __ProfitStdMetric(Metric, ABC):
    _risk_free: float
    _equity: Equity
    _candles: float | int
    _returns: np.ndarray

    def __init__(self, risk_free: float = 0):
        ...

    def _calculate_profit(self) -> float:
        mean: float
        profit: float
        ...

    @abstractmethod
    def _calculate_standard_deviation(self) -> float:
        ...

    def calculate(self, equity: Equity) -> None:
        profit: float
        std: float
        ...


class SharpeRatio(__ProfitStdMetric):
    def _calculate_standard_deviation(self) -> float:
        ...


class SortinoRatio(__ProfitStdMetric):
    def _calculate_standard_deviation(self) -> float:
        neg_ret: np.ndarray
        sd: float
        ...


def evaluate_metric(metric: type | Metric, equity: Equity) -> float:
    ...
