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

from abc import ABC, abstractmethod, abstractproperty
from typing import Iterable, Any

from xoney.generic.candlestick import Chart
from xoney.generic.events import Event
from xoney.strategy.parameters import Parameter


class Strategy(ABC):
    _settings: dict[str, Any]

    def __init__(self, **settings: dict[str, Any]):
        ...


    def edit_settings(self,
                      settings: dict[str, object]) -> None:
        ...

    @abstractmethod
    def run(self, chart: Chart) -> None:
        ...

    @abstractmethod
    def fetch_events(self) -> Iterable[Event]:
        ...

    @property
    def parameters(self) -> dict[str, Parameter]:
        ...

    @property
    def min_candles(self) -> int:
        ...

    @property
    def settings(self) -> dict[str, Any]:
        ...

    def __hash__(self) -> int:
        ...
