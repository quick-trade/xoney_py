# Copyright 2023 Vladyslav Kochetov. All Rights Reserved.
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

from xoney.optimization import DefaultOptimizer
from xoney.backtesting import Backtester
from xoney.analysis.metrics import SharpeRatio
from xoney.strategy import Parameter
from xoney.system.exceptions import UnexpectedParameter


@pytest.fixture
def optimizer():
    return DefaultOptimizer(Backtester(), SharpeRatio, max_trades=Parameter())


def test_parameter(optimizer, system, charts):
    with pytest.raises(UnexpectedParameter):
        optimizer.run(system, charts, n_trials=3)


def test_no_trials(optimizer, system, charts):
    with pytest.raises(ValueError):
        optimizer.run(system, charts, n_trials=None)
