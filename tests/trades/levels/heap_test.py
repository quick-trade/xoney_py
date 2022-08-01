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

from xoney.generic.trades.levels import LevelHeap, StopLoss, TakeProfit
from xoney.generic.enums import TradeSide
from xoney.generic.candlestick import Candle

from tests import utils


@pytest.fixture
def empty_heap():
    return LevelHeap()

@pytest.fixture
def stop_loss():
    sl = StopLoss(price=30_000.0,
                  trade_part=0.1)
    utils.connect_trade(sl, TradeSide.LONG, 1)
    return sl

@pytest.fixture
def take_profit():
    tp = TakeProfit(price=40_000.0,
                   trade_part=0.1)
    utils.connect_trade(tp, TradeSide.LONG, 1)
    return tp

@pytest.fixture
def stop_loss_short():
    sl = StopLoss(price=40_000.0,
                  trade_part=0.1)
    utils.connect_trade(sl, TradeSide.SHORT, 1)
    return sl

@pytest.fixture
def take_profit_short():
    tp = TakeProfit(price=30_000.0,
                   trade_part=0.1)
    utils.connect_trade(tp, TradeSide.SHORT, 1)
    return tp

@pytest.fixture
def candle_above_take_profit():
    return Candle(41_000, 42_500, 40_500, 41_500)

@pytest.fixture
def candle_above_stop_loss():
    return Candle(31_000, 32_500, 30_500, 31_500)

@pytest.fixture
def candle_below_take_profit(candle_above_take_profit):
    return candle_above_take_profit - 3_000

@pytest.fixture
def candle_below_stop_loss(candle_above_stop_loss):
    return candle_above_stop_loss - 3_000

@pytest.fixture
def candle_above_stop_loss_short(candle_above_take_profit):
    return candle_above_take_profit

@pytest.fixture
def candle_below_take_profit_short(candle_below_stop_loss):
    return candle_below_stop_loss


candle_above_take_profit_short = Candle(31_000, 32_500, 30_500, 31_500)
candle_below_stop_loss_short = Candle(41_000, 42_500, 40_500, 41_500) - 3_000


@pytest.fixture
def breakouts(stop_loss, take_profit):
    return LevelHeap((stop_loss, take_profit))

@pytest.fixture
def breakouts_short(stop_loss_short, take_profit_short):
    return LevelHeap((stop_loss_short, take_profit_short))


def set_trade_prices(heap, candle):
    for level in heap:
        level._trade._Trade__update_price = candle.close


class TestMagic:
    def test_empty(self, empty_heap):
        assert not len(empty_heap)

    def test_remove(self, breakouts, stop_loss, take_profit):
        breakouts.remove(stop_loss)
        assert stop_loss not in breakouts
        assert take_profit in breakouts

    def test_iteration(self, breakouts, stop_loss, take_profit):
        for level in breakouts:
            assert level in breakouts

    def test_str(self, breakouts):
        assert str(breakouts) == "LevelHeap([<long StopLoss on 30000.0. " \
                                 "Part of trade: 0.1>, <long TakeProfit on " \
                                 "40000.0. Part of trade: 0.1>])"

    def test_repr(self, breakouts):
        assert repr(breakouts) == str(breakouts)


