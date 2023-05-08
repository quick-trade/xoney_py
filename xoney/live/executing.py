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

from xoney import Exchange, TradingSystem, EquityWorker
from xoney.live.stopping import StopCondition


class Executor(EquityWorker, ABC):
    _exchange: Exchange
    _stop_condition: StopCondition
    _running: bool

    def __init__(self, exchange: Exchange) -> None:
        self._exchange = exchange
        self._running = False

    @abstractmethod
    def _loop(self) -> None:
        ...

    def run(self,
            trading_system: TradingSystem,
            stop_condition: StopCondition) -> None:
        self._trading_system = trading_system
        self._stop_condition = stop_condition
        self._running = True

        self._stop_condition.bind_executor(executor=self)

        while self._running:
            try:
                self._loop()
            except Exception as error:
                self._handle_exception(error=error)

    @abstractmethod
    def _handle_exception(error: Exception) -> None:
        ...

    @property
    def free_balance(self) -> float:
        quote: str = self._current_symbol.quote
        return self.__exchange.fetch_free_balance(currency=quote)

    def stop_trading(self) -> None:
        self._running = False


class DefaultExecutor(Executor):
    def _loop(self) -> None:
        self._stop_condition.check_state()
        # TODO: implement
