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

from xoney.generic.trades.levels.defaults.breakouts import *
from xoney.generic.candlestick import Candle
from xoney.generic.trades import Trade
from xoney.generic.enums import TradeSide, TradeStatus
from xoney.system.exceptions import UnexpectedTradeSideError
from xoney.generic.trades.levels import (
    LevelHeap,
    SimpleEntry,
    AveragingEntry
)

from xoney.math import is_zero


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
def trade(stop_loss, entry, averaging_entry, take_profit, take_profit2):
    return Trade(side=TradeSide.LONG,
                 entries=LevelHeap([averaging_entry, entry]),
                 breakouts=LevelHeap([stop_loss, take_profit, take_profit2]),
                 potential_volume=50.0)


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
def candle_above_take_profit(candle_below_entry):
    return candle_below_entry + 5_500

@pytest.fixture
def candle_above_take_profit_2(candle_above_take_profit):
    return candle_above_take_profit + 5_000


class TestLogic:
    def test_entry_only(self, trade, candle_below_entry, entry):
        expected_realized_after = trade.potential_volume * entry.trade_part

        assert trade.realized_volume == 0
        assert trade.status == TradeStatus.PENDING

        trade.update(candle_below_entry)

        assert trade.status == TradeStatus.ACTIVE
        assert (trade.realized_volume == expected_realized_after)

    def test_averaging_entry(self,
                             trade,
                             candle_below_averaging_entry):
        after_entry = 50 * 0.6
        avg_entry_only = 50 * 0.4

        after_avg_entry = after_entry + avg_entry_only

        assert trade.status == TradeStatus.PENDING

        trade.update(candle_below_averaging_entry)

        assert trade.status == TradeStatus.ACTIVE
        assert (trade.realized_volume == after_avg_entry)

    def test_stop_loss(self, trade, candle_below_stop_loss):
        realized_before_breakout = 50
        realized_after_breakout = realized_before_breakout * (1 - 0.1)
        # realized_volume -= realized_volume * stop_loss.trade_part

        assert trade.status == TradeStatus.PENDING

        trade.update(candle_below_stop_loss)

        assert trade.status == TradeStatus.ACTIVE
        # stop-loss have not 100% trade_part
        assert trade.realized_volume == realized_after_breakout

    def test_entry_take_profit(self,
                              trade,
                              candle_below_entry,
                              candle_above_take_profit):
        realized_after_entry = 50 * 0.6
        realized_after_breakout = realized_after_entry * (1 - 0.7)
        # realized_volume -= realized_volume * take_profit.trade_part

        trade.update(candle_below_entry)
        trade.update(candle_above_take_profit)

        assert is_zero(trade.realized_volume - realized_after_breakout)

    def test_entry_take_profit_averaging_entry_stop_loss(
            self,
            trade,
            candle_below_stop_loss,
            candle_above_take_profit,
            candle_below_entry,
            candle_below_averaging_entry
    ):
        realized_after_entry = 50 * 0.6
        realized_after_tp = realized_after_entry * (1 - 0.7)
        realized_after_avg = realized_after_tp + 50 * 0.4
        realized_after_sl = realized_after_avg * (1 - 0.1)

        trade.update(candle_below_entry)
        trade.update(candle_above_take_profit)
        trade.update(candle_below_averaging_entry)
        assert trade.realized_volume == realized_after_avg

        trade.update(candle_below_stop_loss)
        assert trade.realized_volume == realized_after_sl

    def test_entry_tp2(self,
                       trade,
                       candle_above_take_profit_2,
                       candle_below_entry):
        assert trade.status == TradeStatus.PENDING
        trade.update(candle_below_entry)

        assert trade.status == TradeStatus.ACTIVE
        trade.update(candle_above_take_profit_2)

        assert trade.realized_volume == 0
        assert trade.status == TradeStatus.CLOSED

        trade.update(candle_above_take_profit_2)

        assert trade.realized_volume == 0
        assert trade.status == TradeStatus.CLOSED

    def test_entry_cleanup(self,
                           trade,
                           entry,
                           candle_below_entry):
        trade.update(candle_below_entry)
        trade.cleanup()
        assert trade.realized_volume == 0
        assert trade.status == TradeStatus.CLOSED

    def test_set_potential_volume(self):
        trade = Trade(TradeSide.LONG,
                      LevelHeap(),
                      LevelHeap(),
                      potential_volume=None)
        trade.set_potential_volume(5.5)

        assert trade.potential_volume == 5.5

    def test_set_potential_volume_doesnt_edit(self):
        trade = Trade(TradeSide.LONG,
                      LevelHeap(),
                      LevelHeap(),
                      potential_volume=1)
        trade.set_potential_volume(5.5)

        assert trade.potential_volume == 1


@pytest.mark.parametrize("side",
                         ["long",  # string
                          123,
                          {"DICT": "DICT"}])
def test_unexpected_trade_side(side):
    with pytest.raises(UnexpectedTradeSideError):
        trade = Trade(side=side,
                      potential_volume=10,
                      entries=LevelHeap(),
                      breakouts=LevelHeap())
