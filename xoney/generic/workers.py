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
from abc import abstractproperty, ABC

from xoney.generic.trades import TradeHeap


class Worker(ABC):
    _trades: TradeHeap

    max_trades: int

    @property
    def opened_trades(self) -> int:
        return len(self._trades)

    @abstractproperty
    def total_balance(self) -> float:
        ...

    def used_balance(self) -> float:
        return self._trades.potential_volume

    @abstractproperty
    def free_balance(self) -> float:
        ...

    def filled_balance(self) -> float:
        return self._trades.filled_volume
