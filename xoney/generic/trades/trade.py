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
from xoney.generic.candlestick import Candle
from xoney.generic.enums import TradeSide, TradeStatus
from xoney.system.exceptions import UnexpectedTradeSideError
from xoney.generic.trades.levels import LevelStack


class Trade:
    __entries: LevelStack
    __breakouts: LevelStack
    __side: TradeSide
    __status: TradeStatus
    __potential_volume: float

    @property
    def status(self) -> TradeStatus:
        return self.__status

    @property
    def side(self) -> TradeSide:
        return self.__side

    def __init__(self,
                 side: TradeSide,
                 potential_volume: float,
                 entries: LevelStack,
                 breakouts: LevelStack):
        self.__entries = entries
        self.__breakouts = breakouts
        self.__status = TradeStatus.ACTIVE
        self.__potential_volume = potential_volume

        _validate_trade_side(side=side)
        self.__side = side

        self._bind_levels()

    def _bind_levels(self):
        for level in (*self.__entries, *self.__breakouts):
            level._bind_trade(self)

    def _update_levels(self, candle: Candle) -> None:
        self.__entries.update(candle=candle)
        self.__breakouts.update(candle=candle)

    @property
    def realized_volume(self) -> float:
        entries_vol: float = self.__entries.crossed.quote_volume
        breakouts_vol: float = self.__breakouts.crossed.quote_volume
        return entries_vol - breakouts_vol

    @property
    def potential_volume(self) -> float:
        return self.__potential_volume

    def _update_status(self) -> None:
        ...

    def update(self, candle: Candle) -> None:
        self._update_levels(candle=candle)
        self._update_status()


def _validate_trade_side(side):
    if not isinstance(side, TradeSide):
        raise UnexpectedTradeSideError(side=side)
