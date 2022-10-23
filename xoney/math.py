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

from typing import TypeVar

import numpy as np

from xoney.config import ASSUME_ZERO


T: TypeVar = TypeVar("T")


def is_zero(number) -> bool:
    return abs(number) <= ASSUME_ZERO


def is_equal(num_1, num_2) -> bool:
    return is_zero(divide(num_1, num_2) - 1) or num_1 == num_2


def multiply_diff(abs_change: T, multiplier: float | T = 1.0) -> T:
    difference: T = abs_change - 1
    multiplied_difference: T = difference * multiplier
    return 1 + multiplied_difference


def divide(num_1, num_2) -> float:
    if num_2 == num_1 == 0:
        return 1.0
    elif num_2 == 0:
        return np.inf
    return num_1 / num_2
