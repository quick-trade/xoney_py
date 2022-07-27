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

from xoney.generic.workers import Worker
from xoney.generic.trades import Trade


class VolumeDistributor(ABC):
    _worker: Worker

    def set_worker(self, worker: Worker) -> None:
        self._worker = worker

    @abstractmethod
    def set_trade_volume(self, trade: Trade) -> None:  # pragma: no cover
        ...


class DefaultDistributor(VolumeDistributor):
    def _get_trade_volume(self) -> float:
        free_balance: float = self._worker.free_balance
        opened_trades: float = self._worker.opened_trades
        max_trades: float = self._worker.max_trades

        pending_trades: float = max_trades - opened_trades

        trade_volume: float = free_balance / pending_trades
        return trade_volume

    def set_trade_volume(self, trade: Trade) -> None:
        trade_volume: float = self._get_trade_volume()
        trade.set_potential_volume(trade_volume)
