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
from typing import Sequence

from xoney.generic._series import TimeSeries
from xoney.generic.candlestick import Chart
from xoney.generic.routes import Instrument


def unify_series(series: Sequence[TimeSeries]) -> Sequence[TimeSeries]:
    """
    :return: Sequence of series with same length, but different timeframes (gaps filled)
    """
    ...  # TODO
    
def charts_length(unified: dict[Instrument, Chart]) -> int:
    return len(list(unified.values())[0])
