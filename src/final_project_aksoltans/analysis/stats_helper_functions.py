import numpy as np
import pandas as pd
from statsmodels.stats.weightstats import DescrStatsW


def mean_ci_t(x: pd.Series, alpha: float = 0.05) -> tuple[float, float, float]:
    mean = float(x.mean())
    min_n = 2
    if x.size < min_n:
        return mean, np.nan, np.nan
    ci_low, ci_high = DescrStatsW(x).tconfint_mean(alpha=alpha)
    return mean, float(ci_low), float(ci_high)
