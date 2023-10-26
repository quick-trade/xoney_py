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

from typing import Any, Type, Iterable

from dataclasses import dataclass

from xoney.generic.routes import TradingSystem, Instrument
from xoney.strategy import Parameter, Strategy


def _parameter_path_string(strategy: int, parameter: int) -> str:
    return f"s{strategy}p{parameter}"


@dataclass(frozen=True)
class ParameterPath:
    strategy: int
    parameter: int

    def as_string(self) -> str:
        return _parameter_path_string(strategy=self.strategy,
                                      parameter=self.parameter)


class Parser:
    __system_signature: TradingSystem
    __strategies: tuple[Strategy, ...]

    _parameters_names: tuple[tuple[str, ...], ...]
    _parameters_paths: tuple[tuple[ParameterPath, ...], ...]
    _parameters: tuple[tuple[Parameter, ...], ...]

    def __init__(self, system_signature: TradingSystem):
        self.__system_signature = system_signature
        self.__strategies = system_signature.strategies

        self.__save_parameters()
        self.__save_parameters_paths()
        self.__save_parameters_names()
        self.__save_parameters_table()

    def __save_parameters_paths(self) -> None:
        s: int
        p: int
        strategy: Strategy
        path: ParameterPath
        s_paths: list[ParameterPath]
        paths: list[tuple[ParameterPath, ...]] = []

        for s, strategy in enumerate(self.__strategies):
            s_paths = []
            for p, parameter in enumerate(self._parameters[s]):
                path = ParameterPath(strategy=s, parameter=p)
                s_paths.append(path)
            paths.append(tuple(s_paths))
        self._parameters_paths = tuple(paths)


    def __save_parameters_names(self) -> None:
        strategy: Strategy
        parameters_names: list[tuple[str, ...]] = []
        s_parameters_names: tuple[str, ...]

        for strategy in self.__strategies:
            s_parameters_names = tuple(strategy.parameters.keys())
            parameters_names.append(s_parameters_names)

        self._parameters_names = tuple(parameters_names)

    def __save_parameters(self) -> None:
        strategy: Strategy
        s_parameters: tuple[Parameter, ...]
        parameters: list[tuple[Parameter, ...]] = []

        for strategy in self.__strategies:
            s_parameters = tuple(strategy.parameters.values())
            parameters.append(s_parameters)

        self._parameters = tuple(parameters)

    def __save_parameters_table(self) -> None:
        paths: tuple[ParameterPath, ...]
        parameters: tuple[Parameter]
        path: ParameterPath
        parameter: Parameter

        table: dict[str, Parameter] = dict()

        for paths, parameters in zip(self._parameters_paths,
                                     self._parameters):
            for path, parameter in zip(paths, parameters):
                table[path.as_string()] = parameter

        self.__table = table

    @property
    def parameters(self) -> dict[str, Parameter]:
        return self.__table

    def as_system(self, flatten: dict[str, Any]) -> TradingSystem:
        config: dict[Strategy, Iterable[Instrument]] = dict()
        trading_system_type: Type[TradingSystem]
        instruments: tuple[Iterable[Instrument], ...]
        s_settings: dict[str, Any]
        s: int
        strategy: Strategy
        p: int
        parameter: str
        path: str
        strategy_class: Type[Strategy]
        max_trades: int

        instruments = self.__system_signature._strategy_instruments

        for s, strategy in enumerate(self.__strategies):
            s_settings = dict()
            for p, parameter in enumerate(self._parameters_names[s]):
                path = _parameter_path_string(strategy=s,
                                              parameter=p)
                s_settings[parameter] = flatten[path]
            strategy_class = type(strategy)
            config[strategy_class(**s_settings)] = instruments[s]

        max_trades = flatten["max_trades"]

        trading_system_type = type(self.__system_signature)
        return trading_system_type(config=config, max_trades=max_trades)
