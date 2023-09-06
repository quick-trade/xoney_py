# Copyright 2023 Vladyslav Kochetov. All Rights Reserved.
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
import pytest
from datetime import datetime, timedelta

import pandas as pd

from xoney.backtesting._utils import _equity_start_stop, time_adjustment
from xoney import timeframes


@pytest.fixture
def timestamp_1h():
    return pd.date_range(
        datetime(2000, 1, 1, 1, 1, 0),
        datetime(2002, 1, 1, 2, 1, 0),
        freq=timeframes.HOUR_1.timedelta
    )


@pytest.fixture
def timestamp_3D():
    return pd.date_range(
        datetime(1995, 1, 1, 1, 1, 0),
        datetime(2001, 1, 1, 1, 1, 0),
        freq=timeframes.DAY_3.timedelta
    )


def test_different_timeframes(timestamp_1h, timestamp_3D):
    start, stop = _equity_start_stop([timestamp_3D, timestamp_1h])
    assert datetime(2000, 1, 1, 1, 1, 0) == start
    assert datetime(2002, 1, 1, 2, 1, 0) == stop

def test_float_adjustment():
    adj = 0.5
    timeframe = timeframes.HOUR_1
    result = time_adjustment(adj, timeframe)
    expected = timedelta(hours=0.5)
    assert result == expected

def test_timeframe_adjustment():
    adj = timeframes.DAY_3
    timeframe = timeframes.HOUR_1
    result = time_adjustment(adj, timeframe)
    expected = timedelta(days=3)
    assert result == expected

def test_timedelta_adjustment():
    adj = timedelta(hours=2)
    timeframe = timeframes.HOUR_1
    result = time_adjustment(adj, timeframe)
    expected = timedelta(hours=2)
    assert result == expected

def test_invalid_adjustment():
    adj = "invalid_adjustment"
    timeframe = timeframes.HOUR_1
    with pytest.raises(ValueError):
        time_adjustment(adj, timeframe)
