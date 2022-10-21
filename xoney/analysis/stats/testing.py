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


def critical_level_t_p(mean: float,
                       std: float,
                       n: int,
                       critical: float = 0.0,
                       alternative: str = "greater") -> float:
    """
    :param critical: Critical value for which the p-value is calculated.
    :param alternative: Type of alternative hypothesis.
        {"greater", "less"} (than critical)

    :return: one-sided p-value
    """
    df: int = n - 1

    p_value: float = stats.t.cdf(critical, df=df, scale=std, loc=mean)
    if alternative == "less":
        p_value = 1 - p_value
    elif alternative != "greater":
        raise ValueError("alternative must be \"less\" or \"greater\"")
    return p_value


def critical_level_sample_t_p(x: np.ndarray,
                              critical: float = 0.0,
                              alternative: str = "greater") -> float:
    return critical_level_t_p(mean=x.mean(),
                              std=x.std(),
                              n=len(x),
                              critical=critical,
                              alternative=alternative)
