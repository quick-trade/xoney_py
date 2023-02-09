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
        self._settings |= settings

    @abstractmethod
    def run(self, chart):  # pragma: no cover
        ...

    @abstractmethod
    def fetch_events(self):  # pragma: no cover
        ...

    @abstractproperty
    def parameters(self):  # pragma: no cover
        ...

    @property
    def min_candles(self):
        return 0

    @property
    def settings(self):
        return copy.deepcopy(self._settings)
