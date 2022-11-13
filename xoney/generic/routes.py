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

from typing import Iterable
from dataclasses import dataclass

from xoney.generic.symbol import Symbol
from xoney.generic.timeframes import TimeFrame
from xoney.strategy import Strategy


@dataclass(frozen=True)
class Instrument:
    symbol: Symbol
    timeframe: TimeFrame


class TradingSystem:
    _config: dict[Strategy, Iterable[Instrument]]

    def __init__(self, config: dict[Strategy, Iterable[Instrument]]):
        self._config = config

    @property
    def items(self) -> list[tuple[Strategy, Instrument]]:
        items: list[tuple[Strategy, Instrument]] = []

        strategy: Strategy
        instruments: Iterable[Instrument]
        instrument: Instrument
        for strategy, instruments in self._config.items():
            for instrument in instruments:
                items.append((strategy, instrument))

        return items
