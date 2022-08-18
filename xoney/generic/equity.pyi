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

from typing import Iterable, Callable

from xoney.generic.timeframes import TimeFrame, DAY_1

import numpy as np


class Equity:
    _list: list[float]
    _timestamp: list
    timeframe: TimeFrame

    def as_array(self) -> np.ndarray:
        ...

    def __init__(self,
                 iterable: Iterable[float],
                 timestamp: list | None = None,
                 timeframe: TimeFrame = DAY_1):
        ...

    def append(self, balance: float) -> None:
        ...

    def update(self, balance: float) -> None:
        ...

    def __getitem__(self, item):
        item: int | slice
        ...

    def __op(self, fn: Callable, other) -> Equity:
        ...

    def __add__(self, other) -> Equity:
        ...

    def __sub__(self, other) -> Equity:
        ...

    def __mul__(self, other) -> Equity:
        ...

    def __truediv__(self, other) -> Equity:
        ...

    def __iter__(self):
        deposit: float
        ...

    def __len__(self) -> int:
        ...
