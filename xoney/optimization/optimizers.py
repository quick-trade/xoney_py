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
from xoney.backtesting import Backtester
from xoney.backtesting.backtester import Backtester

from xoney.optimization import Optimizer
from xoney.generic.routes import TradingSystem, Instrument, ChartContainer
from xoney.generic.candlestick import Chart
from xoney.analysis.metrics import Metric
from xoney.strategy import (Parameter,
                            IntParameter,
                            FloatParameter,
                            CategoricalParameter)

from xoney.optimization._system_parsing import Parser

from xoney.system.exceptions import UnexpectedParameter
from xoney.config import n_processes

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
    else:  # pragma: no cover
        raise UnexpectedParameter(parameter)


class DefaultOptimizer(Optimizer):
    _study: Study
    _study_params: dict[str, Any] = dict()
    _opt_params: dict[str, Any] = dict()
    _max_trades: IntParameter
    n_jobs: int
    n_trials: int | None

    def __init__(self,
                 backtester: Backtester,
                 metric: Metric,
                 max_trades: IntParameter | None = None,
                 n_jobs: int | None = None,
                 n_trials: int | None = None):
        if n_jobs is None:
            n_jobs = n_processes
        self.n_jobs = n_jobs
        self.n_trials = n_trials
        super().__init__(backtester=backtester,
                         metric=metric,
                         max_trades=max_trades)

    def __initialize_parser(self, trading_system: TradingSystem) -> None:
        self._parser = Parser(system_signature=trading_system)

    def _system_to_objective(self, trading_system: TradingSystem) -> Callable[[Trial], float]:
        self.__initialize_parser(trading_system=trading_system)

        def objective(trial: Trial) -> float:
            flatten: dict[str, Any] = dict()
            for path, parameter in self._parser.parameters.items():
                flatten[path] = _parameter_to_value(
                    parameter=parameter,
                    path=path,
                    trial=trial
                )
            flatten["max_trades"] = _parameter_to_value(parameter=self._max_trades,
                                                        path="max_trades",
                                                        trial=trial)
            system: TradingSystem = self._parser.as_system(flatten=flatten)
            return self._system_score(trading_system=system)

        return objective

    def run(self,
            trading_system: TradingSystem,
            charts: dict[Instrument, Chart] | ChartContainer,
            n_trials: int | None = None) -> None:
        if n_trials is None:
            n_trials = self.n_trials
        if n_trials is None:
            raise ValueError("n_trials must be specified in constructor or .run() method")
        if not isinstance(charts, ChartContainer):
            charts = ChartContainer(charts=charts)
        self._charts = charts
        self._trading_system = trading_system
        self._initialize_max_trades()

        self._opt_params.update(
            dict(n_jobs=self.n_jobs,
                 n_trials=n_trials)
        )
        direction: str = "maximize" if self._metric.positive else "minimize"
        self._study = create_study(direction=direction,
                                   **self._study_params)
        objective = self._system_to_objective(
            trading_system=trading_system
        )
        self._study.optimize(func=objective,
                             **self._opt_params)

    def _best_trials(self, n: int) -> list[FrozenTrial]:
        # length of values is 1, because only 1 metric
        # can be used in optimization
        trial_score: Callable = lambda trial: trial.values[0]
        trials: list[FrozenTrial] = self._study.trials
        # TODO: debug. Trials now is just a list of best trials
        sorted_trials: list = sorted(trials,
                                     key=trial_score,
                                     reverse=self._metric.positive)
        return sorted_trials[:n] # The best systems should come first

    def _trial_to_system(self, trial: FrozenTrial) -> TradingSystem:
        settings: dict[str, Any] = trial.params
        return self._parser.as_system(flatten=settings)

    def best_systems(self, n: int = 1) -> list[TradingSystem]:
        systems: map = map(self._trial_to_system,
                           self._best_trials(n=n))
        return list(systems)


class GeneticAlgorithmOptimizer(DefaultOptimizer):
    def __init__(self,
                 backtester: Backtester,
                 metric: Metric,
                 max_trades: IntParameter | None = None,
                 n_jobs: int | None = None,
                 n_trials: int | None = None,
                 population_size: int = 30,
                 mutation_prob: float | None = None,
                 crossover_prob: float = 0.9,
                 swapping_prob: float = 0.5,
                 seed: int | None = None,
                 **NSGA2_sampler_kwargs):
        self._study_params = dict(
            sampler=NSGAIISampler(population_size=population_size,
                                  mutation_prob=mutation_prob,
                                  crossover_prob=crossover_prob,
                                  swapping_prob=swapping_prob,
                                  seed=seed,
                                  **NSGA2_sampler_kwargs)
        )
        super().__init__(backtester=backtester,
                         metric=metric,
                         max_trades=max_trades,
                         n_jobs=n_jobs,
                         n_trials=n_trials)
