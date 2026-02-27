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


def build_fig1_data(fb: pd.DataFrame) -> pd.DataFrame:
    rows = []
    for treat, g in fb.groupby("treat", sort=True):
        mean, ci_low, ci_high = mean_ci_t(g["FollowBacks"])
        rows.append(
            {
                "treat": int(pd.to_numeric(treat)),
                "pct_flwback": mean,
                "ciL": ci_low,
                "ciH": ci_high,
            }
        )
    return pd.DataFrame(rows).sort_values("treat").reset_index(drop=True)
