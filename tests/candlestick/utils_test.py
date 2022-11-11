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

from xoney.generic.candlestick import _utils
import datetime as dt


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


class TestDefaultVolume:
    @pytest.mark.parametrize("value", [
        {"KEY": 123},
        42.42,
        0.5,
        "string"
    ])
    def test_typeerror(self, value):
        with pytest.raises(TypeError):
            _utils.default_volume(value)

    def test_list_123(self):
        result = _utils.default_volume(123)

        assert type(result) == list
        assert len(result) == 123

        for element in result:
            assert element == 1
            assert type(element) == float
