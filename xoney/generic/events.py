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

from xoney.generic.trades import Trade


class Event(ABC):
    @abstractmethod
    def handle_trades(self, trades: list[Trade]) -> list[Trade]:
        ...


class OpenTrade(Event):
    _trade: Trade

    def __init__(self, trade: Trade):
        self._trade = trade

    def handle_trades(self, trades: list[Trade]) -> list[Trade]:
        return [*trades, self._trade]


class CloseTrade(Event):
    _trade: Trade

    def __init__(self, trade: Trade):
        self._trade = trade

    def handle_trades(self, trades: list[Trade]) -> list[Trade]:
        trades_copy: list[Trade] = trades
        trades_copy.remove(self._trade)

        return trades_copy


class CloseAllTrades(Event):
    _trade: Trade

    def __init__(self):
        pass

    def handle_trades(self, trades: list[Trade]) -> list[Trade]:
        return []
