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
from __future__ import annotations

from typing import Any
from abc import ABC


from xoney import Instrument, Chart, TradingSystem
from xoney.generic.routes import ChartContainer
from xoney.backtesting import Backtester
from xoney.generic.equity import Equity
from xoney.optimization import Optimizer
from xoney.backtesting._utils import equity_timestamp, min_timeframe

import copy


class Sample(ABC):
    charts: ChartContainer


    def __init__(self,
                 charts: dict[Instrument, Chart] | ChartContainer,
                 *args,
                 **kwargs) -> None:
        if not isinstance(charts, ChartContainer):
            charts = ChartContainer(charts=charts)
        self.charts = charts


class InSample(Sample):
    _optimizer: Optimizer
    _opt_params: dict[str, Any]


    def __init__(self,
                 charts: dict[Instrument, Chart] | ChartContainer,
                 optimizer: Optimizer,
                 deepcopy: bool = True) -> None:
        super().__init__(charts)
        if deepcopy:
            optimizer = copy.deepcopy(optimizer)
        self._optimizer = optimizer

    def optimize(self,
                 trading_system: TradingSystem,
                 opt_params: dict[str, Any] | None = None) -> None:
        if opt_params is None:
            opt_params = dict()
        self._opt_params = opt_params
        self._optimizer.run(trading_system=trading_system,
                            charts=self.charts,
                            **self._opt_params)

    def select_system(self) -> TradingSystem:
        return self._optimizer.best_systems(n=1)[0]


class OutOfSample(Sample):
    bt_params: dict[str, Any]
    _backtester: Backtester
    __equity: Equity
    __trading_system: TradingSystem


    @property
    def equity(self):
        return self.__equity

    @property
    def trading_system(self) -> TradingSystem:
        return self.__trading_system

    def __init__(self,
                 charts: dict[Instrument, Chart] | ChartContainer,
                 backtester: Backtester,
                 deepcopy_bt: bool = True):
        super().__init__(charts=charts)

        if deepcopy_bt:
            backtester = copy.deepcopy(backtester)
        self._backtester = backtester

    def backtest(self,
                 trading_system: TradingSystem,
                 bt_kwargs: dict[str, Any] | None = None):
        if bt_kwargs is None:
            bt_kwargs = dict()
        self.bt_params = bt_kwargs

        self._backtester.run(trading_system=trading_system,
                             charts=self.charts,
                             **self.bt_params)
        self.__equity = self._backtester.equity
        self.__trading_system = trading_system


def walk_forward_timestamp(charts) -> tuple[tuple, tuple]:
    times = equity_timestamp(charts=charts,
                             timeframe=min_timeframe(charts=charts))
    # TODO: implement
