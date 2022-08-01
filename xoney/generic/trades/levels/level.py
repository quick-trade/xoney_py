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


class Level(ABC):
    def _on_update_callback(self):
        pass

    def _on_breakout_callback(self):
        pass

    @property
    def trade_part(self):
        return self.__trade_part

    @property
    def trigger_price(self):
        return self.__trigger_price

    @property
    def side(self):
        return self.__side

    @property
    def crossed(self):
        return self.__cross_flag

    @abstractproperty
    def _trade_volume(self):  # pragma: no cover
        ...

    def __init__(self,
                 price,
                 trade_part):
        self.__trigger_price = price
        self.__trade_part = trade_part
        self.__cross_flag = False
        self.__quote_volume = 0.0

    def edit_trigger_price(self, price: float):
        if not self.crossed:
            self.__trigger_price = price

    def check_breaking(self, candle):  # pragma: no cover
        return self.__trigger_price in candle

    def update(self, candle):
        self._update_volume()
        self._on_update_callback()
        if not self.crossed and self.check_breaking(candle):
            self.__cross_flag = True
            self._on_breakout_callback()

    def _update_volume(self):
        if not self.crossed:
            self.__quote_volume = self._trade_volume * self.trade_part

    def _bind_trade(self, trade):
        self._trade = trade
        self.__side = trade.side

    @property
    def quote_volume(self):
        return self.__quote_volume

    @property
    def base_volume(self):
        return self.__quote_volume / self.__trigger_price

    def __eq__(self, other):
        if not isinstance(other, Level):
            raise TypeError("To compare object with <Level>, "
                            "this object must be of type <Level>")
        same_side = other.__side == self.__side
        same_price = other.__trigger_price == self.__trigger_price
        same_quantity = other.__trade_part == self.__trade_part
        same_status = other.crossed == self.crossed
        return same_status and same_side and same_quantity and same_price

    def __repr__(self):
        return f"<{self.__side.value} {self.__class__.__name__} on " \
               f"{self.__trigger_price}. Part of trade: {self.trade_part}>"
