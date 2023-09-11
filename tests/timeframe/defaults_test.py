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
import pytest

from xoney.generic.timeframes import defaults, TimeFrame
from datetime import timedelta


def assert_minute_timeframe(timeframe, minutes):
    expected_seconds = 60 * minutes
    assert timeframe.seconds == expected_seconds
    assert timeframe.timedelta == timedelta(
        seconds=expected_seconds
    )
    assert timeframe.candles_in_year == (60 / minutes) * 24 * 365
    assert str(timeframe) == f"{minutes}m"


def assert_hour_timeframe(timeframe, hours):
    expected_seconds = 60 * 60 * hours
    assert timeframe.seconds == expected_seconds
    assert timeframe.timedelta == timedelta(
        seconds=expected_seconds
    )
    assert timeframe.candles_in_year == (24/hours) * 365
    assert str(timeframe) == f"{hours}h"


def assert_day_timeframe(timeframe, days):
    expected_seconds = 60 * 60 * 24 * days
    assert timeframe.seconds == expected_seconds
    assert timeframe.timedelta == timedelta(
        seconds=expected_seconds
    )
    assert timeframe.candles_in_year == 365 / days
    assert str(timeframe) == f"{days}d"


def assert_week_timeframe(timeframe, weeks):
    expected_seconds = 60 * 60 * 24 * 7 * weeks
    assert timeframe.seconds == expected_seconds
    assert timeframe.timedelta == timedelta(
        seconds=expected_seconds
    )
    assert timeframe.candles_in_year == 365 / (weeks*7)
    assert str(timeframe) == f"{weeks}w"


class TestDefaults:
    def test_minute_1(self):
        assert_minute_timeframe(defaults.MINUTE_1, 1)

    def test_minute_3(self):
        assert_minute_timeframe(defaults.MINUTE_3, 3)

    def test_minute_5(self):
        assert_minute_timeframe(defaults.MINUTE_5, 5)

    def test_minute_15(self):
        assert_minute_timeframe(defaults.MINUTE_15, 15)

    def test_minute_30(self):
        assert_minute_timeframe(defaults.MINUTE_30, 30)

    def test_minute_45(self):
        assert_minute_timeframe(defaults.MINUTE_45, 45)

    def test_hour_1(self):
        assert_hour_timeframe(defaults.HOUR_1, 1)

    def test_hour_2(self):
        assert_hour_timeframe(defaults.HOUR_2, 2)

    def test_hour_3(self):
        assert_hour_timeframe(defaults.HOUR_3, 3)

    def test_hour_4(self):
        assert_hour_timeframe(defaults.HOUR_4, 4)

    def test_day_1(self):
        assert_day_timeframe(defaults.DAY_1, 1)

    def test_day_3(self):
        assert_day_timeframe(defaults.DAY_3, 3)

    def test_week_1(self):
        assert_week_timeframe(defaults.WEEK_1, 1)


@pytest.mark.parametrize("name", ["1 day", "2 days", "3 days", "4 days"])
def test_name(name):
    tf = TimeFrame(name, 3600)
    assert tf.name == name
