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

from xoney.generic.candlestick import utils
import datetime as dt
from xoney.generic.timeframes import HOUR_1


@pytest.fixture
def end_time():
    return dt.datetime(1991, 8, 24)


FROZEN_TIME = dt.datetime(2022, 2, 24, 5)


@pytest.fixture
def freeze_time(monkeypatch):
    class FrozenTime:
        @classmethod
        def now(cls):
            return FROZEN_TIME

    monkeypatch.setattr(dt, "datetime", FrozenTime)


class TestStartFromEnd:
    def test_1h_12(self, end_time):
        delta = dt.timedelta(hours=1)
        expected_start = dt.datetime(1991, 8, 23, 12)
        result = utils.start_from_end(end=end_time,
                                      period=12,
                                      delta=delta)
        assert result == expected_start

    def test_1d_7(self, end_time):
        delta = dt.timedelta(days=1)
        expected_start = dt.datetime(1991, 8, 17)
        result = utils.start_from_end(end=end_time,
                                      period=7,
                                      delta=delta)
        assert result == expected_start


class TestDateRange:
    def test_start_is_none_hour1(self, freeze_time):
        expected_values = [
            dt.datetime.now() - (HOUR_1 * 5).timedelta,
            dt.datetime.now() - (HOUR_1 * 4).timedelta,
            dt.datetime.now() - (HOUR_1 * 3).timedelta,
            dt.datetime.now() - (HOUR_1 * 2).timedelta,
            dt.datetime.now() - HOUR_1.timedelta,
        ]
        result = utils.date_range(timeframe=HOUR_1,
                                  length=5,
                                  start=None)
        for real, expected in zip(result, expected_values):
            assert real == expected


class TestDefaultVolume:
    @pytest.mark.parametrize("value", [
        {"KEY": 123},
        42.42,
        0.5,
        "string"
    ])
    def test_typeerror(self, value):
        with pytest.raises(TypeError):
            utils.default_volume(value)

    def test_list_123(self):
        result = utils.default_volume(123)

        assert type(result) == list
        assert len(result) == 123

        for element in result:
            assert element == 1
            assert type(element) == float
