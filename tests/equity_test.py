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
import pytest

from xoney.generic.equity import Equity
from xoney.generic.timeframes import HOUR_1


@pytest.fixture
def equity_1d():
    return Equity([1, 2, 3, 4, 5, 6, 7, 8, 9, 10])


@pytest.fixture
def equity_1d_2():
    return Equity([2, 3, 4, 5, 6, 7, 8, 9, 10, 11])


def test_append(equity_1d):
    expected = Equity([*equity_1d.as_array(), 11, 12],
                      timeframe=equity_1d.timeframe)
    equity_1d.append(11)
    equity_1d.append(12)
    assert expected == equity_1d


def test_update(equity_1d):
    expected = Equity([*equity_1d.as_array()[:-1], 13],
                      timeframe=equity_1d.timeframe)
    equity_1d.update(11)
    equity_1d.update(13)
    assert expected == equity_1d


def test_log(equity_1d):
    expected = Equity(np.log(equity_1d.as_array()),
                      timeframe=equity_1d.timeframe)
    assert expected == equity_1d.log()
    assert expected != equity_1d


def test_len(equity_1d):
    assert len(equity_1d) == len(equity_1d.as_array())


def test_eq_tf(equity_1d):
    other = Equity(equity_1d.as_array(),
                   timeframe=HOUR_1,
                   timestamp=equity_1d._timestamp)
    assert other != equity_1d


def test_iter(equity_1d):
    for i, val in enumerate(equity_1d):
        assert val == equity_1d.as_array()[i] == equity_1d[i]


@pytest.mark.parametrize("op",
                         [lambda x, y: x * y,
                          lambda x, y: x / y,
                          lambda x, y: x + y,
                          lambda x, y: x - y])
def test_op(equity_1d, op, equity_1d_2):
    assert op(equity_1d, equity_1d_2) == Equity(op(equity_1d.as_array(),
                                                   equity_1d_2.as_array()))


@pytest.mark.parametrize("op",
                         [lambda x, y: x * y,
                          lambda x, y: x / y,
                          lambda x, y: x + y,
                          lambda x, y: x - y])
@pytest.mark.parametrize("val",
                         [2.5, 6, 1, 2])
def test_op_float(op, equity_1d, val):
    assert op(equity_1d, val) == Equity(op(equity_1d.as_array(), val))
