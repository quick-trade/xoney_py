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

from copy import deepcopy
from datetime import timedelta
from numbers import Number


class TimeFrame:
    __name: str
    __seconds: int | float
    __candles_in_year: float
    __timedelta: timedelta

    @property
    def timedelta(self) -> timedelta:
        return deepcopy(self.__timedelta)

    @property
    def seconds(self) -> int | float:
        return self.__seconds

    @property
    def candles_in_year(self) -> float:
        return self.__candles_in_year

    def __init__(self,
                 name: str,
                 seconds: int | float):
        self.__name = name
        self.__seconds = seconds
        self.__candles_in_year = self._candles_in_year()
        self.__timedelta = timedelta(seconds=seconds)

    def _candles_in_year(self) -> float:
        seconds_in_year: int = 365 * 24 * 60 * 60
        return seconds_in_year / self.seconds

    def __repr__(self) -> str:
        return self.__name

    def __eq__(self, other):
        if not isinstance(other, TimeFrame):
            raise TypeError("To compare an object with a <TimeFrame>, "
                            "this object must be of type <TimeFrame>")
        return self.seconds == other.seconds

    def __mul__(self, other):
        if isinstance(other, Number):
            return TimeFrame(name=f"{other}x{self}",
                             seconds=self.seconds * other)
        raise TypeError("To multiply the <TimeFrame> by an object, "
                        "that object must be a number")

    def __truediv__(self, other):
        if isinstance(other, Number):
            return TimeFrame(name=f"{self}/{other}",
                             seconds=self.seconds / other)
        raise TypeError("To divide the <TimeFrame> by an object, "
                        "that object must be a number")
