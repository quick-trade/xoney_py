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

from xoney.generic.timeframes import TimeFrameFactory
from xoney.generic.timeframes.defaults import HOUR_1, DAY_1, WEEK_1


class TestEqual:
    def test_d1_24h(self):
        D1 = TimeFrameFactory.from_days(1)
        H24 = TimeFrameFactory.from_hours(24)
        assert D1 == H24

    def test_d7_w1(self):
        D7 = TimeFrameFactory.from_days(7)
        W1 = TimeFrameFactory.from_weeks(1)
        assert D7 == W1

    def test_d7_h168(self):
        D7 = TimeFrameFactory.from_days(7)
        H168 = TimeFrameFactory.from_hours(168)
        assert D7 == H168

    def test_w1_h168(self):
        W1 = TimeFrameFactory.from_weeks(1)
        H168 = TimeFrameFactory.from_hours(168)
        assert W1 == H168

    def test_h1_m60(self):
        M60 = TimeFrameFactory.from_minutes(60)
        H1 = TimeFrameFactory.from_hours(1)
        assert H1 == M60

    def test_raises_str(self):
        M60 = TimeFrameFactory.from_minutes(60)
        with pytest.raises(TypeError):
            M60 == "string"

    def test_raises_int(self):
        W1 = TimeFrameFactory.from_weeks(1)
        with pytest.raises(TypeError):
            W1 == 1

    def test_raises_dict(self):
        D7 = TimeFrameFactory.from_days(7)
        with pytest.raises(TypeError):
            D7 == {"key": D7}


class TestMultiply:
    @pytest.mark.parametrize("timeframe", [
        DAY_1,
        HOUR_1,
        WEEK_1
    ])
    @pytest.mark.parametrize("value", [
        "string",
        {"KEY": 123},
        [1, 2, 3, 4, 5],
        (42,)
    ])
    def test_typeerror(self, value, timeframe):
        with pytest.raises(TypeError):
            self.result = timeframe * value

    def test_h1_int(self):
        result = HOUR_1 * 5
        assert result.seconds == HOUR_1.seconds * 5
        assert result.candles_in_year == HOUR_1.candles_in_year / 5
        assert str(result) == "5x1h"

    def test_h1_float(self):
        result = HOUR_1 * 5.5
        assert result.seconds == HOUR_1.seconds * 5.5
        assert result.candles_in_year == HOUR_1.candles_in_year / 5.5
        assert str(result) == "5.5x1h"


class TestDivision:
    def test_h1_int(self):
        result = HOUR_1 / 5
        assert result.seconds == HOUR_1.seconds / 5
        assert result.candles_in_year == HOUR_1.candles_in_year * 5
        assert str(result) == "1h/5"

    def test_h1_float(self):
        result = HOUR_1 / 5.5
        assert result.seconds == HOUR_1.seconds / 5.5
        assert result.candles_in_year == HOUR_1.candles_in_year * 5.5
        assert str(result) == "1h/5.5"

    def test_typeerror_h1_str(self):
        with pytest.raises(TypeError):
            HOUR_1 / "string"

    def test_typeerror_d1_str(self):
        with pytest.raises(TypeError):
            DAY_1 / "string"

    def test_typeerror_h1_dict(self):
        with pytest.raises(TypeError):
            HOUR_1 / {"KEY": 123}
