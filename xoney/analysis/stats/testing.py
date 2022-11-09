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

from xoney.analysis.stats import _intervals


def critical_level_p(mean: float,
                     std: float,
                     n: int,
                     critical: float = 0.0,
                     alternative: str = "greater") -> float:
    """
    :param critical: Critical value for which the p-value will be calculated.
    :param alternative: Type of alternative hypothesis. {"greater", "less"} (than critical)

    :return: one-sided p-value
    """
    df: int = n - 1

    p_value: float = stats.t.cdf(critical, df=df, scale=std, loc=mean)
    if alternative == "less":
        p_value = 1 - p_value
    elif alternative != "greater":
        raise ValueError("alternative must be \"less\" or \"greater\"")
    return p_value


class WorstPopulation:
    @classmethod
    def _worst_dist_std(cls,
                        x: np.ndarray,
                        alpha: float = 0.05) -> float:
        return _intervals.max_std(x=x, alpha=alpha)

    @classmethod
    def _worst_dist_mean(cls,
                         x: np.ndarray,
                         alternative: str = "greater",
                         alpha: float = 0.05) -> float:
        return _intervals.PopulationMean.evaluate(
            x=x,
            alpha=alpha,
            alternative=alternative
        )

    @classmethod
    def critical_level_x_p(cls,
                           x: np.ndarray,
                           critical: float = 0.0,
                           alternative: str = "greater",
                           population_p: float = 0.05) -> float:
        population_mean: float = cls._worst_dist_mean(x=x,
                                                     alternative=alternative,
                                                     alpha=population_p)
        population_std: float = cls._worst_dist_std(x=x, alpha=population_p)

        return critical_level_p(mean=population_mean,
                                std=population_std,
                                n=len(x),
                                critical=critical,
                                alternative=alternative)

    @classmethod
    def mean_t_p(cls,
                 x: np.ndarray,
                 value: float,
                 alternative: str = "greater") -> float:
        return stats.ttest_1samp(x,
                                 popmean=value,
                                 alternative=alternative).pvalue
