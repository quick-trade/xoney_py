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

from xoney.generic.trades import Trade
from xoney.generic.trades.levels import LevelStack
from xoney.generic.enums import TradeSide
from xoney.generic.trades.levels.defaults.entries import *
from tests import utils


@pytest.fixture
def random_candle():
    return utils.random_candle()

@pytest.fixture
def default_trigger_price():
    return 30_000.0

@pytest.fixture
def default_quantity():
    return 0.01

@pytest.fixture
def averaging_entry(default_trigger_price, default_quantity):
    entry = AveragingEntry(default_trigger_price,
                           default_quantity)
    _trade = Trade(TradeSide.LONG,
                   1,
                   entries=LevelStack([entry]),
                   breakouts=LevelStack())
    return entry

@pytest.fixture
def candle_below_entry(default_trigger_price):
    return Candle(default_trigger_price - 2_000,
                  default_trigger_price - 500,
                  default_trigger_price - 3_000,
                  default_trigger_price - 800)

@pytest.fixture
def candle_above_entry(candle_below_entry, default_trigger_price):
    return Candle(default_trigger_price + 100,
                  default_trigger_price + 3_000,
                  default_trigger_price + 50,
                  default_trigger_price + 1_000)

@pytest.fixture
def candle_at_intersection(default_trigger_price):
    return Candle(default_trigger_price - 100,
                  default_trigger_price + 100,
                  default_trigger_price - 500,
                  default_trigger_price - 50)


class TestSimpleEntry:
    def test_start_on_position(self,
                               random_candle,
                               default_trigger_price,
                               default_quantity):
        entry = SimpleEntry(price=default_trigger_price,
                            trade_part=default_quantity)
        _trade = Trade(TradeSide.LONG,
                       1,
                       entries=LevelStack([entry]),
                       breakouts=LevelStack())
        assert entry.check_breaking(random_candle)

class TestAveragingEntry:
    def test_crossed_below(self, averaging_entry, candle_below_entry):
        averaging_entry._trade.update(candle_below_entry)
        assert averaging_entry.crossed

    def test_crossed_intersection(self, averaging_entry,
                                  candle_at_intersection):
        averaging_entry._trade.update(candle_at_intersection)
        assert averaging_entry.crossed

    def test_pending(self, averaging_entry, candle_above_entry):
        averaging_entry._trade.update(candle_above_entry)
        assert not averaging_entry.crossed
