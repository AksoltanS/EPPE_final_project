from pathlib import Path

import matplotlib.pyplot as plt
import pandas as pd

from final_project_aksoltans.analysis.fig1_data import build_fig1_data
from final_project_aksoltans.config import (
    FIG1_DATA,
    FIG1_PNG,
    FOLLOW_BACKS_ANALYSIS,
    SRC,
)

TREAT_LABELS = {
    1: "White\nMale\nTop-Ranked",
    2: "White\nMale\nLower-Ranked",
    3: "Black\nMale\nTop-Ranked",
    4: "Black\nMale\nLower-Ranked",
    5: "White\nFemale\nTop-Ranked",
    6: "White\nFemale\nLower-Ranked",
    7: "Black\nFemale\nTop-Ranked",
    8: "Black\nFemale\nLower-Ranked",
}


def task_build_fig1_data(
    script: Path = SRC / "analysis" / "task_fig1.py",
    data: Path = FOLLOW_BACKS_ANALYSIS,
    produces: Path = FIG1_DATA,
) -> None:
    fb = pd.read_parquet(data)
    fig1 = build_fig1_data(fb)

    produces.parent.mkdir(parents=True, exist_ok=True)
    fig1.to_csv(produces, index=False)


def task_plot_fig1(
    script: Path = SRC / "analysis" / "task_fig1.py",
    data: Path = FIG1_DATA,
    produces: Path = FIG1_PNG,
) -> None:
    df = pd.read_csv(data).copy()

    df["treat"] = pd.to_numeric(df["treat"], errors="coerce").astype("Int64")
    df["pct_flwback"] = pd.to_numeric(df["pct_flwback"], errors="coerce")
    df["ciL"] = pd.to_numeric(df["ciL"], errors="coerce")
    df["ciH"] = pd.to_numeric(df["ciH"], errors="coerce")

    df["label"] = df["treat"].map(TREAT_LABELS)
    df = df.sort_values("pct_flwback").reset_index(drop=True)

    x = range(len(df))
    y = df["pct_flwback"].to_numpy()
    yerr_low = (df["pct_flwback"] - df["ciL"]).to_numpy()
    yerr_high = (df["ciH"] - df["pct_flwback"]).to_numpy()

    produces.parent.mkdir(parents=True, exist_ok=True)

    fig, ax = plt.subplots(figsize=(12, 6))
    ax.bar(x, y, edgecolor="black")
    ax.errorbar(x, y, yerr=[yerr_low, yerr_high], fmt="none", capsize=4)

    ax.set_ylabel("Share of Follow Backs")
    ax.set_xticks([])
    ax.set_ylim(0, 0.30)

    labels = df["label"].astype(str).to_numpy()
    vals = df["pct_flwback"].astype(float).to_numpy()

    for i, (lab, v) in enumerate(zip(labels, vals, strict=False)):
        ax.text(i, v / 2, lab, ha="center", va="center", fontweight="bold")
        ax.text(i, 0.01, f"{v:.3f}", ha="center", va="bottom", fontweight="bold")

    fig.tight_layout()
    fig.savefig(produces, dpi=200)
    plt.close(fig)
