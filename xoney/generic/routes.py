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

import itertools
from typing import Iterable
from dataclasses import dataclass

from xoney.generic.symbol import Symbol
from xoney.generic.timeframes import TimeFrame
from xoney.strategy import Strategy


@dataclass(frozen=True, unsafe_hash=True)
class Instrument:
    symbol: Symbol
    timeframe: TimeFrame


class TradingSystem:
    _config: dict[Strategy, Iterable[Instrument]]
    max_trades: int

    def __init__(self,
                 config: dict[Strategy, Iterable[Instrument]],
                 max_trades: int = 1):
        self._config = config
        self.max_trades = max_trades

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

    @property
    def strategies(self) -> tuple[Strategy, ...]:
        return tuple(self._config.keys())

    @property
    def instruments(self) -> tuple[Iterable[Instrument], ...]:
        return tuple(self._config.values())

    @property
    def n_instruments(self) -> int:
        """
        Number of unique instruments
        """
        flat_list: set[Instrument] = set(itertools.chain(*self.instruments))
        return len(flat_list)

    @property
    def n_strategies(self) -> int:
        """
        Number of pairs like (strategy, instrument)
        """

        flat_list: tuple[Instrument, ...] = tuple(itertools.chain(*self.instruments))
        return len(flat_list)
