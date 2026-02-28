from pathlib import Path

import matplotlib.pyplot as plt
import numpy as np
import pandas as pd
from statsmodels.stats.weightstats import DescrStatsW

from final_project_aksoltans.config import (
    FIG2_GENDER_DATA,
    FIG2_PNG,
    FIG2_RACE_DATA,
    FIG2_UNI_DATA,
    FOLLOW_BACKS_ANALYSIS,
    SRC,
)

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


def _plot_one(ax, df: pd.DataFrame, group_col: str, xlabel: str, ylabel: str) -> None:
    df = df.copy()
    df["label"] = df[group_col].map(LABELS[group_col])

    x = range(len(df))
    y = df["pct_flwback"].astype(float).to_numpy()
    yerr_low = (df["pct_flwback"] - df["ciL"]).astype(float).to_numpy()
    yerr_high = (df["ciH"] - df["pct_flwback"]).astype(float).to_numpy()

    ax.bar(x, y, edgecolor="black")
    ax.errorbar(x, y, yerr=[yerr_low, yerr_high], fmt="none", capsize=4)

    ax.set_xticks(list(x))
    ax.set_xticklabels(df["label"].astype(str).tolist())
    ax.set_xlabel(xlabel)
    ax.set_ylabel(ylabel)
    ax.set_ylim(0, 0.245)

    for i, v in enumerate(y):
        ax.text(i, 0.01, f"{v:.3f}", ha="center", va="bottom", fontweight="bold")


def task_plot_fig2_marginals(
    script: Path = SRC / "analysis" / "task_fig2_plot.py",
    data: Path = FOLLOW_BACKS_ANALYSIS,
    produces: Path = FIG2_PNG,
) -> None:
    df = pd.read_parquet(data)
    out_gender = build_marginal(df, "bot_gender")
    out_race = build_marginal(df, "bot_race")
    out_uni = build_marginal(df, "bot_uni")

    produces.parent.mkdir(parents=True, exist_ok=True)
    out_gender.to_csv(FIG2_GENDER_DATA, index=False)
    out_race.to_csv(FIG2_RACE_DATA, index=False)
    out_uni.to_csv(FIG2_UNI_DATA, index=False)

    fig, axes = plt.subplots(1, 3, figsize=(14, 5))
    _plot_one(
        axes[0], out_gender, "bot_gender", "Bot's Gender", "Share of Follow Backs"
    )
    _plot_one(axes[1], out_race, "bot_race", "Bot's Race", "")
    _plot_one(axes[2], out_uni, "bot_uni", "Bot's University Affiliation", "")

    fig.tight_layout()
    fig.savefig(produces, dpi=200)
    plt.close(fig)
