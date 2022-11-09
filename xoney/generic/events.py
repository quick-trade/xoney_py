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
from __future__ import annotations

from abc import ABC, abstractmethod

from xoney.generic.trades import Trade, TradeHeap
from xoney.generic.trades.levels import Level
from xoney.generic.volume_distribution import (VolumeDistributor,
                                               DefaultDistributor)
from xoney.generic.workers import Worker


class Event(ABC):
    _worker: Worker

    @abstractmethod
    def handle_trades(self,
                      trades: TradeHeap) -> None:  # pragma: no cover
        ...

    def set_worker(self, worker: Worker) -> None:
        self._worker = worker


class OpenTrade(Event):
    _trade: Trade
    _volume_distributor: VolumeDistributor

    def __init__(self,
                 trade: Trade,
                 volume_distributor: VolumeDistributor | None = None):
        if volume_distributor is None:
            volume_distributor = DefaultDistributor()

        self._volume_distributor = volume_distributor
        self._trade = trade

    def set_worker(self, worker: Worker) -> None:
        super().set_worker(worker=worker)
        self._volume_distributor.set_worker(worker)
        self.__set_trade_commission()

    def __set_trade_commission(self):
        trade_level: Level
        for trade_level in self._trade._levels:
            @trade_level.add_on_breakout_callback
            def decrease_filled_volume(level):
                commission: float = self._worker.commission
                commission_size: float = level.quote_volume * commission
                self._worker._free_balance -= commission_size

    def handle_trades(self, trades: TradeHeap) -> None:
        if self._worker.max_trades > self._worker.opened_trades:
            self._volume_distributor.set_trade_volume(self._trade)

            trades.add(self._trade)
            self._worker._free_balance -= self._trade.potential_volume


class CloseTrade(Event):
    _trade: Trade

    def __init__(self, trade: Trade):
        self._trade = trade

    def handle_trades(self, trades: TradeHeap) -> None:
        trade_value: float = self._trade.potential_volume + self._trade.profit
        self._worker._free_balance += trade_value
        self._trade.cleanup()


class CloseAllTrades(Event):
    def __init__(self):
        pass

    def handle_trades(self, trades: TradeHeap) -> None:
        trade: Trade
        close_trade: CloseTrade

        for trade in trades:
            close_trade = CloseTrade(trade=trade)
            close_trade.set_worker(self._worker)
            close_trade.handle_trades(trades=trades)
