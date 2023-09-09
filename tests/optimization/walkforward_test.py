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

from xoney.optimization.validation.walkforward import WFSampler
from xoney.optimization.validation.validator import Validator
from xoney.optimization import GeneticAlgorithmOptimizer
from xoney.backtesting import Backtester
from xoney.analysis.metrics import SharpeRatio
from xoney import timeframes, ChartContainer, Instrument, Chart
from xoney import TradingSystem
from xoney.strategy import IntParameter


instrument = Instrument("SOME/THING", timeframes.DAY_1)

@pytest.fixture
def sampler():
    return WFSampler(timeframes.DAY_1*10,
                     timeframes.DAY_1*10,
                     optimizer=GeneticAlgorithmOptimizer(
                         backtester=Backtester(),
                         metric=SharpeRatio),
                     backtester=Backtester())


@pytest.fixture
def trades_sampler():
    return WFSampler(timeframes.DAY_1*10,
                     timeframes.DAY_1*10,
                     optimizer=GeneticAlgorithmOptimizer(
                         backtester=Backtester(),
                         metric=SharpeRatio,
                         max_trades=IntParameter(1, 5)),
                     backtester=Backtester())



@pytest.fixture
def charts(dataframe):
    return ChartContainer(
        {instrument: Chart(df=dataframe)}
    )

def test_working(sampler, charts, TrendCandleStrategy):
    validator = Validator(charts=charts,
                          sampler=sampler)
    validator.test(TradingSystem({TrendCandleStrategy(): [instrument],
                                  TrendCandleStrategy(): [instrument]}))


def test_error(charts, TrendCandleStrategy):
    with pytest.raises(TypeError):
        sampler = WFSampler("not a <TimeFrame> or timedelta",
                            timeframes.DAY_1*10,
                            optimizer=GeneticAlgorithmOptimizer(
                                backtester=Backtester(),
                                metric=SharpeRatio,
                                max_trades=IntParameter(1, 5)),
                            backtester=Backtester())

        validator = Validator(charts=charts,
                              sampler=sampler)
        validator.test(TradingSystem({TrendCandleStrategy(): [instrument],
                                      TrendCandleStrategy(): [instrument]}))
