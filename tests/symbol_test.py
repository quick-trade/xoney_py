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

import pytest

from xoney.generic.symbol import Symbol
from xoney.system.exceptions import InvalidSymbolError


class TestSymbolCorrectInitialization:
    def assert_base_quote_symbol(self):
        assert self.pair.base == "BTC"
        assert self.pair.quote == "USD"
        assert self.pair.pair == "BTC/USD"

    def test_base_quote_arg(self):
        self.pair = Symbol("BTC/USD")
        self.assert_base_quote_symbol()

    def test_base_quote_kwarg(self):
        self.pair = Symbol(symbol="BTC/USD")
        self.assert_base_quote_symbol()

    def test_exchange(self):
        self.pair = Symbol("BINANCE:BTC/USD")
        assert self.pair.exchange == "BINANCE"
        self.assert_base_quote_symbol()


class TestSymbolIncorrectInitialization:
    def test_unexpected_arg_type(self):
        with pytest.raises(TypeError):
            self.pair = Symbol(5)

    @pytest.mark.parametrize("args", [
        ("BTC", 5),
        (5, 5, 5),
        (5, "BTC"),
    ])
    def test_unexpected_args_type(self, args):
        with pytest.raises(TypeError):
            self.pair = Symbol(*args)


class TestInvalidSymbol:
    def test_incorrect_symbol(self):
        with pytest.raises(InvalidSymbolError):
            self.pair = Symbol(symbol="ABC 123")

    def test_incorrect_base_quote(self):
        with pytest.raises(InvalidSymbolError):
            self.pair = Symbol("AB3C./2AB{C")

    def test_incorrect_arg(self):
        with pytest.raises(InvalidSymbolError):
            self.pair = Symbol("ABC 123")


class TestEqual:
    def test_str(self):
        assert Symbol("BTC/USD") == "BTC/USD"

    def test_symbol(self):
        assert Symbol("BTC/USD") == Symbol("BTC/USD")

    @pytest.mark.parametrize("not_a_symbol", [
        1,
        {"BASE": "BTC",
         "QUOTE": "USD"}
    ])
    def test_false(self, not_a_symbol):
        assert (Symbol("BTC/USD") == not_a_symbol) == False


def test_str():
    symbol = Symbol("BTC/USD")
    assert str(symbol) == "BTC/USD"


def test_repr():
    symbol = Symbol("BTC/USD")
    assert repr(symbol) == "BTC/USD"

def test_hashing():
    symbol_1 = Symbol("BTC/CAD")
    symbol_2 = Symbol("BTC/CAD")
    hashtable = {symbol_1: 123, symbol_2: 234}
    assert len(hashtable.items()) == 1
