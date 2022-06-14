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

from xoney.generic.trades.levels import TakeProfit
from xoney.generic.enums import TradeSide
from xoney.generic.candlestick import Candle
from xoney.generic.trades.levels import LevelStack
from xoney.generic.trades import Trade


@pytest.fixture
def level():
    tp = TakeProfit(price=30_000.0,
                   trade_part=0.1)
    _trade = Trade(TradeSide.LONG,
                   1,
                   entries=LevelStack(),
                   breakouts=LevelStack([tp]))
    return tp

@pytest.fixture
def candle_below():
    return Candle(20_000, 22_000, 18_000, 21_000)


@pytest.fixture
def candle_above():
    return Candle(35_020, 40_003, 32_400, 33_000)


@pytest.fixture
def candle_at_intersection():
    return Candle(30_000, 31_000, 29_000, 30_000)


class TestLevel:
    def test_quantity(self, level):
        assert level.trade_part == 0.1

    def test_side(self, level):
        assert level.side == TradeSide.LONG

    def test_update(self, level, candle_at_intersection):
        level._trade.update(candle_at_intersection)
        assert level.crossed

    def test_update_above(self, level, candle_above):
        level._trade.update(candle_above)
        assert level.crossed

    def test_update_below(self, level, candle_below):
        level.update(candle_below)
        assert not level.crossed

    def test_flag(self, level, candle_at_intersection, candle_below):
        level._trade.update(candle_at_intersection)
        assert level.crossed
        level._trade.update(candle_below)
        assert level.crossed

class TestEditing:
    @pytest.mark.parametrize("value", [
        42
    ])
    def test_trigger_price(self, level, value):
        level.edit_trigger_price(value)
        assert level.trigger_price == value

@pytest.mark.parametrize("varname, value", [
    ("trade_part", 0.1),
    ("trigger_price", 30_000),
])
def test_immutable(level, varname, value):
    with pytest.raises(AttributeError):
        setattr(level, varname, value*2)
    assert getattr(level, varname) == value


@pytest.fixture
def callback_var():
    return 5

class TestCallbacks:
    def test_on_update(self, level, candle_below, callback_var):

        def callback():
            nonlocal callback_var
            callback_var += 10

        level._on_update_callback = callback
        level._trade.update(candle_below)
        assert callback_var == 5 + 10

    def test_on_breakout(self,
                         level,
                         candle_above,
                         callback_var):

        def callback_break():
            nonlocal callback_var
            callback_var += 3

        level._on_breakout_callback = callback_break

        level._trade.update(candle_above)

        assert callback_var == 5 + 3
