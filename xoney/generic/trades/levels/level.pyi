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
from xoney.generic.trades import Trade


class Level(ABC):
    __trigger_price: float
    __side: TradeSide
    __trade_part: float
    __cross_flag: bool
    __quote_volume: float
    _trade: Trade
    _trade_volume: float

    @property
    def trade_part(self) -> float:
        ...

    @property
    def trigger_price(self) -> float:
        ...

    @property
    def side(self) -> TradeSide:
        ...

    @property
    def crossed(self) -> bool:
        ...

    def _update_trade_volume(self) -> None:
        ...

    def __init__(self,
                 price: float,
                 trade_part: float):
        ...

    def edit_trigger_price(self, price: float) -> None:
        ...

    def check_breaking(self, candle: Candle) -> bool:
        ...

    def update(self, candle: Candle) -> None:
        ...

    def _update_volume(self) -> None:
        ...

    def _bind_trade(self, trade: Trade) -> None:
        ...

    @property
    def quote_volume(self) -> float:
        ...

    @property
    def base_volume(self) -> float:
        ...

    def __eq__(self, other) -> bool:
        same_side: bool
        same_price: bool
        same_quantity: bool
        same_status: bool
        ...

    def __repr__(self) -> str:
        ...

    def _on_update_callback(self):
        ...

    def _on_breakout_callback(self):
        ...
