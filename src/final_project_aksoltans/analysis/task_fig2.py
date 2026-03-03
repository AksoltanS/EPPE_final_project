from pathlib import Path

import matplotlib.pyplot as plt
import pandas as pd

from final_project_aksoltans.analysis.fig2_data import build_fig2_marginals
from final_project_aksoltans.analysis.plot_utils import plot_bars_with_ci
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


def _plot_one(ax, df: pd.DataFrame, group_col: str, xlabel: str, ylabel: str) -> None:
    df = df.copy()
    df["label"] = df[group_col].map(LABELS[group_col])

    plot_bars_with_ci(
        ax=ax,
        df=df,
        y_col="pct_flwback",
        ci_low_col="ciL",
        ci_high_col="ciH",
        x_labels=df["label"].astype(str).tolist(),
        ylim=(0, 0.245),
        show_value_labels=True,
    )

    ax.set_xlabel(xlabel)
    ax.set_ylabel(ylabel)


def task_plot_fig2_marginals(
    script: Path = SRC / "analysis" / "task_fig2.py",
    data: Path = FOLLOW_BACKS_ANALYSIS,
    produces: Path = FIG2_PNG,
) -> None:
    df = pd.read_parquet(data)
    outs = build_fig2_marginals(df)

    produces.parent.mkdir(parents=True, exist_ok=True)
    outs["bot_gender"].to_csv(FIG2_GENDER_DATA, index=False)
    outs["bot_race"].to_csv(FIG2_RACE_DATA, index=False)
    outs["bot_uni"].to_csv(FIG2_UNI_DATA, index=False)

    fig, axes = plt.subplots(1, 3, figsize=(14, 5))
    _plot_one(
        axes[0],
        outs["bot_gender"],
        "bot_gender",
        "Bot's Gender",
        "Share of Follow Backs",
    )
    _plot_one(axes[1], outs["bot_race"], "bot_race", "Bot's Race", "")
    _plot_one(
        axes[2],
        outs["bot_uni"],
        "bot_uni",
        "Bot's University Affiliation",
        "",
    )

    fig.tight_layout()
    fig.savefig(produces, dpi=200)
    plt.close(fig)
