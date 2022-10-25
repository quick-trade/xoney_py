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

from xoney.generic.trades import TradeHeap

from xoney.generic.trades.levels.defaults.breakouts import *
from xoney.generic.candlestick import Candle
from xoney.generic.trades import Trade
from xoney.generic.enums import TradeSide, TradeStatus
from xoney.generic.trades.levels import (
    LevelHeap,
    SimpleEntry,
    AveragingEntry
)

from xoney.math import is_equal, is_zero


@pytest.fixture
def stop_loss():
    return StopLoss(30_000,
                    0.1)


@pytest.fixture
def entry():
    return SimpleEntry(35_000,
                       0.6)


@pytest.fixture
def averaging_entry():
    return AveragingEntry(32_500,
                          0.4)


@pytest.fixture
def take_profit():
    return TakeProfit(40_000,
                     0.7)


@pytest.fixture
def take_profit2():
    return TakeProfit(45_000,
                     1.0)

@pytest.fixture
def breakouts(stop_loss, take_profit, take_profit2):
    return LevelHeap([stop_loss, take_profit, take_profit2])


@pytest.fixture
def entries(entry, averaging_entry):
    return LevelHeap([entry, averaging_entry])


@pytest.fixture
def breakouts_2(stop_loss, take_profit, take_profit2):
    return LevelHeap([stop_loss, take_profit2])


@pytest.fixture
def entries_2(entry, averaging_entry):
    return LevelHeap([entry])


@pytest.fixture
def trade(entries, breakouts):
    return Trade(side=TradeSide.LONG,
                 entries=entries,
                 breakouts=breakouts,
                 potential_volume=50.0)

@pytest.fixture
def trade_2(entries_2, breakouts_2):
    return Trade(side=TradeSide.LONG,
                 entries=entries_2,
                 breakouts=breakouts_2,
                 potential_volume=150.0)


@pytest.fixture
def candle_below_entry():
    return Candle(34_500, 34_600, 34_200, 34_300)


@pytest.fixture
def candle_below_averaging_entry(candle_below_entry):
    return candle_below_entry - 2_500


@pytest.fixture
def candle_below_stop_loss(candle_below_averaging_entry):
    return candle_below_averaging_entry - 2_500


@pytest.fixture
def trade_heap(trade, trade_2):
    return TradeHeap([trade, trade_2])


class TestPotentialVolume:
    def test_at_init(self, trade_heap, trade, trade_2):
        expected = trade_2.potential_volume + trade.potential_volume
        assert is_equal(trade_heap.potential_volume, expected)

    def test_at_init_active(self, trade_heap, trade, trade_2):
        expected = trade_2.potential_volume + trade.potential_volume
        assert is_equal(trade_heap.active.potential_volume, expected)

    def test_zero(self, trade_heap, trade, trade_2):
        assert is_zero(trade_heap.closed.potential_volume)
