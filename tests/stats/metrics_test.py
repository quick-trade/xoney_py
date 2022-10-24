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
import numpy as np

from xoney.analysis.metrics import *
from xoney.generic.equity import Equity
from xoney.generic.timeframes import *

from xoney.math import is_equal

import pytest


@pytest.fixture
def equity_d1_exp():
    return Equity([1, 2, 4, 8])


@pytest.fixture
def equity_h1_exp():
    return Equity([1, 1.01, 1.01**2], timeframe=HOUR_1)

@pytest.fixture
def equity_d1_1_pct():
    return Equity([1, 1.01, 1.01**2, 1.01**3], timeframe=DAY_1)


@pytest.fixture
def equity_1d_15_pct_dd():
    return Equity([100, 110, 110*0.9, 100, 110*0.85, 150, 140],
                  timeframe=DAY_1)


class TestYearProfit:
    def test_d1(self, equity_d1_exp):
        metric = YearProfit()
        metric.calculate(equity=equity_d1_exp)

        assert is_equal(metric.value, 2**365)

    def test_h1(self, equity_h1_exp):
        metric = YearProfit()
        metric.calculate(equity=equity_h1_exp)

        assert is_equal(metric.value, 1.01**(365*24))


class TestMaxDrawDown:
    def test_d1(self, equity_d1_exp):
        value = evaluate_metric(MaxDrawDown(), equity=equity_d1_exp)
        assert is_equal(value, 0.0)

    def test_h1(self, equity_h1_exp):
        value = evaluate_metric(MaxDrawDown, equity=equity_h1_exp)
        assert is_equal(value, 0.0)

    def test_d1_15_pct(self, equity_1d_15_pct_dd):
        metric = MaxDrawDown()
        metric.calculate(equity_1d_15_pct_dd)

        assert is_equal(metric.value, 0.15)


class TestCalmarRatio:
    def test_d1(self, equity_d1_exp):
        value = evaluate_metric(CalmarRatio, equity_d1_exp)
        assert is_equal(value, np.inf)

    def test_d1_15_pct(self, equity_1d_15_pct_dd):
        value = evaluate_metric(CalmarRatio, equity_1d_15_pct_dd)
        expected = evaluate_metric(
            YearProfit,
            equity_1d_15_pct_dd
        ) / 0.15
        assert is_equal(value,
                        expected)


class TestSharpeRatio:
    def test_1h(self, equity_h1_exp):
        value = evaluate_metric(SharpeRatio, equity_h1_exp)
        mean_profit = equity_h1_exp.change().mean()
        std_profit = equity_h1_exp.change().std()
        candles_sqrt = np.sqrt(equity_h1_exp.timeframe.candles_in_year)
        expected = (mean_profit / std_profit) * candles_sqrt
        assert is_equal(value, expected)

    def test_d1_15_pct(self, equity_1d_15_pct_dd):
        value = evaluate_metric(SharpeRatio, equity_1d_15_pct_dd)
        mean_profit = equity_1d_15_pct_dd.change().mean()
        std_profit = equity_1d_15_pct_dd.change().std()
        candles_sqrt = np.sqrt(equity_1d_15_pct_dd.timeframe.candles_in_year)
        expected = (mean_profit / std_profit) * candles_sqrt
        assert is_equal(value, expected)


class TestSortinoRatio:
    @pytest.mark.parametrize("risk_free",
                             [1,
                              0.05,
                              0.2])
    def test_d1_15_pct(self, equity_1d_15_pct_dd, risk_free):
        value = evaluate_metric(SortinoRatio(risk_free=risk_free),
                                equity_1d_15_pct_dd)
        candles = equity_1d_15_pct_dd.timeframe.candles_in_year
        returns = equity_1d_15_pct_dd.change().as_array()
        mean_profit = returns.mean()
        std_profit = returns[returns < 0].std()

        expected = (mean_profit * candles - risk_free) / \
                   (std_profit * candles**0.5)
        assert is_equal(value, expected)

