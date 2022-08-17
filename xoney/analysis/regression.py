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
from abc import ABC, abstractproperty, abstractmethod

import numpy as np


class RegressionModel(ABC):
    _result: np.ndarray

    @property
    def curve(self) -> np.ndarray:
        return self._result

    @abstractmethod
    def fit(self, array: np.ndarray) -> None:
        ...


class LinearRegression(RegressionModel):
    def fit(self, array: np.ndarray) -> None:
        x = np.arange(0, len(array) + 1)
        slope, intercept = np.polyfit(x, array, 1)
        linear: np.ndarray = x * slope + intercept

        self._result = linear


class ExponentialRegression(RegressionModel):
    def fit(self, array: np.ndarray) -> None:
        linear_model: LinearRegression = LinearRegression()
        linear_model.fit(array=np.log(array))
        self._result = np.exp(linear_model.curve)
