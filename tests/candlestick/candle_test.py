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

import pytest
from xoney.generic.candlestick import Candle
import numpy as np
from copy import deepcopy
from datetime import datetime
from tests import utils

time = datetime(1984, 1, 1, 5)

@pytest.fixture
def candle() -> Candle:
    return Candle(2, 4, 1, 3, volume=100., timestamp=time)


@pytest.fixture
def other_candle() -> Candle:
    return Candle(6, 10, 3, 5)


def test_time(candle):
    assert candle.timestamp == deepcopy(time)


class TestComparisonOperators:
    def test_gt(self, candle):
        assert candle > 0.5
        for expected_false_gt in [1, 1.5, 2, 2.5, 3, 3.5, 4, 4.5]:
            assert not candle > expected_false_gt

    def test_ge(self, candle):
        for expected_ge in [0.5, 1]:
            assert candle >= expected_ge
        for expected_false_gt in [1.5, 2, 2.5, 3, 3.5, 4, 4.5]:
            assert not candle >= expected_false_gt

    def test_eq(self, candle):
        for not_expected in [0.5, 1, 1.5, 2, 2.5, 3, 3.5, 4, 4.5]:
            with pytest.raises(TypeError):
                candle == not_expected

    def test_le(self, candle):
        for expected_le in [4, 4.5]:
            assert candle <= expected_le
        for expected_false_le in [1.5, 2, 2.5, 3, 3.5]:
            assert not candle <= expected_false_le

    def test_lt(self, candle):
        assert candle < 4.5
        for expected_false_lt in [1, 1.5, 2, 2.5, 3, 3.5, 4]:
            assert not candle < expected_false_lt

    def test_eq_candles(self, candle):
        assert candle == Candle(2.0, 4.0, 1.0, 3.0)

    def test_eq_deepcopy(self, candle):
        assert candle == deepcopy(candle)

    def test_lt_candle(self, candle, other_candle):
        assert not candle < other_candle
        assert not candle < Candle(2, 3, 1, 2)
        assert candle < Candle(5, 8, 4.5, 6)
        assert not candle < Candle(5, 8, 4, 6)
        assert not candle < Candle(5, 8, 2, 6)
        assert not candle < Candle(2, 3, 1.5, 2)

    def test_le_candle(self, candle, other_candle):
        assert not candle <= other_candle
        assert not candle <= Candle(2, 3, 1, 2)
        assert candle <= Candle(5, 8, 4.5, 6)
        assert candle <= Candle(5, 8, 4, 6)
        assert not candle <= Candle(5, 8, 2, 6)
        assert not candle <= Candle(2, 3, 1.5, 2)

    def test_ge_candle(self, candle, other_candle):
        assert not candle >= other_candle
        assert not candle >= Candle(2, 3, 0.1, 2.5)
        assert other_candle >= Candle(2, 3, 1, 2.5)
        assert other_candle >= Candle(2, 3, 2, 2)
        assert not candle >= Candle(1, 5, 0.5, 2)
        assert candle >= Candle(0.5, 1, 0.3, 0.6)

    def test_gt_candle(self, candle, other_candle):
        assert not candle > other_candle
        assert not candle > Candle(2, 3, 0.1, 2.5)
        assert not other_candle > Candle(2, 3, 1, 2.5)
        assert not other_candle > Candle(2, 3, 2, 2)
        assert not candle > Candle(1, 5, 0.5, 2)
        assert other_candle > Candle(0.5, 1, 0.3, 0.6)


def assert_contains(contains, not_contains, candle):
    for c in contains:
        assert c in candle
    for nc in not_contains:
        assert nc not in candle


class TestContains:

    def test_int_contains(self, candle):
        contains = [1, 2, 3, 4]
        not_contains = [0, -1, -5, 5, 10, 7]
        assert_contains(contains, not_contains, candle)

    def test_number_contains(self, candle):
        contains = [np.uint(1),
                    np.float64(2),
                    np.intc(3),
                    np.float32(3.5)]
        not_contains = [np.ushort(0),
                        np.single(-1),
                        np.float32(-5),
                        np.float64(5),
                        np.short(10),
                        np.byte(10 ** 9)]
        assert_contains(contains, not_contains, candle)

    def test_float_contains(self, candle):
        contains = [1.5, 2.5, 3.5, 4.0]
        not_contains = [0.1, -1.0, -5.3, 5.0, 10.1, 7.0]
        assert_contains(contains, not_contains, candle)

    def test_candle_contains(self, candle):
        contains = [Candle(2.5, 3.6, 2.1, 2.9),
                    Candle(1.2, 2, 1, 1.5)]
        not_contains = [Candle(1, 5, 1, 2),
                        Candle(2, 3, 0.5, 4)]
        assert_contains(contains, not_contains, candle)


