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
import numpy as np
from scipy import stats


def max_variance(x: np.ndarray,
                 alpha: float = 0.05):
    df: int = len(x) - 1
    sample_var = stats.variation(x)
    chi2: float = stats.chi2.ppf(1-alpha, df=df)

    return (df * sample_var) / chi2


def max_std(x: np.ndarray,
            alpha: float = 0.05):
    return np.sqrt(max_variance(x=x, alpha=alpha))
