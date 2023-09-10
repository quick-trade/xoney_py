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
# WITHOUT WARRANTIES OR CONDITIONS OF ANY KIND, either express or implied.
# See the License for the specific language governing permissions and
# limitations under the License.
# =============================================================================
import pytest

from xoney import ChartContainer, Instrument, timeframes, Chart


@pytest.fixture
def charts_dict(dataframe):
    return {Instrument("BTC/USD", timeframes.DAY_1): Chart(df=dataframe),
            Instrument("BTC/USD", timeframes.DAY_3): Chart(df=dataframe)}


@pytest.fixture
def custom_charts(charts_dict):
    return ChartContainer(charts_dict)


def test_n_instruments(system):
    instruments = system.instruments
    print(instruments)
    for i, instrument in enumerate(instruments):
        if i > 0:
            assert instrument[0] == instruments[i-1][0]
    assert system.n_instruments == 1


def test_chartcontainer_len(charts):
    assert len(charts) == 1


def test_len_chartcontainer_custom(custom_charts):
    assert len(custom_charts) == 2


def test_iter_container(custom_charts, charts_dict):
    assert list(custom_charts) == list(charts_dict)
