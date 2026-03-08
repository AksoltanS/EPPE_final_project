import numpy as np
import pandas as pd
from matplotlib.axes import Axes

_BAR_COLORS = {0: "#e6e6e6", 1: "#7f7f7f"}

_GENDER_LABEL = {0: "Male", 1: "Female"}
_RACE_LABEL = {0: "White", 1: "Black"}
_UNI_LABEL = {0: "Lower-Ranked", 1: "Top-Ranked"}

_WIDTH = 0.35
_OFFSETS = {0: -_WIDTH / 2, 1: _WIDTH / 2}
_X_POS = np.array([0, 1], dtype=float)


def plot_fig3a(axes: list[Axes], df: pd.DataFrame) -> None:
    for ax in axes:
        ax.grid(axis="y", alpha=0.25)
        ax.set_axisbelow(True)

    for ax, gdr in zip(axes, [0, 1], strict=False):
        sub = df[df["bot_gender"] == gdr].copy()

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
            x_pos = _X_POS + _OFFSETS[race]

            ax.bar(
                x_pos,
                y,
                width=_WIDTH,
                edgecolor="black",
                color=_BAR_COLORS[race],
                label=_RACE_LABEL[race],
                zorder=2,
            )
            ax.errorbar(
                x_pos,
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
                    x_pos[i],
                    0.01,
                    f"{v:.3f}",
                    ha="center",
                    va="bottom",
                    fontweight="bold",
                    fontsize=9,
                )

        ax.set_title(f"Bot's Gender: {_GENDER_LABEL[gdr]}")
        ax.set_xticks([0, 1])
        ax.set_xticklabels([_UNI_LABEL[0], _UNI_LABEL[1]])
        ax.set_xlabel("Bot's University Affiliation")
        ax.set_ylim(0, 0.30)

    axes[0].set_ylabel("Share of Follow Backs")
    axes[1].legend(title="Bot's Race", loc="center left", bbox_to_anchor=(1.02, 0.5))
