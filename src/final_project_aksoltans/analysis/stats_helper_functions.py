import numpy as np
import pandas as pd
from statsmodels.stats.weightstats import DescrStatsW

_MIN_GROUP_SIZE = 2


def aggregate_experimental_data(
    df: pd.DataFrame,
    group_cols: list[str],
    *,
    value_col: str = "FollowBacks",
    out_col: str = "pct_flwback",
) -> pd.DataFrame:
    """Aggregate follow-back rates and confidence intervals by group.

    Args:
        df: Analysis DataFrame.
        group_cols: Columns to group by.
        value_col: Column containing the outcome values.
        out_col: Name of the mean column in the output.

    Returns:
        DataFrame with one row per group containing out_col, ciL, and ciH.
    """
    rows: list[dict[str, object]] = []
    for keys, g in df.groupby(group_cols, sort=True):
        key_tuple = keys if isinstance(keys, tuple) else (keys,)
        mean, ci_low, ci_high = _mean_ci_t(g[value_col])
        row: dict[str, object] = {col: key_tuple[i] for i, col in enumerate(group_cols)}
        row[out_col] = mean
        row["ciL"] = ci_low
        row["ciH"] = ci_high
        rows.append(row)
    return pd.DataFrame(rows).reset_index(drop=True)


def _mean_ci_t(x: pd.Series, alpha: float = 0.05) -> tuple[float, float, float]:
    """Return the mean and t-based confidence interval for a series.

    Falls back to NaN bounds when the group has fewer than
    _MIN_GROUP_SIZE observations.

    Args:
       x: Numeric series to summarise.
       alpha: Significance level for the confidence interval.

    Returns:
      Tuple of (mean, ci_low, ci_high).
    """
    mean = float(x.mean())
    if x.size < _MIN_GROUP_SIZE:
        return mean, np.nan, np.nan
    ci_low, ci_high = DescrStatsW(x).tconfint_mean(alpha=alpha)
    return mean, float(ci_low), float(ci_high)
