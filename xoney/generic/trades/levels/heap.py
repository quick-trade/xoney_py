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

import copy
from typing import Iterable

from xoney.generic.candlestick import Candle
from xoney.generic.trades.levels import Level


class LevelHeap:
    __levels: list[Level]

    def __init__(self, levels: Iterable[Level] | None = None):
        if levels is None:
            levels = []
        self.__levels = list(levels)

    def __iter__(self):
        level: Level
        for level in self.__levels:
            yield level

    def add(self, level: Level) -> None:
        self.__levels.append(level)

    def remove(self, level: Level) -> None:
        member: Level

        for member in self.__levels:
            if member == level:
                self.__levels.remove(member)
                break

    def update(self, candle: Candle) -> None:
        """
        Update the state of all levels in the heap.
        :param candle: Candle by which the crossing of each
        of the levels will be checked.
        """

        level: Level
        for level in self.__levels:
            level.update(candle=candle)

    @property
    def crossed(self) -> LevelHeap:
        """
        :return: Already crossed levels.
        """

        crossed: LevelHeap = LevelHeap()

        level: Level
        for level in self.__levels:
            if level.crossed:
                crossed.add(level)

        return crossed

    @property
    def pending(self) -> LevelHeap:
        """
        :return: Levels waiting to be crossed.
        """

        pending: LevelHeap = LevelHeap()

        level: Level
        for level in self.__levels:
            if not level.crossed:
                pending.add(level)

        return pending

    def get_levels(self) -> list[Level]:
        """
        :return: Copies of all levels in the heap.
        """
        return copy.deepcopy(self.__levels)

    @property
    def quote_volume(self) -> float:
        level: Level

        return sum(
            level.quote_volume
            for level in self.__levels
        )

    def __len__(self):
        return len(self.__levels)

    def __contains__(self, item):
        for level in self.__levels:
            if level == item:
                return True
        return False

    def __repr__(self):
        return f"{self.__class__.__name__}({str(self.__levels)})"
