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


from xoney.generic.trades import Trade
from xoney.generic.heap import Heap
from xoney.generic.candlestick import Candle
from xoney.generic.enums import TradeStatus


class TradeHeap(Heap):
    def update(self, candle: Candle) -> None:
        trade: Trade
        for trade in self._members:
            trade.update(candle=candle)
            if trade.status == TradeStatus.CLOSED:
                self.remove(member=trade)

    @property
    def filled_volume(self) -> float:
        trade: Trade

        return sum(trade.filled_volume
                   for trade in self._members)

    @property
    def potential_volume(self) -> float:
        trade: Trade

        return sum(trade.potential_volume
                   for trade in self._members)
