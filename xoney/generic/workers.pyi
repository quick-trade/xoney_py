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

from abc import abstractproperty, abstractmethod, ABC

from xoney.generic.trades import TradeHeap
from xoney.strategy import Strategy


class Worker(ABC):
    _trades: TradeHeap
    _strategies: list[Strategy]
    max_trades: int

    @abstractmethod
    def run(self,
            *args,
            **kwargs) -> None:
        ...

    @abstractproperty
    def equity(self) -> list[float | int]:
        ...

    @property
    def opened_trades(self) -> int:
        ...

    @property
    def total_balance(self) -> float:
        ...

    @property
    def used_balance(self) -> float:
        ...

    @abstractproperty
    def free_balance(self) -> float:
        ...

    @property
    def filled_balance(self) -> float:
        ...
