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

from typing import Collection

from numbers import Number

from xoney.system.exceptions import (IncorrectChartLength,
                                     InvalidChartParameters)


def validate_ohlc(open, high, low, close) -> None:
    for price in (open, high, low, close):
        if not isinstance(price, Number):
            raise TypeError("All candle fields must be numbers")


def validate_chart_length(*arrays) -> None:
    lens = map(len, arrays)
    if len(set(lens)) - 1:  # If elements have different length.
        raise IncorrectChartLength(lens)

def validate_chart_parameters(open,
                              high,
                              low,
                              close,
                              volume,
                              timestamp) -> None:
    for collection in (open, high, low, close, volume, timestamp):
        is_sequence: bool = isinstance(collection, Collection)
        is_not_normal: bool = isinstance(collection, (str, dict, set))
        if not is_sequence or is_not_normal:
            raise InvalidChartParameters
