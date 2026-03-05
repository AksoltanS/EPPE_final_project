from pathlib import Path

import numpy as np
import pandas as pd
from matplotlib import pyplot as plt

from final_project_aksoltans.analysis.fig3a_data import build_fig3a_data
from final_project_aksoltans.config import (
    FIG3A_DATA,
    FIG3A_PNG,
    FOLLOW_BACKS_ANALYSIS,
    SRC,
)


def task_plot_fig3a(
    script: Path = SRC / "analysis" / "task_fig3a_plot.py",
    data: Path = FOLLOW_BACKS_ANALYSIS,
    produces: tuple[Path, Path] = (FIG3A_DATA, FIG3A_PNG),
) -> None:
    produces_csv, produces_png = produces
    df = pd.read_parquet(data)

    plotdf = build_fig3a_data(df)
    for col in ["bot_gender", "bot_race", "bot_uni"]:
        plotdf[col] = pd.to_numeric(plotdf[col], errors="coerce").astype("Int64")

    produces_csv.parent.mkdir(parents=True, exist_ok=True)
    plotdf.to_csv(produces_csv, index=False)

    gender_label = {0: "Male", 1: "Female"}
    race_label = {0: "White", 1: "Black"}
    uni_label = {0: "Lower-Ranked", 1: "Top-Ranked"}

    fig, axes = plt.subplots(1, 2, figsize=(12, 5), sharey=True)

    for ax in axes:
        ax.grid(axis="y", alpha=0.25)
        ax.set_axisbelow(True)

    x_positions = np.array([0, 1], dtype=float)
    width = 0.35
    offsets = {0: -width / 2, 1: width / 2}
    bar_colors = {0: "0.90", 1: "0.55"}
    for ax, gdr in zip(axes, [0, 1], strict=False):
        sub = plotdf[plotdf["bot_gender"] == gdr].copy()

        for race in [0, 1]:
            s = (
                sub[sub["bot_race"] == race]
                .set_index("bot_uni")
                .reindex([0, 1])
                .reset_index()
            )

            y = s["pct_flwback"].to_numpy(dtype=float)
            yerr_low = (s["pct_flwback"] - s["ciL"]).to_numpy(dtype=float)
            yerr_high = (s["ciH"] - s["pct_flwback"]).to_numpy(dtype=float)

            ax.bar(
                x_positions + offsets[race],
                y,
                width=width,
                edgecolor="black",
                color=bar_colors[race],
                label=race_label[race],
                zorder=2,
            )
            ax.errorbar(
                x_positions + offsets[race],
                y,
                yerr=[yerr_low, yerr_high],
                fmt="none",
                capsize=6,
                ecolor="black",
                elinewidth=1.5,
                capthick=1.5,
                zorder=3,
            )

            for i, v in enumerate(y):
                ax.text(
                    x_positions[i] + offsets[race],
                    0.01,
                    f"{v:.3f}",
                    ha="center",
                    va="bottom",
                    fontweight="bold",
                    fontsize=9,
                )

        ax.set_title(f"Bot's Gender: {gender_label[gdr]}")
        ax.set_xticks([0, 1])
        ax.set_xticklabels([uni_label[0], uni_label[1]])
        ax.set_xlabel("Bot's University Affiliation")
        ax.set_ylim(0, 0.30)

    axes[0].set_ylabel("Share of Follow Backs")
    axes[1].legend(title="Bot's Race", loc="center left", bbox_to_anchor=(1.02, 0.5))

    produces_png.parent.mkdir(parents=True, exist_ok=True)
    fig.tight_layout()
    fig.savefig(produces_png, dpi=200)
    plt.close(fig)
