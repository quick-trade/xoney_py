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

from warnings import warn

import copy
from abc import ABC, abstractmethod, abstractproperty


class Strategy(ABC):
    _settings = dict()

    def __init__(self, **settings):
        self.edit_settings(settings)

    def edit_settings(self, settings):
        """
        Parameters for strategy optimization.

        for example:
            {"window_length": xoney.strategy.IntParameter(min=1, max=500)}

        Important: name of parameter will contains in _settings of the strategy

        """
        self._settings.update(settings)

    @abstractmethod
    def run(self, chart):  # pragma: no cover
        ...

    @abstractmethod
    def fetch_events(self):  # pragma: no cover
        ...

    @property
    def parameters(self):
        warn("[OPTIMIZATION WARNING] If you want to optimize parameters for "
        f"\"{self.__class__.__name__}\" strategy, you may redefine \"parameters()\" property")

    @property
    def min_candles(self):  # pragma: no cover
        return 0

    @property
    def settings(self):
        return copy.deepcopy(self._settings)

    def __hash__(self):
        return hash(tuple(self._settings.items()))
