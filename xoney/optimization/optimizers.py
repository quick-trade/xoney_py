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

from typing import Callable, Any

from optuna.trial import FrozenTrial

from xoney.optimization import Optimizer
from xoney.generic.routes import TradingSystem, Instrument
from xoney.generic.candlestick import Chart
from xoney.analysis.metrics import Metric
from xoney.strategy import (Parameter,
                            IntParameter,
                            FloatParameter,
                            CategoricalParameter)

from xoney.optimization._system_parsing import Parser

from xoney.system.exceptions import UnexpectedParameter

from optuna import Study, create_study, Trial
from optuna.samplers import NSGAIISampler


def _parameter_to_value(parameter: Parameter,
                        path: str,
                        trial: Trial) -> Any:
    if isinstance(parameter, IntParameter):
        return trial.suggest_int(name=path,
                                 low=parameter.min,
                                 high=parameter.max)
    if isinstance(parameter, FloatParameter):
        return trial.suggest_float(name=path,
                                  low=parameter.min,
                                  high=parameter.max)
    if isinstance(parameter, CategoricalParameter):
        return trial.suggest_categorical(name=path,
                                         choices=parameter.categories)
    else:
        raise UnexpectedParameter(parameter)


class DefaultOptimizer(Optimizer):  # TODO
    _study: Study
    _study_params: dict[str, object] = dict()
    _opt_params: dict[str, object] = dict()

    def __initialize_metric(self, metric: Metric | type) -> None:
        if isinstance(metric, type):
            metric = metric()
        self._metric = metric

    def __max_trades_parameter(self,
                               min: int | None,
                               max: int | None) -> IntParameter:
        # During the optimization process, the parameter of the maximum
        # number of open trades can change, but if it is not specified,
        # then the strategy has 1 trade for 1 pair.
        n_instruments = self._trading_system.n_instruments
        if min is None or max is None:
            min = n_instruments
            max = n_instruments
        return IntParameter(min=min,
                            max=max)

    def __initialize_parser(self, trading_system: TradingSystem) -> None:
        self._parser = Parser(system_signature=trading_system)

    def _system_to_objective(
            self,
            trading_system: TradingSystem,
            max_trades: IntParameter,
            charts: dict[Instrument, Chart],
            commission: float,
            metric: Metric
    ) -> Callable[[Trial], float]:
        self.__initialize_parser(trading_system=trading_system)

        def objective(trial: Trial) -> float:
            flatten: dict[str, Any] = dict()
            for path, parameter in self._parser.parameters:
                flatten[path] = _parameter_to_value(
                    parameter=parameter,
                    path=path,
                    trial=trial
                )
            flatten["max_trades"] = _parameter_to_value(parameter=max_trades,
                                                         path="max_parameter",
                                                         trial=trial)
            system: TradingSystem = self._parser.as_system(flatten=flatten)
            self._backtester.run(trading_system=system,
                                charts=charts,
                                commission=commission)
            return self._backtester.equity.evaluate(metric=metric)

        return objective

    def run(self,
            trading_system: TradingSystem,
            charts: dict[Instrument, Chart],
            metric: Metric | type,
            commission: float = 0.1 * 0.01,
            min_trades: int | None = None,
            max_trades: int | None = None,
            **kwargs) -> None:
        self.__initialize_metric(metric)
        self._trading_system = trading_system
        direction: str = "maximize" if metric.positive else "minimize"
        self._study = create_study(direction=direction,
                                   **self._study_params)
        max_trades_parameter: IntParameter = self.__max_trades_parameter(
            min=min_trades,
            max=max_trades
        )
        objective = self._system_to_objective(
            trading_system=trading_system,
            max_trades=max_trades_parameter,
            charts=charts,
            commission=commission,
            metric=self._metric
        )
        self._study.optimize(func=objective,
                             **self._opt_params)

    def _best_trials(self, n: int) -> list[FrozenTrial]:
        # length of values is 1, because only 1 metric
        # can be used in optimization
        trial_score: Callable = lambda trial: trial.values[0]
        trials: list[FrozenTrial] = self._study.trials
        sorted_trials: list = sorted(trials, key=trial_score)
        if not self._metric.positive:
            sorted_trials = sorted_trials[::-1]
        return sorted_trials[-n:][::-1]  # The best systems should come first

    def _trial_to_system(self, trial: FrozenTrial) -> TradingSystem:
        settings: dict[str, Any] = trial.params
        return self._parser.as_system(flatten=settings)

    def best_systems(self, n: int = 1) -> list[TradingSystem]:
        systems: map = map(self._trial_to_system,
                           self._best_trials(n=n))
        return list(systems)


class GeneticAlgorithmOptimizer(DefaultOptimizer):
    _opt_params: dict[str, object] = dict(sampler=NSGAIISampler())
