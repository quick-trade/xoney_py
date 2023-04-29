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

from re import match

from xoney.config import SYMBOL, EXCHANGE_REGEX, EXCHANGE_SPLIT, SYMBOL_SPLIT
from xoney.system.exceptions import InvalidSymbolError


_EXCHANGE_SYMBOL = EXCHANGE_REGEX + EXCHANGE_SPLIT + SYMBOL

def _full_match(text, pattern):
    return match(pattern="^" + pattern + "$", string=text)


class Symbol:
    __exchange = None

    @property
    def symbol(self):
        return self.__symbol

    @property
    def pair(self):
        return self.__pair

    @property
    def base(self):
        return self.__base

    @property
    def quote(self):
        return self.__quote

    @property
    def exchange(self):
        return self.__exchange

    def __init__(self, symbol):
        self.__symbol = symbol
        self.__generate_missing()

    def __generate_missing(self):
        if _full_match(self.__symbol, _EXCHANGE_SYMBOL):
            self.__parse_exchange()
        elif not _full_match(self.__symbol, SYMBOL):
            raise InvalidSymbolError(self.__symbol)
        self.__parse_pair()

    def __parse_exchange(self):
        match_ = match(EXCHANGE_REGEX, self.__symbol)
        self.__exchange = match_.group()

    def __parse_pair(self):
        match_ = match(SYMBOL, self.__symbol)
        self.__pair = match_.group()
        self.__base, self.__quote = self.__pair.split(SYMBOL_SPLIT)

    def __repr__(self):
        return self.symbol

    def __eq__(self, other):
        if isinstance(other, Symbol):
            symbol = other.symbol
        elif isinstance(other, str):
            symbol = other
        else:
            return False
        return self.__symbol == symbol

    def __hash__(self):
        return hash(self.__symbol)