class TestLevelOperations:
    def test_add(self, empty_heap, stop_loss, breakouts):
        empty_heap.add(stop_loss)
        assert stop_loss in empty_heap
        assert stop_loss not in breakouts.crossed
        assert stop_loss in breakouts.pending

    def test_remove(self, breakouts, stop_loss):
        assert stop_loss in breakouts
        breakouts.remove(stop_loss)
        assert stop_loss not in breakouts
        assert stop_loss not in breakouts.crossed
        assert stop_loss not in breakouts.pending

    def test_update_stop_loss_breaking(self,
                                       breakouts,
                                       candle_below_stop_loss,
                                       take_profit,
                                       stop_loss):
        set_trade_prices(breakouts, candle_below_stop_loss)

        breakouts.update(candle_below_stop_loss)
        assert stop_loss in breakouts.crossed
        assert take_profit not in breakouts.crossed
        assert stop_loss not in breakouts.pending
        assert take_profit in breakouts.pending

    def test_update_take_profit_breaking(self,
                                        breakouts,
                                        candle_above_take_profit,
                                        take_profit,
                                        stop_loss):
        set_trade_prices(breakouts, candle_above_take_profit)

        breakouts.update(candle_above_take_profit)
        assert take_profit in breakouts.crossed
        assert stop_loss not in breakouts.crossed
        assert stop_loss in breakouts.pending
        assert take_profit not in breakouts.pending

    def test_update_stop_loss_short_breaking(
            self,
            breakouts_short,
            candle_above_stop_loss_short,
            take_profit_short,
            stop_loss_short):
        set_trade_prices(breakouts_short, candle_above_stop_loss_short)

        breakouts_short.update(candle_above_stop_loss_short)
        assert stop_loss_short in breakouts_short.crossed
        assert take_profit_short not in breakouts_short.crossed
        assert stop_loss_short not in breakouts_short.pending
        assert take_profit_short in breakouts_short.pending

    def test_update_take_profit_short_breaking(
            self,
            breakouts_short,
            candle_below_take_profit_short,
            take_profit_short,
            stop_loss_short):
        set_trade_prices(breakouts_short, candle_below_take_profit_short)

        breakouts_short.update(candle_below_take_profit_short)
        assert take_profit_short in breakouts_short.crossed
        assert stop_loss_short not in breakouts_short.crossed
        assert stop_loss_short in breakouts_short.pending
        assert take_profit_short not in breakouts_short.pending

    @pytest.mark.parametrize("candle", [
        candle_below_stop_loss_short,
        candle_above_take_profit_short
    ])
    def test_update_take_profit_short_normal(
            self,
            breakouts_short,
            candle,
            take_profit_short,
            stop_loss_short):
        set_trade_prices(breakouts_short, candle)

        breakouts_short.update(candle)
        assert take_profit_short not in breakouts_short.crossed
        assert stop_loss_short not in breakouts_short.crossed
        assert stop_loss_short in breakouts_short.pending
        assert take_profit_short in breakouts_short.pending

    def test_update_stop_loss_normal(self,
                                     breakouts,
                                     candle_above_stop_loss,
                                     take_profit,
                                     stop_loss):
        set_trade_prices(breakouts, candle_above_stop_loss)

        breakouts.update(candle_above_stop_loss)
        assert not len(breakouts.crossed)
        assert stop_loss in breakouts.pending
        assert take_profit in breakouts.pending
        assert take_profit not in breakouts.crossed
        assert stop_loss not in breakouts.crossed

    def test_update_take_profit_normal(self,
                                      breakouts,
                                      candle_below_take_profit,
                                      take_profit,
                                      stop_loss):
        set_trade_prices(breakouts, candle_below_take_profit)

        breakouts.update(candle_below_take_profit)
        assert not len(breakouts.crossed)
        assert stop_loss in breakouts.pending
        assert take_profit in breakouts.pending
        assert take_profit not in breakouts.crossed
        assert stop_loss not in breakouts.crossed

    def test_crossed(self, breakouts, stop_loss, take_profit):
        assert not len(breakouts.crossed)


class TestTraceBacks:
    @pytest.mark.parametrize("invalid_level",
                             [
                                 -42,
                                 42,
                                 1.0,
                                 "string",
                                 TradeSide.LONG,
                                 {"other": take_profit}
                             ])
    def test_contains(self, invalid_level, breakouts):
        with pytest.raises(TypeError):
            self.result = invalid_level in breakouts


def test_immutable_levels(breakouts, stop_loss):
    breakouts.get_members().remove(stop_loss)
    assert stop_loss in breakouts


def test_iter(breakouts):
    for level in breakouts:
        level.edit_trigger_price(0)

    for edited_level in breakouts:
        assert edited_level.trigger_price == 0
