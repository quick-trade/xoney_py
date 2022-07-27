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
from __future__ import annotations

import pytest

from xoney.generic.volume_distribution import DefaultDistributor
from xoney.generic.workers import Worker

from xoney.generic.trades import Trade, TradeHeap
from xoney.generic.enums import TradeSide, TradeStatus
from xoney.generic.trades.levels import LevelHeap, SimpleEntry

from xoney.math import is_equal


class TemplateWorker(Worker):
    _free_balance: float
    _opened_trades: int
    _total_balance: float
    _used_balance: float

    def set_free_balance(self, balance: float) -> None:
        self._free_balance = balance

    def set_opened_trades(self, trades: int) -> None:
        self._opened_trades = trades

    def set_total_balance(self, balance: float) -> None:
        self._total_balance = balance

    def set_max_trades(self, trades: int) -> None:
        self.max_trades = trades

    def set_trades(self, trades: list[Trade]):
        self._trades = TradeHeap(trades)

    @property
    def opened_trades(self) -> int:
        return self._opened_trades

    @property
    def free_balance(self) -> float:
        return self._free_balance

    @property
    def used_balance(self) -> float:
        return self._used_balance

    @property
    def total_balance(self) -> float:
        return self._total_balance

    def run(self, *args, **kwargs) -> None:
        pass

    @property
    def equity(self):
        raise NotImplementedError


@pytest.fixture
def worker():
    return TemplateWorker()

@pytest.fixture
def default_distributor(worker):
    distributor = DefaultDistributor()
    distributor.set_worker(worker)
    return distributor

@pytest.fixture
def active_trades():
    trade_long = Trade(
        side=TradeSide.LONG,
        entries=LevelHeap(
            [
                SimpleEntry(
                    trade_part=1,
                    price=30000
                )
            ]
        ),
        breakouts=LevelHeap()
    )
    trade_short = Trade(
            side=TradeSide.SHORT,
            entries=LevelHeap(
                [
                    SimpleEntry(
                        trade_part=1,
                        price=35000
                    )
                ]
            ),
            breakouts=LevelHeap()
        )
    trade_long.__Trade_status = TradeStatus.ACTIVE
    trade_short.__Trade_status = TradeStatus.ACTIVE

    return [trade_long, trade_short]


class TestDefault:
    # free balance, opened trades, max trades,
    def test_volume_10_2_3(self, default_distributor):
        default_distributor._worker.set_total_balance(35)
        default_distributor._worker.set_free_balance(10)
        default_distributor._worker.set_opened_trades(2)
        default_distributor._worker.set_max_trades(3)

        assert is_equal(default_distributor._get_trade_volume(), 10)

    def test_volume_10_2_4(self, default_distributor):
        default_distributor._worker.set_total_balance(23)
        default_distributor._worker.set_free_balance(10)
        default_distributor._worker.set_opened_trades(2)
        default_distributor._worker.set_max_trades(4)

        assert is_equal(default_distributor._get_trade_volume(), 5)

    def test_volume_30_3_10(self, default_distributor):
        default_distributor._worker.set_total_balance(90)
        default_distributor._worker.set_free_balance(70)
        default_distributor._worker.set_opened_trades(3)
        default_distributor._worker.set_max_trades(10)

        assert is_equal(default_distributor._get_trade_volume(), 10)

    def test_trade_binding(self, default_distributor, active_trades):
        default_distributor._worker.set_trades(active_trades)
        default_distributor._worker.set_total_balance(95)
        default_distributor._worker.set_max_trades(5)
        default_distributor._worker.set_opened_trades(2)
        default_distributor._worker.set_free_balance(30)

        default_distributor.set_trade_volume(
            default_distributor._worker._trades[-1]
        )

        assert is_equal(
            default_distributor._worker._trades[-1].potential_volume,
            10
        )
