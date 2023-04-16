# This Source Code Form is subject to the terms of the Mozilla Public
## Copyright 2022 Vladyslav Kochetov. All Rights Reserved.
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
import pandas as pd
import random
from xoney.generic.candlestick import Candle


random.seed(0)

def random_ohlc():
    randoms = [random.random() for _ in "ohlc"]
    l, *oc, h = sorted(randoms)
    random.shuffle(oc)
    o, c = oc
    return o, h, l, c


def random_candle():
    return Candle(*random_ohlc())


def random_df(length=100):
    data = []
    prev = Candle(length, length, length, length)
    for i in range(length):
        diff = random_candle()
        candle = prev + diff - 0.5
        data.append(candle.as_array())
        prev = candle
    return pd.DataFrame(data, columns=["Open", "High", "Low", "Close"])
