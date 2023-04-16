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

from xoney.generic.routes import TradingSystem
from xoney.generic.symbol import Symbol
from xoney.generic.trades import TradeHeap
from xoney.generic.equity import Equity


class Worker(ABC):
    _trading_system: TradingSystem

    @abstractmethod
    def run(self,
            *args,
            **kwargs) -> None:
        ...


class EquityWorker(Worker):
    _trades: TradeHeap
    max_trades: int
    commission: float
    _free_balance: float
    _current_symbol: Symbol

    @abstractproperty
    def equity(self) -> Equity:
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

    def _set_symbol(self, symbol: Symbol) -> None:
        ...
