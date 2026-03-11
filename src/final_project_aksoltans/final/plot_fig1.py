import matplotlib.pyplot as plt
import pandas as pd
from matplotlib.figure import Figure

from final_project_aksoltans.final.plot_utils import plot_bars_with_ci

_TREAT_LABELS = {
    1: "White\nMale\nTop-Ranked",
    2: "White\nMale\nLower-Ranked",
    3: "Black\nMale\nTop-Ranked",
    4: "Black\nMale\nLower-Ranked",
    5: "White\nFemale\nTop-Ranked",
    6: "White\nFemale\nLower-Ranked",
    7: "Black\nFemale\nTop-Ranked",
    8: "Black\nFemale\nLower-Ranked",
}


def plot_fig1(df: pd.DataFrame) -> Figure:
    """Plot follow-back rates by treatment group for Figure 1.

    Args:
        df: Aggregated Figure 1 data from 'build_fig1_data'.

    Returns:
        Matplotlib figure with bars sorted by follow-back rate.
    """
    df = df.copy()
    df["treat"] = pd.to_numeric(df["treat"], errors="coerce").astype("Int64")
    df["label"] = df["treat"].map(_TREAT_LABELS)
    df = df.sort_values("pct_flwback").reset_index(drop=True)

    fig, ax = plt.subplots(figsize=(12, 6))
    plot_bars_with_ci(
        ax=ax,
        df=df,
        y_col="pct_flwback",
        ci_low_col="ciL",
        ci_high_col="ciH",
        ylim=(0, 0.30),
        show_value_labels=True,
    )
    ax.set_ylabel("Share of Follow Backs")
    ax.set_xticks([])

    labels = df["label"].astype(str).to_numpy()
    vals = df["pct_flwback"].astype(float).to_numpy()
    for i, (lab, v) in enumerate(zip(labels, vals, strict=False)):
        ax.text(i, v / 2, lab, ha="center", va="center", fontweight="bold")

    fig.tight_layout()
    return fig
