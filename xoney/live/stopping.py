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

from abc import ABC, abstractmethod
from datetime import datetime

from xoney.live import Executor
from xoney.generic.events import CloseAllTrades


class StopCondition(ABC):
    _executor: Executor

    def bind_executor(self, executor: Executor) -> None:
        self._executor = executor

    @abstractmethod
    def should_stop(self) -> bool:
        ...

    def stop(self) -> None:
        self._executor.stop_trading()

    def check_state(self) -> None:
        if self.should_stop():
            self.stop()


class ClosingTradesStopCondition(StopCondition, ABC):
     def stop(self) -> None:
        super().stop()
        close_trades: CloseAllTrades = CloseAllTrades()
        close_trades.set_worker(self._executor)
        close_trades.handle_trades(self._executor._trades)


class StopAtTime(ClosingTradesStopCondition):
    def __init__(self, stopping_time: datetime) -> None:
        self.stopping_time = stopping_time

    def should_stop(self) -> bool:
        return self.stopping_time <= datetime.now()
