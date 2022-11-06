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
from xoney.strategy import Strategy
from xoney.generic.candlestick import Chart, Candle
from xoney.generic.events import Event, OpenTrade, CloseAllTrades
from xoney.generic.enums import TradeSide
from xoney.generic.trades import Trade
from xoney.generic.trades.levels import LevelHeap, SimpleEntry
from xoney.backtesting import Backtester


class TrendCandleStrategy(Strategy):
    _signal: str
    candle: Candle

    def __init__(self, n: int = 3):
        self._signal = None
        self.edit_settings({'n': n})

    def run(self, chart: Chart) -> None:
        diff: np.ndarray = chart.close - chart.open
        if all(diff > 0):
            signal = "long"
        elif all(diff < 0):
            signal = "short"
        else:
            signal = None

        if self._signal != signal:
            self._signal = signal
        else:
            self._signal = None

        self.candle = chart[-1]

    def fetch_events(self) -> Iterable[Event]:
        if self._signal == "long":
            return [
                CloseAllTrades(),
                OpenTrade(
                    Trade(
                        side=TradeSide.LONG,
                        entries=LevelHeap(
                            [
                                SimpleEntry(
                                    trade_part=1,
                                    price=self.candle.close
                                )
                            ]
                        ),
                        breakouts=LevelHeap()
                    )
                )
            ]

        if self._signal == "short":
            return [
                CloseAllTrades(),
                OpenTrade(
                    Trade(
                        side=TradeSide.SHORT,
                        entries=LevelHeap(
                            [
                                SimpleEntry(
                                    trade_part=1,
                                    price=self.candle.close
                                )
                            ]
                        ),
                        breakouts=LevelHeap()
                    )
                )
            ]
        return []


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
def test_return_type_equity(dataframe, n, deposit, commission):
    backtester = Backtester(strategies=[TrendCandleStrategy(n=n)])
    backtester.run(chart=dataframe,
                   initial_depo=deposit,
                   commission=commission)
    assert isinstance(backtester.equity, Equity)


@pytest.mark.parametrize("max_trades",
                         [1, 2, 3])
def test_set_max_trades(dataframe, max_trades):
    backtester_1 = Backtester(strategies=[TrendCandleStrategy()],
                              max_trades=max_trades)
    backtester_1.run(chart=dataframe, initial_depo=100, commission=0.01)
    equity_1 = backtester_1.equity

    backtester_2 = Backtester(strategies=[TrendCandleStrategy()])
    backtester_2.set_max_trades(max_trades=max_trades)
    backtester_2.run(chart=dataframe, initial_depo=100, commission=0.01)
    equity_2 = backtester_2.equity

    assert equity_2 == equity_1