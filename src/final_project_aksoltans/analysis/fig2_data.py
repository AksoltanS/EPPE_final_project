import pandas as pd

from final_project_aksoltans.analysis.fe_ols import fe_ols
from final_project_aksoltans.analysis.stats_helper_functions import (
    aggregate_experimental_data,
)

_BOT_VARS = ["bot_gender", "bot_race", "bot_uni"]
_CONTROLS = [
    "above_median_year_created",
    "follow_diversity",
    "background_pic",
    "above_median_followers_count",
    "above_median_friends_count",
]


def build_fig2_marginals(df: pd.DataFrame) -> dict[str, pd.DataFrame]:
    return {
        col: aggregate_experimental_data(df, [col])
        .sort_values(col)
        .reset_index(drop=True)
        for col in _BOT_VARS
    }


def _regressors(df: pd.DataFrame, *, controls: bool) -> tuple[pd.DataFrame, list[str]]:
    if not controls:
        return df, _BOT_VARS

    df = df.copy()
    dummy_cols: list[str] = []
    for col in ("continent", "profession", "female"):
        dummies = pd.get_dummies(df[col], prefix=col, drop_first=True, dtype=float)
        for c in dummies.columns:
            df[c] = dummies[c]
        dummy_cols += list(dummies.columns)

    continuous = [c for c in _CONTROLS if c in df.columns]
    return df, _BOT_VARS + dummy_cols + continuous


def build_fig2_controls_data(fb: pd.DataFrame) -> pd.DataFrame:
    rows = []
    for controls in (False, True):
        df, regs = _regressors(fb.copy(), controls=controls)
        res, *_ = fe_ols(df, y="FollowBacks", regressors=regs)
        label = "Yes" if controls else "No"
        for coef in _BOT_VARS:
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
