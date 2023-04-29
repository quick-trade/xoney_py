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
from multiprocessing import cpu_count
from datetime import datetime


ASSUME_ZERO = 10 ** -10

n_processes = cpu_count()

DEFAULT_CURR_TIME = datetime(1970, 1, 1)


SYMBOL_SPLIT: str = "/"
EXCHANGE_REGEX: str = r"[a-zA-Z0-9]+"
EXCHANGE_SPLIT: str = ":"
# [A-Z0-9]+ -- Capital letters or numbers;
SYMBOL: str = r"[A-Z0-9]+" + SYMBOL_SPLIT + r"[A-Z0-9]+"
