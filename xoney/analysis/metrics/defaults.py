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
from abc import ABC, abstractmethod

from xoney.generic.equity import Equity
from xoney.analysis.regression import (RegressionModel,
                                       ExponentialRegression,
                                       LinearRegression)


class Metric(ABC):
    _value: float

    @property
    def value(self) -> float:
        return self._value

    @abstractmethod
    def calculate(self, equity: Equity) -> None:
        ...


class YearProfit(Metric):
    __model: ExponentialRegression

    def __init__(self):
        self.__model = ExponentialRegression()

    def calculate(self, equity: Equity) -> None:
        self.__model.fit(array=equity.as_array())

        regression = self.__model.curve

        profit_per_candle: float = regression[1] / regression[0]
        candles_per_year: float = equity.timeframe.candles_in_year

        profit_per_year: float = profit_per_candle ** candles_per_year

        self._value = profit_per_year
