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

from xoney.system.exceptions import InvalidSymbolError
from . import _formatting
from . import _validation


class Symbol:
    __symbol: str = None
    __base: str
    __quote: str

    @property
    def symbol(self) -> str:
        return self.__symbol

    @property
    def base(self) -> str:
        return self.__base

    @property
    def quote(self) -> str:
        return self.__quote

    def __base_quote_from_symbol(self) -> tuple[str, str]:
        return _formatting.split_base_and_quote(self.__symbol)

    def __symbol_from_base_quote(self) -> str:
        return _formatting.pair_from_base_and_quote(
            base=self.base,
            quote=self.quote)

    def __generate_missing(self):
        if self.__symbol is not None:
            _validation.validate_symbol(self.symbol)
            self.__base, self.__quote = self.__base_quote_from_symbol()
        else:
            self.__symbol = self.__symbol_from_base_quote()
            _validation.validate_symbol(self.symbol)

    def __init__(self,
                 *args,
                 **kwargs):
        _validation.validate_parameters(args=args,
                                        kwargs=kwargs)
        # setting symbol, base and quote
        if "symbol" in kwargs:
            # symbol="BASE/QUOTE"
            self.__symbol = kwargs["symbol"]

        elif len(args) == 1:
            if not kwargs:
                # "BASE/QUOTE"
                self.__symbol = args[0]

            elif len(kwargs) == 1:
                if "quote" in kwargs:
                    # "BASE", quote="QUOTE"
                    self.__base = args[0]
                    self.__quote = kwargs["quote"]
                elif "base" in kwargs:
                    # "QUOTE", base="BASE"
                    self.__base = kwargs["base"]
                    self.__quote = args[0]

        elif len(args) == 2:
            # "BASE", "QUOTE"
            self.__base = args[0]
            self.__quote = args[1]

        elif "base" in kwargs and "quote" in kwargs:
            # base="BASE", quote="QUOTE"
            self.__base = kwargs["base"]
            self.__quote = kwargs["quote"]

        self.__generate_missing()

    def __repr__(self):
        return self.symbol

    def __eq__(self, other):
        symbol: str

        if isinstance(other, Symbol):
            symbol = other.symbol
        elif isinstance(other, str):
            symbol = other
        else:
            raise TypeError("To compare an object with symbol "
                            "that object must be of type <Symbol>")
        return self.symbol == symbol
