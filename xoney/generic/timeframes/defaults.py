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

from .factory import TimeFrameFactory

MINUTE_1 = TimeFrameFactory.from_minutes(1)
MINUTE_3 = TimeFrameFactory.from_minutes(3)
MINUTE_5 = TimeFrameFactory.from_minutes(5)
MINUTE_15 = TimeFrameFactory.from_minutes(15)
MINUTE_30 = TimeFrameFactory.from_minutes(30)
MINUTE_45 = TimeFrameFactory.from_minutes(45)
HOUR_1 = TimeFrameFactory.from_hours(1)
HOUR_2 = TimeFrameFactory.from_hours(2)
HOUR_3 = TimeFrameFactory.from_hours(3)
HOUR_4 = TimeFrameFactory.from_hours(4)
DAY_1 = TimeFrameFactory.from_days(1)
DAY_3 = TimeFrameFactory.from_days(3)
WEEK_1 = TimeFrameFactory.from_weeks(1)
