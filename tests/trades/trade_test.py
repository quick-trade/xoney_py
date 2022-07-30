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

from xoney.math import is_equal


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
                 entries=LevelHeap([entry, averaging_entry]),
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
        expected_filled_after = trade.potential_volume * entry.trade_part

        assert trade.filled_volume == 0
        assert trade.status == TradeStatus.PENDING

        trade.update(candle_below_entry)

        assert trade.status == TradeStatus.ACTIVE
        assert trade.filled_volume == expected_filled_after

    def test_averaging_entry(self,
                             trade,
                             candle_below_averaging_entry):
        after_entry = 50 * 0.6
        avg_entry_only = 50 * 0.4

        after_avg_entry = after_entry + avg_entry_only

        assert trade.status == TradeStatus.PENDING

        trade.update(candle_below_averaging_entry)

        assert trade.status == TradeStatus.ACTIVE
        assert trade.filled_volume == after_avg_entry

    def test_stop_loss(self, trade, candle_below_stop_loss):
        filled_before_breakout = 50
        filled_after_breakout = filled_before_breakout * (1 - 0.1)
        # filled_volume -= filled_volume * stop_loss.trade_part

        assert trade.status == TradeStatus.PENDING

        trade.update(candle_below_stop_loss)

        assert trade.status == TradeStatus.ACTIVE
        # stop-loss have not 100% trade_part
        assert trade.filled_volume == filled_after_breakout

    def test_entry_take_profit(self,
                              trade,
                              candle_below_entry,
                              candle_above_take_profit):
        filled_after_entry = 50 * 0.6
        filled_after_breakout = filled_after_entry * (1 - 0.7)
        # filled_volume -= filled_volume * take_profit.trade_part

        trade.update(candle_below_entry)
        trade.update(candle_above_take_profit)

        assert is_equal(trade.filled_volume, filled_after_breakout)

    def test_entry_take_profit_averaging_entry_stop_loss(
            self,
            trade,
            candle_below_stop_loss,
            candle_above_take_profit,
            candle_below_entry,
            candle_below_averaging_entry
    ):
        filled_after_entry = 50 * 0.6
        filled_after_tp = filled_after_entry * (1 - 0.7)
        filled_after_avg = filled_after_tp + 50 * 0.4
        filled_after_sl = filled_after_avg * (1 - 0.1)

        trade.update(candle_below_entry)
        trade.update(candle_above_take_profit)
        trade.update(candle_below_averaging_entry)
        assert trade.filled_volume == filled_after_avg

        trade.update(candle_below_stop_loss)
        assert trade.filled_volume == filled_after_sl

    def test_entry_tp2(self,
                       trade,
                       candle_above_take_profit_2,
                       candle_below_entry):
        assert trade.status == TradeStatus.PENDING
        trade.update(candle_below_entry)

        assert trade.status == TradeStatus.ACTIVE
        trade.update(candle_above_take_profit_2)

        assert trade.filled_volume == 0
        assert trade.status == TradeStatus.CLOSED

        trade.update(candle_above_take_profit_2)

        assert trade.filled_volume == 0
        assert trade.status == TradeStatus.CLOSED

    def test_entry_cleanup(self,
                           trade,
                           entry,
                           candle_below_entry):
        trade.update(candle_below_entry)
        trade.cleanup()
        assert trade.filled_volume == 0
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


class TestProfit:
    def test_entry_only(self, trade, candle_below_entry, entry):
        price = candle_below_entry.close

        trade.update(candle_below_entry)

        active_volume = entry.quote_volume * (price / entry.trigger_price)
        expected_profit = active_volume - entry.quote_volume

        assert is_equal(trade.profit, expected_profit)

    def test_stop_loss(self, trade, candle_below_stop_loss, stop_loss):
        price = candle_below_stop_loss.close

        trade.update(candle_below_stop_loss)

        expected_profit = (1-(1-32.5/35)*0.6) * (1-(1-30/32.5)*(0.6+0.4)) * (1-(1-price/30000)*0.1*(0.6+0.4)) * trade.potential_volume - trade.potential_volume

        assert is_equal(trade.profit, expected_profit)

    def test_entry_take_profit(self,
                              trade,
                              candle_below_entry,
                              candle_above_take_profit):
        price = candle_above_take_profit.close

        trade.update(candle_below_entry)
        trade.update(candle_above_take_profit)

        expected_profit = (1 - (1 - 40 / 35) * 0.6) * (1-(1-price/40000)*(0.6-0.6*0.7)) * trade.potential_volume - trade.potential_volume

        assert is_equal(trade.profit, expected_profit)

    def test_entry_take_profit_averaging_entry_stop_loss(
            self,
            trade,
            candle_below_stop_loss,
            candle_above_take_profit,
            candle_below_entry,
            candle_below_averaging_entry
    ):
        price = candle_above_take_profit.close

        trade.update(candle_below_entry)
        trade.update(candle_above_take_profit)
        trade.update(candle_below_averaging_entry)
        trade.update(candle_below_stop_loss)

        expected_profit = (1 - (1 - 40 / 35) * 0.6) * (1-(1-32.5/40)*(0.6-0.6*0.7)) * (1-(1-30/32.5)*(0.6*(1-0.7)+0.4)) * (1-(1-price/30000)*(0.6*(1-0.7)+0.4)*(1-0.1)) * trade.potential_volume - trade.potential_volume

        assert is_equal(trade.profit, expected_profit)

    def test_entry_take_profit_averaging_entry_tp2(
            self,
            trade,
            candle_above_take_profit_2,
            candle_above_take_profit,
            candle_below_entry,
            candle_below_averaging_entry
    ):
        trade.update(candle_below_entry)
        trade.update(candle_above_take_profit)
        trade.update(candle_below_averaging_entry)
        trade.update(candle_above_take_profit_2)

        expected_profit = (1 - (1 - 40 / 35) * 0.6) * (1-(1-32.5/40)*(0.6*(1-0.7))) * (1-(1-45/32.5)*(0.6*(1-0.7)+0.4)) * trade.potential_volume - trade.potential_volume

        assert is_equal(trade.profit, expected_profit)


class TestOperations:
    def test_eq_true(self, trade):
        trade_copy = copy.deepcopy(trade)
        assert trade == trade_copy

    def test_eq_false(self, trade):
        trade_copy = copy.deepcopy(trade)
        trade_copy.update(Candle(1, 1, 1, 1))  # Different status.
        assert trade != trade_copy

    @pytest.mark.parametrize("not_a_trade",
                             [12345,
                              "string",
                              {"dict": 0},
                              ["list"]])
    def test_eq_typeerror(self, trade, not_a_trade):
        with pytest.raises(TypeError):
            trade == not_a_trade


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