class TestTypeError:
    def test_init_raises(self):
        with pytest.raises(TypeError):
            Candle("not a number",
                   "not a number",
                   "not a number",
                   "not a number")

    def test_init_raises_last_invalid(self):
        with pytest.raises(TypeError):
            Candle(2, 3, 1, "not a number")

    def test_init_with_numpy(self):
        Candle(np.float32(2),
               np.float128(10 ** 8),
               np.uint(4),
               np.int32(3))

    def test_contains_str(self, candle):
        with pytest.raises(TypeError):
            "string" in candle


def test_array():
    for _ in range(50):
        ohlc = utils.random_ohlc()
        candle = Candle(*ohlc)

        equals = candle.as_array() == np.array(ohlc)
        assert equals.all()


class TestOp:
    def test_pos(self, candle):
        pos = +candle
        assert pos == candle

    def test_neg(self, candle):
        neg = -candle
        for neg_price, price in zip(neg.as_array(),
                                    candle.as_array()):
            assert neg_price == -price

    def test_abs(self, candle):
        neg = -candle
        assert abs(neg) == candle
        assert abs(candle) == candle

    def test_add(self, candle):
        result = candle + 1.7
        for result_price, price in zip(result.as_array(),
                                       candle.as_array()):
            assert result_price == price + 1.7

    @pytest.mark.parametrize("value", [
        "string",
        {"string": 123},
        (1, 2, 3, 4)
    ])
    def test_add_typeerror(self, candle, value):
        with pytest.raises(TypeError):
            candle + value

    def test_sub(self, candle):
        result = candle - 1.8
        for result_price, price in zip(result.as_array(),
                                       candle.as_array()):
            assert result_price == price - 1.8

    @pytest.mark.parametrize("value", [
        "string",
        {"string": 123},
        (1, 2, 3, 4)
    ])
    def test_sub_typeerror(self, candle, value):
        with pytest.raises(TypeError):
            candle - value

    def test_mul(self, candle):
        result = candle * 5.3
        for result_price, price in zip(result.as_array(),
                                       candle.as_array()):
            assert result_price == price * 5.3

    @pytest.mark.parametrize("value", [
        "string",
        {"string": 123},
        (1, 2, 3, 4)
    ])
    def test_mul_typeerror(self, candle, value):
        with pytest.raises(TypeError):
            candle * value

    def test_div(self, candle):
        result = candle / 5.5
        for result_price, price in zip(result.as_array(),
                                       candle.as_array()):
            assert result_price == price / 5.5

    @pytest.mark.parametrize("value", [
        "string",
        {"string": 123},
        (1, 2, 3, 4)
    ])
    def test_div_typeerror(self, candle, value):
        with pytest.raises(TypeError):
            candle / value

    def test_add_candle(self, candle, other_candle):
        result = candle + other_candle
        for result_price, expected in zip(
                result.as_array(),
                candle.as_array() + other_candle.as_array()
        ):
            assert result_price == expected

    def test_sub_candle(self, candle, other_candle):
        result = candle - other_candle
        for result_price, expected in zip(
                result.as_array(),
                candle.as_array() - other_candle.as_array()
        ):
            assert result_price == expected

    def test_mul_candle(self, candle, other_candle):
        result = candle * other_candle
        for result_price, expected in zip(
                result.as_array(),
                candle.as_array() * other_candle.as_array()):
            assert result_price == expected

    def test_div_candle(self, candle, other_candle):
        result = candle / other_candle
        assert result.open == (candle.open / other_candle.open)
        assert result.close == (candle.close / other_candle.close)

        assert result.high == (candle.high / other_candle.low)
        assert result.low == (candle.low / other_candle.high)
