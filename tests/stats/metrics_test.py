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
from xoney.analysis.metrics import YearProfit
from xoney.generic.equity import Equity
from xoney.generic.timeframes import HOUR_1

from xoney.math import is_equal

import pytest


@pytest.fixture
def equity_d1_exp():
    return Equity([1, 2, 4, 8])

@pytest.fixture
def equity_h1_exp():
    return Equity([1, 1.01, 1.01**2], timeframe=HOUR_1)

class TestYearProfit:
    def test_d1(self, equity_d1_exp):
        metric = YearProfit()
        metric.calculate(equity=equity_d1_exp)

        assert is_equal(metric.value, 2**365)

    def test_h1(self, equity_h1_exp):
        metric = YearProfit()
        metric.calculate(equity=equity_h1_exp)

        assert is_equal(metric.value, 1.01**(365*24))
