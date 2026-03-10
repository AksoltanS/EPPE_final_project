import numpy as np
import pandas as pd
from scipy import stats

from final_project_aksoltans.analysis.fe_ols import fe_ols

_CENTRE_COLS = [
    "above_median_year_created",
    "background_pic",
    "above_median_followers_count",
    "above_median_friends_count",
]
_DIMS = ["bot_gender", "bot_race"]


def build_fig3b_data(fb: pd.DataFrame, alpha: float = 0.05) -> pd.DataFrame:
    """Estimate heterogeneity in bot_uni effect by gender and race for Figure 3b.

    Centers continuous controls, constructs bot_uni interaction terms, runs
    FE-OLS, and returns main effects and interaction estimates with confidence
    intervals.

    Args:
        fb: Cleaned follow-backs DataFrame.
        alpha: Significance level for confidence intervals.

    Returns:
        DataFrame with one row per dimension and level (0, 1, int).
    """
    df = fb.copy()
    centre_cols = [c for c in _CENTRE_COLS if c in df.columns]
    df[centre_cols] = df[centre_cols].astype(float) - df[centre_cols].mean()
    interact = {b: f"bot_uni_x_{b}" for b in _DIMS}
    for b, iv in interact.items():
        df[iv] = df["bot_uni"].astype(float) * df[b].astype(float)

    dummy_cols: list[str] = []
    for col in ("continent", "profession", "female"):
        dummies = pd.get_dummies(df[col], prefix=col, drop_first=True, dtype=float)
        for c in dummies.columns:
            df[c] = dummies[c]
        dummy_cols += list(dummies.columns)

    regs = [
        "bot_gender",
        "bot_race",
        "bot_uni",
        interact["bot_gender"],
        interact["bot_race"],
        *dummy_cols,
        *centre_cols,
    ]

    res, vcov, g_clusters = fe_ols(df, y="FollowBacks", regressors=regs)
    idx = {name: i for i, name in enumerate(regs)}
    t_crit = stats.t.ppf(1 - alpha / 2, df=g_clusters - 1)

    def _row(dim, x_label, est, se):
        """Build a result row with estimate, CI bounds, and p-value."""
        t = est / se if se > 0 else np.nan
        p = float(2 * (1 - stats.t.cdf(abs(t), df=g_clusters - 1)))
        return {
            "dim": dim,
            "x": x_label,
            "fb": est,
            "CIlow": est - t_crit * se,
            "CIhigh": est + t_crit * se,
            "pval": p,
        }

    rows = []
    for b in _DIMS:
        iv = interact[b]
        ib, ii = idx[b], idx[iv]
        b0 = res[b]["estimate"]
        b_int = res[iv]["estimate"]
        se_b0 = (res[b]["ci_high"] - res[b]["ci_low"]) / (2 * t_crit)
        se_int = (res[iv]["ci_high"] - res[iv]["ci_low"]) / (2 * t_crit)
        se_b1 = float(np.sqrt(max(vcov[ib, ib] + vcov[ii, ii] + 2 * vcov[ib, ii], 0.0)))
        rows += [
            _row(b, "0", b0, se_b0),
            _row(b, "1", b0 + b_int, se_b1),
            _row(b, "int", b_int, se_int),
        ]

    return pd.DataFrame(rows)
