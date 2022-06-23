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
from xoney.generic.volume_distribution import (VolumeDistributor,
                                               DefaultDistributor)
from xoney.generic.workers import Worker


class Event(ABC):
    _worker: Worker

    @abstractmethod
    def handle_trades(self, trades: TradeHeap) -> None:
        ...

    def set_worker(self, worker: Worker) -> None:
        self._worker = worker


class OpenTrade(Event):
    _trade: Trade
    _volume_distributor: VolumeDistributor

    def __init__(self,
                 trade: Trade,
                 volume_distributor: VolumeDistributor | None = None):
        self._trade = trade
        if volume_distributor is None:
            volume_distributor = DefaultDistributor()
            volume_distributor.set_worker(self._worker)
        self._volume_distributor = volume_distributor
        self._volume_distributor.set_worker(self._worker)

    def handle_trades(self, trades: TradeHeap) -> None:
        trade_volume: float = self._volume_distributor.trade_volume()
        self._trade.set_potential_volume(trade_volume)

        trades.add(self._trade)


class CloseTrade(Event):
    _trade: Trade

    def __init__(self, trade: Trade):
        self._trade = trade

    def handle_trades(self, trades: TradeHeap) -> None:
        trades.remove(self._trade)
        self._trade.cleanup()


class CloseAllTrades(Event):
    def __init__(self):
        pass

    def handle_trades(self, trades: TradeHeap) -> None:
        trade: Trade

        for trade in trades:
            trade.cleanup()
