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


def aggregate_experimental_data(
    df: pd.DataFrame,
    group_cols: list[str],
    *,
    value_col: str = "FollowBacks",
    out_col: str = "pct_flwback",
) -> pd.DataFrame:
    rows: list[dict[str, object]] = []
    for keys, g in df.groupby(group_cols, sort=True):
        key_tuple = keys if isinstance(keys, tuple) else (keys,)
        mean, ci_low, ci_high = mean_ci_t(g[value_col])
        row: dict[str, object] = {col: key_tuple[i] for i, col in enumerate(group_cols)}
        row[out_col] = mean
        row["ciL"] = ci_low
        row["ciH"] = ci_high
        rows.append(row)
    return pd.DataFrame(rows).reset_index(drop=True)
