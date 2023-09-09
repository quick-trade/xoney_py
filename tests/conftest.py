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

from typing import Iterable

import pandas as pd
import numpy as np

from xoney.strategy import Strategy
from xoney.generic.candlestick import Chart, Candle
from xoney.generic.events import Event, OpenTrade, CloseStrategyTrades
from xoney.generic.enums import TradeSide
from xoney.generic.trades import Trade, TradeMetaInfo
from xoney.generic.trades.levels import LevelHeap, SimpleEntry
from xoney.strategy import IntParameter, CategoricalParameter, Parameter

from .data_array import tohlcv


class _Strategy(Strategy):
    _signal: str
    candle: Candle
    flip: bool

    def __init__(self, n: int = 3, flip=False):
        super().__init__(n=n)
        self._signal = None
        self.flip = flip

    def run(self, chart: Chart) -> None:
        diff: np.ndarray = chart.close - chart.open
        if all(diff > 0):
            signal = "long"
        elif all(diff < 0):
            signal = "short"
        else:
            signal = None

        if self.flip:
            if signal == "long":
                signal = "short"
            if signal == "short":
                signal = "long"

        if self._signal != signal:
            self._signal = signal
        else:
            self._signal = None

        self.candle = chart[-1]

    def fetch_events(self) -> Iterable[Event]:
        if self._signal == "long":
            return [
                CloseStrategyTrades(strategy_id=self._id),
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
                        breakouts=LevelHeap(),
                        meta_info=TradeMetaInfo(strategy_id=self._id)
                    )
                )
            ]

        if self._signal == "short":
            return [
                CloseStrategyTrades(strategy_id=self._id),
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
                        breakouts=LevelHeap(),
                        meta_info=TradeMetaInfo(strategy_id=self._id)
                    )
                )
            ]
        return []

    @property
    def parameters(self) -> dict[str, Parameter]:
        return {"n": IntParameter(1, 6),
                "flip": CategoricalParameter([False, True])}

@pytest.fixture(scope="session", autouse=True)
def TrendCandleStrategy():
    return _Strategy


@pytest.fixture(scope="session", autouse=True)
def dataframe():
    data = tohlcv
    columns = ["Timestamp", "Open", "High", "Low", "Close", "Volume"]
    df = pd.DataFrame(data, columns=columns)
    df["Timestamp"] = pd.to_datetime(df["Timestamp"])
    return df
