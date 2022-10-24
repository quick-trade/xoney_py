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
import numpy as np
import pandas as pd
import pytest

from .data_array import tohlcv
from xoney.generic.candlestick import Chart, Candle
from xoney.system.exceptions import IncorrectChartLength


@pytest.fixture
def dataframe():
    data = tohlcv
    columns = ["time", "open", "high", "low", "close", "volume"]
    return pd.DataFrame(data, columns=columns)


@pytest.fixture
def chart(dataframe):
    return Chart(open=dataframe["open"],
                 high=dataframe["high"],
                 low=dataframe["low"],
                 close=dataframe["close"],
                 timestamp=dataframe["time"],
                 volume=dataframe["volume"])


class TestOperations:
    def test_div_int(self, chart):
        result = chart / 3
        assert all(result.open == chart.open / 3)
        assert all(result.high == chart.high / 3)
        assert all(result.low == chart.low / 3)
        assert all(result.close == chart.close / 3)

    def test_div_chart(self, chart):
        result = chart / chart
        assert all(result.open == np.ones(chart.open.shape))
        assert all(result.high == chart.high / chart.low)
        assert all(result.low == chart.low / chart.high)
        assert all(result.close == np.ones(chart.close.shape))


class TestGetItem:
    @pytest.mark.parametrize("index",
                             [-1,
                              1,
                              0,
                              50])
    def test_candle(self, dataframe, chart, index):
        result = chart[index]
        expected = Candle(
            open=dataframe["open"].values[index],
            high=dataframe["high"].values[index],
            low=dataframe["low"].values[index],
            close=dataframe["close"].values[index],
            timestamp=dataframe["time"].values[index],
            volume=dataframe["volume"].values[index]
        )
        assert isinstance(result, Candle)
        assert result == expected
        assert result.volume == expected.volume
        assert result.timestamp == expected.timestamp

    @pytest.mark.parametrize("index",
                             [-1,
                              1,
                              0,
                              50,
                              52])
    def test_candle(self, dataframe, chart, index):
        expected = Candle(
            open=dataframe["open"].values[index],
            high=dataframe["high"].values[index],
            low=dataframe["low"].values[index],
            close=dataframe["close"].values[index],
            timestamp=dataframe["time"].values[index],
            volume=dataframe["volume"].values[index]
        )
        index = dataframe["time"].values[index]
        result = chart[index]
        assert isinstance(result, Candle)
        assert result == expected
        assert result.volume == expected.volume
        assert result.timestamp == expected.timestamp

    @pytest.mark.parametrize("index",
                             [slice(10, 30),
                              slice(0, -1),
                              slice(15, 25, 2),
                              slice(15, 25, 10),
                              slice(15, 25, 11)])
    def test_chart(self, dataframe, chart, index):
        expected = Chart(
            open=dataframe["open"].values[index],
            high=dataframe["high"].values[index],
            low=dataframe["low"].values[index],
            close=dataframe["close"].values[index],
            timestamp=dataframe["time"].values[index],
            volume=dataframe["volume"].values[index]
        )

        start = index.start
        stop = index.stop
        step = index.step

        index = dataframe["time"].values
        index = slice(index[start], index[stop], step)
        result = chart[index]
        assert isinstance(result, Chart)
        assert result == expected
        assert all(result.volume == expected.volume)
        assert result.timestamp == expected.timestamp


def test_empty():
    empty_chart = Chart()
    assert not empty_chart.open.shape[0]
    assert not empty_chart.high.shape[0]
    assert not empty_chart.low.shape[0]
    assert not empty_chart.close.shape[0]


def test_incorrect_lens():
    with pytest.raises(IncorrectChartLength):
        chart = Chart([1.], [1., 2., 3.], [3.], [4.3])
