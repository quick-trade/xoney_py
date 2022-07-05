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

from abc import ABC, abstractproperty

from xoney.generic.candlestick import Candle
from xoney.generic.enums import TradeSide


class Level(ABC):
    __trigger_price: float
    __side: TradeSide
    __trade_part: float
    __cross_flag: bool
    __quote_volume: float

    def _on_update_callback(self):
        pass

    def _on_breakout_callback(self):
        pass

    @property
    def trade_part(self) -> float:
        return self.__trade_part

    @property
    def trigger_price(self) -> float:
        return self.__trigger_price

    @property
    def side(self) -> TradeSide:
        return self.__side

    @property
    def crossed(self) -> bool:
        return self.__cross_flag

    @abstractproperty
    def _trade_volume(self) -> float:  # pragma: no cover
        ...

    def __init__(self,
                 price: float,
                 trade_part: float):
        self.__trigger_price = price
        self.__trade_part = trade_part
        self.__cross_flag = False
        self.__quote_volume = 0.0

    def edit_trigger_price(self, price: float) -> None:
        if not self.crossed:
            self.__trigger_price = price

    def check_breaking(self, candle: Candle) -> bool:  # pragma: no cover
        return self.__trigger_price in candle

    def update(self, candle: Candle) -> None:
        self._update_volume()
        self._on_update_callback()
        if not self.crossed and self.check_breaking(candle):
            self.__cross_flag = True
            self._on_breakout_callback()

    def _update_volume(self) -> None:
        if not self.crossed:
            self.__quote_volume = self._trade_volume * self.trade_part

    def _bind_trade(self, trade) -> None:
        self._trade = trade
        self.__side = trade.side

    @property
    def quote_volume(self) -> float:
        return self.__quote_volume

    @property
    def base_volume(self) -> float:
        return self.__quote_volume / self.__trigger_price

    def __eq__(self, other) -> bool:
        if not isinstance(other, Level):
            raise TypeError("To compare object with <Level>, "
                            "this object must be of type <Level>")
        same_side: bool = other.__side == self.__side
        same_price: bool = other.__trigger_price == self.__trigger_price
        same_quantity: bool = other.__trade_part == self.__trade_part
        same_status: bool = other.crossed == self.crossed
        return same_status and same_side and same_quantity and same_price

    def __repr__(self) -> str:
        return f"<{self.__side.value} {self.__class__.__name__} on " \
               f"{self.__trigger_price}. Part of trade: {self.trade_part}>"
