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
from abc import ABC, abstractmethod
from xoney.generic.workers import Worker


class VolumeDistributor(ABC):
    _worker: Worker

    def set_worker(self, worker: Worker) -> None:
        self._worker = worker

    @abstractmethod
    def trade_volume(self) -> float:  # pragma: no cover
        ...


class DefaultDistributor(VolumeDistributor):
    def trade_volume(self) -> float:
        free_balance: float = self._worker.free_balance
        opened_trades: float = self._worker.opened_trades
        max_trades: float = self._worker.max_trades

        pending_trades: float = max_trades - opened_trades

        return free_balance / pending_trades