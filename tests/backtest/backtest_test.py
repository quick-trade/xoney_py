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
# WITHOUT WARRANTIES OR CONDITIONS OF ANY KIND either express or implied.
# See the License for the specific language governing permissions and
# limitations under the License.
# =============================================================================
import numpy as np
from typing import Iterable

import pytest

from xoney.generic.equity import Equity
from xoney.generic.routes import Instrument
from xoney.strategy import Strategy
from xoney.generic.candlestick import Chart, Candle
from xoney.generic.events import Event, OpenTrade, CloseStrategyTrades
from xoney.generic.enums import TradeSide
from xoney.generic.trades import Trade, TradeMetaInfo
from xoney.generic.trades.levels import LevelHeap, SimpleEntry
from xoney.backtesting import Backtester
from xoney import TradingSystem, Symbol
from xoney.generic.timeframes import DAY_1


@pytest.fixture
def dataframe():
    base = np.array(
        [1, 2, 3, 4, 5, 3, 6, 2, 1, 1, 1, 1, 2, 3, 4, 5, 6, 7, 8, 9, 3]
    )
    return Chart(
        open=base[:-1],
        high=base[:-1]+1,
        low=base[:-1]*0.5+0.1,
        close=base[1:]
    )

@pytest.mark.parametrize("commission",
                         [0.1, 0, 0.01, 0.5])
@pytest.mark.parametrize("deposit",
                         [100, 0.1, 897*10**5])

@pytest.mark.parametrize("n",
                         [1, 2, 3, 4, 5])
def test_return_type_equity(dataframe, n, deposit, commission, TrendCandleStrategy):
    some_pair = Instrument(Symbol("SOME/THING"), DAY_1)
    strategy = TrendCandleStrategy(n=n)

    trading_system = TradingSystem(config={strategy: [some_pair]})

    backtester = Backtester(initial_depo=deposit,
                            commission=commission)
    backtester.run(charts={some_pair: dataframe},
                   trading_system=trading_system)
    assert isinstance(backtester.equity, Equity)
