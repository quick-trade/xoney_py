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

from __future__ import annotations

from typing import Any

from xoney.system.exceptions import SymbolArgumentsError
from xoney.system.exceptions import InvalidSymbolError
import re

# [A-Z0-9]+ -- Capital letters or numbers;
# / -- Separation character (slash).
SYMBOL: str = r"[A-Z0-9]+/[A-Z0-9]+"


def valid_args_type(args: tuple, kwargs: dict) -> bool:
    for arg in (*args, *kwargs.values()):
        if not isinstance(arg, str):
            return False
    return True


def valid_kwargs(kwargs: dict) -> bool:
    arg_name: str
    for arg_name in kwargs:
        if arg_name not in ("base", "quote", "symbol"):
            return False
    return True


def validate_parameters(args: tuple, kwargs: dict[str, Any]) -> None:
    total_args_name: int = len(args) + len(kwargs)
    # validation arguments types
    if not valid_args_type(args=args, kwargs=kwargs):
        raise TypeError("All arguments must be of type <str>")

    # validation of kwargs
    invalid_kwargs: bool = not valid_kwargs(kwargs=kwargs)
    if invalid_kwargs or total_args_name not in (1, 2):
        raise SymbolArgumentsError(args=args, kwargs=kwargs)


def valid_symbol(symbol: str) -> bool:
    return bool(re.fullmatch(pattern=SYMBOL,
                             string=symbol))


def validate_symbol(symbol: str) -> None:
    if not valid_symbol(symbol):
        raise InvalidSymbolError(symbol)
