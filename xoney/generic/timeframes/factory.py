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

from .template import TimeFrame


class ToSeconds:
    @classmethod
    def from_minutes(cls, minutes: int | float) -> int | float:
        return minutes * 60

    @classmethod
    def from_hours(cls, hours: int | float) -> int | float:
        return cls.from_minutes(minutes=hours * 60)

    @classmethod
    def from_days(cls, days: int | float) -> int | float:
        return cls.from_hours(hours=days * 24)

    @classmethod
    def from_weeks(cls, weeks: int | float) -> int | float:
        return cls.from_days(days=weeks * 7)

class TimeFrameFactory:
    @classmethod
    def from_minutes(cls, minutes: int | float) -> TimeFrame:
        return TimeFrame(name=f"{minutes}m",
                         seconds=ToSeconds.from_minutes(minutes))

    @classmethod
    def from_hours(cls, hours: int | float) -> TimeFrame:
        return TimeFrame(name=f"{hours}h",
                         seconds=ToSeconds.from_hours(hours))

    @classmethod
    def from_days(cls, days: int | float) -> TimeFrame:
        return TimeFrame(name=f"{days}d",
                         seconds=ToSeconds.from_days(days))

    @classmethod
    def from_weeks(cls, weeks: int | float) -> TimeFrame:
        return TimeFrame(name=f"{weeks}w",
                         seconds=ToSeconds.from_weeks(weeks))

    @classmethod
    def from_seconds(cls, seconds: int | float) -> TimeFrame:
        return TimeFrame(name=f"{seconds}s",
                         seconds=seconds)
