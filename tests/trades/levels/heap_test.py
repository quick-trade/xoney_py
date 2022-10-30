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
import copy

import pytest

from xoney.generic.trades import Trade, TradeHeap
from xoney.generic.trades.levels import StopLoss, TakeProfit, LevelHeap, SimpleEntry
from xoney.generic.enums import TradeSide
from xoney.generic.candlestick import Candle
from xoney.math import is_equal


@pytest.fixture
def _entries():
    return LevelHeap([SimpleEntry(35_000, 0.6)])


@pytest.fixture
def _breakouts():
    return LevelHeap([StopLoss(40_000, 0.7), TakeProfit(30_000, 0.8)])


@pytest.fixture
def trade_short(_entries, _breakouts):
    return Trade(TradeSide.SHORT,
                 entries=_entries,
                 breakouts=_breakouts,
                 potential_volume=100)


@pytest.fixture
def candle_below_entry(_entries):
    entry = _entries[0]
    price = entry.trigger_price
    return Candle(price+5, price+10, price-5, price+2)


@pytest.fixture
def candle_above_sl(_breakouts):
    sl = _breakouts[0]
    price = sl.trigger_price
    return Candle(price+5, price+10, price-5, price+2)


def test_short_entry(trade_short,
                     candle_below_entry):
    last_price = candle_below_entry.close
    entr = trade_short._Trade__entries[0].trigger_price
    entr_vol = trade_short._Trade__entries[0].trade_part

    expected = (entr-last_price)*entr_vol / entr * trade_short.potential_volume

    trade_short.update(candle_below_entry)

    assert is_equal(expected, trade_short.profit)


class TestTraceBacks:
    @pytest.mark.parametrize("invalid_level",
                             [
                                 -42,
                                 42,
                                 1.0,
                                 "string",
                                 TradeSide.LONG,
                                 {"other": 123}
                             ])
    def test_contains(self, invalid_level, _breakouts):
        with pytest.raises(TypeError):
            invalid_level in _breakouts


def test_immutable_levels(trade_short):
    _breakouts = trade_short._Trade__breakouts
    stop_loss = _breakouts.get_members()[0]
    assert stop_loss in _breakouts


def test_iter(_breakouts):
    for level in _breakouts:
        level.edit_trigger_price(0)

    for edited_level in _breakouts:
        assert edited_level.trigger_price == 0


@pytest.mark.parametrize("obj",
                         [123,
                          "123",
                          123.123123,
                          {"dict": "key"},
                          {123, 12, 1},
                          [123, 123, 123]])
def test_eq_type_false(_breakouts, obj):
    with pytest.raises(TypeError):
        _breakouts == 123
