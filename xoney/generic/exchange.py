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

from abc import ABC, abstractmethod


class Exchange(ABC):
    _stop_loss_type = "stop_loss"
    _take_profit_type = "take_profit_limit"
    _simple_entry_type = "market"
    _averaging_entry_type = "limit"

    @abstractmethod
    def new_order(self,
                  symbol: str,
                  side: str,
                  type: str,
                  amount: float,
                  price: float) -> Order:
        ...

    @abstractmethod
    def cancel_order(self, order: Order) -> None:
        ...

    def edit_order(self,
                   order: Order,
                   amount: float,
                   price: float) -> Order:
        self.cancel_order(order=order)
        return self.new_order(symbol=order.symbol,
                              side=order.side,
                              type=order.type,
                              amount=amount,
                              price=price)

    @abstractmethod
    def fetch_balance(self, currency: str, marker: str) -> float:
        ...

    def fetch_free_balance(self, currency: str) -> float:
        return self.fetch_balance(currency=currency, marker="free")

    def fetch_used_balance(self, currency: str) -> float:
        return self.fetch_balance(currency=currency, marker="used")

    def fetch_total_balance(self, currency: str) -> float:
        return self.fetch_balance(currency=currency, marker="total")


class Order:
    __id: str | int
    __symbol: str
    __type: str
    __side: str
    __amount: float
    __price: float | None
    __exchange: Exchange

    @property
    def symbol(self):
        return self.__symbol

    @property
    def side(self):
        return self.__side

    @property
    def id(self):
        return self.__id

    @property
    def amount(self):
        return self.__amount

    @property
    def price(self):
        return self.__price

    @property
    def type(self):
        return self.__type

    def __init__(self,
                 exchange: Exchange,
                 id: str | int,
                 symbol: str,
                 side: str,
                 type: str,
                 amount: float,
                 price: float | None):
        self.__id = id
        self.__symbol = symbol
        self.__side = side
        self.__type = type
        self.__amount = amount
        self.__price = price
        self.__exchange = exchange

    def edit_price(self, price: float):
        order_after_editing = self.__exchange.edit_order(
            order=self,
            amount=self.__amount,
            price=price
        )
        self.__id = order_after_editing.__id
        self.__price = price

    def edit_amount(self, amount: float):
        order_after_editing = self.__exchange.edit_order(
            order=self,
            amount=amount,
            price=self.__price
        )
        self.__id = order_after_editing.__id
        self.__amount = amount

    def cancel(self) -> None:
        self.__exchange.cancel_order(order=self)
