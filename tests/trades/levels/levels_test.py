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

from xoney.generic.trades.levels import TakeProfit, Level
from xoney.generic.enums import TradeSide
from xoney.generic.candlestick import Candle
from xoney.generic.trades.levels import LevelStack
from xoney.generic.trades import Trade


@pytest.fixture
def level():
    return Level(30_000,
                 0.99)

@pytest.fixture
def take_profit():
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


class TestTakeProfit:
    def test_quantity(self, take_profit):
        assert take_profit.trade_part == 0.1

    def test_side(self, take_profit):
        assert take_profit.side == TradeSide.LONG

    def test_update(self, take_profit, candle_at_intersection):
        take_profit._trade.update(candle_at_intersection)
        assert take_profit.crossed

    def test_update_above(self, take_profit, candle_above):
        take_profit._trade.update(candle_above)
        assert take_profit.crossed

    def test_update_below(self, take_profit, candle_below):
        take_profit.update(candle_below)
        assert not take_profit.crossed

    def test_flag(self, take_profit, candle_at_intersection, candle_below):
        take_profit._trade.update(candle_at_intersection)
        assert take_profit.crossed
        take_profit._trade.update(candle_below)
        assert take_profit.crossed

class TestEditing:
    @pytest.mark.parametrize("value", [
        42
    ])
    def test_trigger_price(self, take_profit, value):
        take_profit.edit_trigger_price(value)
        assert take_profit.trigger_price == value

@pytest.mark.parametrize("varname, value", [
    ("trade_part", 0.1),
    ("trigger_price", 30_000),
])
def test_immutable(take_profit, varname, value):
    with pytest.raises(AttributeError):
        setattr(take_profit, varname, value * 2)
    assert getattr(take_profit, varname) == value


@pytest.fixture
def callback_var():
    return 5

class TestCallbacks:
    def test_on_update(self, take_profit, candle_below, callback_var):

        def callback():
            nonlocal callback_var
            callback_var += 10

        take_profit._on_update_callback = callback
        take_profit._trade.update(candle_below)
        assert callback_var == 5 + 10

    def test_on_breakout(self,
                         take_profit,
                         candle_above,
                         callback_var):

        def callback_break():
            nonlocal callback_var
            callback_var += 3

        take_profit._on_breakout_callback = callback_break

        take_profit._trade.update(candle_above)

        assert callback_var == 5 + 3
