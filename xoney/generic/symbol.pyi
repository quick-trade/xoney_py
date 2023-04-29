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

from re import Match


_EXCHANGE_SYMBOL: str

def _full_match(text: str, pattern: str) -> Match:
    ...

class Symbol:
    __symbol: str
    __exchange: str
    __base: str
    __quote: str
    __pair: str

    @property
    def symbol(self) -> str:
        ...

    @property
    def pair(self) -> str:
        ...

    @property
    def base(self) -> str:
        ...

    @property
    def quote(self) -> str:
        ...

    @property
    def exchange(self) -> str:
        ...

    def __init__(self, symbol: str) -> None:
        ...

    def __parse_exchange(self) -> None:
        match_: Match
        ...

    def __parse_pair(self) -> None:
        match_: Match
        ...

    def __repr__(self) -> str:
        ...

    def __eq__(self, other) -> bool:
        symbol: str
        ...

    def __hash__(self) -> int:
        ...
