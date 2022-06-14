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
import numpy as np
import pytest

from .data_array import tohlcv
from xoney.generic.candlestick import Chart
from xoney.system.exceptions import IncorrectChartLength

@pytest.fixture
def chart():
    t, o, h, l, c, v = tohlcv.T
    return Chart(open=o,
                 high=h,
                 low=l,
                 close=c,
                 timestamp=t,
                 volume=v)


class TestOperations:
    def test_div_int(self, chart):
        result = chart / 3
        assert all(result.open == chart.open / 3)
        assert all(result.high == chart.high / 3)
        assert all(result.low == chart.low / 3)
        assert all(result.close == chart.close / 3)

    def test_div_chart(self, chart):
        result = chart / chart
        assert all(result.open == np.ones(chart.open.shape))
        assert all(result.high == chart.high / chart.low)
        assert all(result.low == chart.low / chart.high)
        assert all(result.close == np.ones(chart.close.shape))


def test_empty():
    empty_chart = Chart()
    assert not empty_chart.open.shape[0]
    assert not empty_chart.high.shape[0]
    assert not empty_chart.low.shape[0]
    assert not empty_chart.close.shape[0]

def test_incorrect_lens():
    with pytest.raises(IncorrectChartLength):
        chart = Chart([1.], [1., 2., 3.], [3.], [4.3])