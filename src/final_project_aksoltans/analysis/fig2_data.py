import pandas as pd

from final_project_aksoltans.analysis.fe_ols import fe_ols
from final_project_aksoltans.analysis.stats_helper_functions import (
    aggregate_experimental_data,
)
from final_project_aksoltans.config import BOT_VARS, CONTROLS_CONTINUOUS


def build_fig2_marginals(df: pd.DataFrame) -> dict[str, pd.DataFrame]:
    """Aggregate follow-backs by each bot variable for Figure 2 marginal plots.

    Args:
        df: Cleaned follow-backs DataFrame.

    Returns:
        Mapping each bot variable to a sorted aggregated DataFrame.
    """
    return {
        col: aggregate_experimental_data(df, [col])
        .sort_values(col)
        .reset_index(drop=True)
        for col in BOT_VARS
    }


def _regressors(df: pd.DataFrame, *, controls: bool) -> tuple[pd.DataFrame, list[str]]:
    """Return the DataFrame and regressor list, optionally with controls."""
    if not controls:
        return df, BOT_VARS

    df = df.copy()
    dummy_cols: list[str] = []
    for col in ("continent", "profession", "female"):
        dummies = pd.get_dummies(df[col], prefix=col, drop_first=True, dtype=float)
        for c in dummies.columns:
            df[c] = dummies[c]
        dummy_cols += list(dummies.columns)

    continuous = [c for c in CONTROLS_CONTINUOUS if c in df.columns]
    return df, BOT_VARS + dummy_cols + continuous


def build_fig2_controls_data(df: pd.DataFrame) -> pd.DataFrame:
    """Run FE-OLS with and without controls, returning estimates for each bot variable.

    Args:
        df: Cleaned follow-backs DataFrame.

    Returns:
        DataFrame with one row per bot variable and control specification.
    """
    rows = []
    for controls in (False, True):
        df, regs = _regressors(df.copy(), controls=controls)
        res, *_ = fe_ols(df, y="FollowBacks", regressors=regs)
        label = "Yes" if controls else "No"
        for coef in BOT_VARS:
            r = res[coef]
            rows.append(
                {
                    "coef": coef,
                    "controls": label,
                    "Estimate": r["estimate"],
                    "pval": r["pval"],
                    "ciL": r["ci_low"],
                    "ciH": r["ci_high"],
                }
            )
    return pd.DataFrame(rows)
