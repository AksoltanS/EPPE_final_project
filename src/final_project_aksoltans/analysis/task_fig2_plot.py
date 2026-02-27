import numpy as np
import pandas as pd
from statsmodels.stats.weightstats import DescrStatsW

LABELS = {
    "bot_gender": {0: "Male", 1: "Female"},
    "bot_race": {0: "White", 1: "Black"},
    "bot_uni": {0: "Lower-Ranked", 1: "Top-Ranked"},
}


def mean_ci_t(x: pd.Series, alpha: float = 0.05) -> tuple[float, float, float]:
    mean = float(x.mean())
    min_n = 2
    if x.size < min_n:
        return mean, np.nan, np.nan
    ci_low, ci_high = DescrStatsW(x).tconfint_mean(alpha=alpha)
    return mean, float(ci_low), float(ci_high)


def build_marginal(df: pd.DataFrame, group_col: str) -> pd.DataFrame:
    rows: list[dict[str, float | int]] = []
    for val, g in df.groupby(group_col, sort=True):
        mean, ci_low, ci_high = mean_ci_t(g["FollowBacks"])
        rows.append(
            {
                group_col: int(pd.to_numeric(val)),
                "pct_flwback": mean,
                "ciL": ci_low,
                "ciH": ci_high,
            }
        )
    return pd.DataFrame(rows).sort_values(group_col).reset_index(drop=True)
