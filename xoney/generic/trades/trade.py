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

from xoney.generic.candlestick import Candle
from xoney.generic.enums import TradeSide, TradeStatus
from xoney.system.exceptions import UnexpectedTradeSideError
from xoney.generic.trades.levels import LevelHeap

from xoney import math


class Trade:
    __entries: LevelHeap
    __breakouts: LevelHeap
    __side: TradeSide
    __status: TradeStatus
    __potential_volume: float
    __opened: bool
    __update_price: float

    @property
    def status(self) -> TradeStatus:
        return self.__status

    @property
    def side(self) -> TradeSide:
        return self.__side

    @property
    def _levels(self) -> LevelHeap:
        return LevelHeap((*self.__entries, *self.__breakouts))

    def __init__(self,
                 side: TradeSide,
                 entries: LevelHeap,
                 breakouts: LevelHeap,
                 potential_volume: float | None = None):
        self.__entries = entries
        self.__breakouts = breakouts
        self.__status = TradeStatus.ACTIVE
        self.__potential_volume = potential_volume

        self.__opened = False

        _validate_trade_side(side=side)
        self.__side = side

        self._bind_levels()

    def __eq__(self, other) -> bool:
        if not isinstance(other, Trade):
            raise TypeError("To compare object with <Trade>, "
                            "this object must be of type <Trade>")
        same_side: bool = self.__side == other.__side
        same_status: bool = self.__status == other.__status
        same_volume: bool = self.__potential_volume == other.__potential_volume
        same_breakouts: bool = self.__breakouts == other.__breakouts
        same_entries: bool = self.__entries == other.__entries

        same_levels: bool = same_entries and same_breakouts

        return same_volume and same_levels and same_side and same_status

    def set_potential_volume(self, potential_volume: float) -> None:
        if self.__potential_volume is None:
            self.__potential_volume = potential_volume

    def _bind_levels(self) -> None:
        for level in (*self.__entries, *self.__breakouts):
            level._bind_trade(self)

    def _update_levels(self, candle: Candle) -> None:
        self.__entries.update(candle=candle)
        self.__breakouts.update(candle=candle)

    @property
    def filled_volume(self) -> float:
        entries_vol: float = self.__entries.crossed.quote_volume
        breakouts_vol: float = self.__breakouts.crossed.quote_volume
        return entries_vol - breakouts_vol

    @property
    def filled_volume_base(self) -> float:
        entries_vol: float = self.__entries.crossed.base_volume
        breakouts_vol: float = self.__breakouts.crossed.base_volume
        return entries_vol - breakouts_vol

    @property
    def profit(self) -> float:
        # TODO: debug
        active_volume: float = self.filled_volume_base * self.__update_price
        volume_multiplier: float = math.divide(active_volume,
                                              self.filled_volume)

        if self.side == TradeSide.SHORT:
            volume_multiplier = math.multiply_diff(volume_multiplier, -1)

        result_volume: float = volume_multiplier * self.filled_volume
        return result_volume - self.filled_volume

    @property
    def potential_volume(self) -> float:
        return self.__potential_volume

    def _update_status(self) -> None:
        if not self.__opened and not math.is_zero(self.filled_volume):
            self.__opened = True
        elif math.is_zero(self.filled_volume):
            self.__status = TradeStatus.CLOSED

    def update(self, candle: Candle) -> None:
        self.__update_price = candle.close
        self._update_levels(candle=candle)
        self._update_status()

    def _cleanup_callback(self):
        pass

    def cleanup(self) -> None:
        """
        This method closes all opened positions
        and updates the status of the trade.

        """
        self._cleanup_callback()

        self.__entries = self.__entries.__class__()
        self.__breakouts = self.__breakouts.__class__()
        # To zero the filled volume, the level
        # heaps are set empty, but of the same type.

        self._update_status()


def _validate_trade_side(side) -> None:
    if not isinstance(side, TradeSide):
        raise UnexpectedTradeSideError(side=side)
