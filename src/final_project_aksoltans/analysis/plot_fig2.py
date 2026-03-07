import pandas as pd
from matplotlib.axes import Axes
from matplotlib.lines import Line2D

from final_project_aksoltans.analysis.plot_utils import (
    PVAL_THRESHOLD,
    plot_bars_with_ci,
)

_LABELS = {
    "bot_gender": {0: "Male", 1: "Female"},
    "bot_race": {0: "White", 1: "Black"},
    "bot_uni": {0: "Lower-Ranked", 1: "Top-Ranked"},
}
_COLORS = {"Yes": "steelblue", "No": "darkred"}
_MARKERS = {"Yes": "x", "No": "o"}
_DODGE = 0.08


def _fmt_p(p: float) -> str:
    return f"<{PVAL_THRESHOLD:.3f}" if p < PVAL_THRESHOLD else f"{round(p, 3):.3f}"


def plot_marginal(
    ax: Axes, df: pd.DataFrame, group_col: str, xlabel: str, ylabel: str
) -> None:
    df = df.copy()
    df["label"] = df[group_col].map(_LABELS[group_col])
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


def plot_controls(ax: Axes, df: pd.DataFrame) -> None:
    coef_order = ["bot_uni", "bot_race", "bot_gender"]
    coef_to_y = {c: i for i, c in enumerate(coef_order)}
    coef_labels = {
        "bot_gender": "Bot's Gender\n(1=Female)",
        "bot_race": "Bot's Race\n(1=Black)",
        "bot_uni": "Bot's University\nAffiliation\n(1=Top-ranked)",
    }

    ax.axhspan(0.5, 1.5, color="grey", alpha=0.12, zorder=0)
    ax.axvline(0, linestyle="--", color="black", linewidth=0.8, zorder=1)

    for label, offset in [("Yes", _DODGE), ("No", -_DODGE)]:
        sub = df[df["controls"] == label].copy()
        sub["y_pos"] = sub["coef"].map(coef_to_y)
        sub = sub.dropna(subset=["y_pos"])

        y = sub["y_pos"].to_numpy(dtype=float) + offset
        x = sub["Estimate"].to_numpy(dtype=float)
        xl = sub["ciL"].to_numpy(dtype=float)
        xh = sub["ciH"].to_numpy(dtype=float)
        pv = sub["pval"].to_numpy(dtype=float)

        ax.errorbar(
            x,
            y,
            xerr=[x - xl, xh - x],
            fmt="none",
            ecolor=_COLORS[label],
            elinewidth=0.9,
            capsize=2.5,
            capthick=0.9,
            zorder=2,
        )
        ax.scatter(
            x,
            y,
            marker=_MARKERS[label],
            color=_COLORS[label],
            s=35,
            linewidths=1.5,
            zorder=3,
        )

        va = "bottom" if label == "Yes" else "top"
        y_off = +0.02 if label == "Yes" else -0.02
        for xi, yi, pvi in zip(x, y, pv, strict=False):
            ax.text(
                xi,
                yi + y_off,
                f"{xi:.3f}\n[{_fmt_p(pvi)}]",
                ha="center",
                va=va,
                fontsize=6.5,
                fontweight="bold",
                color=_COLORS[label],
                linespacing=0.85,
            )

    ax.set_yticks(range(len(coef_order)))
    ax.set_yticklabels(
        [coef_labels[c] for c in coef_order], fontsize=8, va="center", ha="right"
    )
    ax.yaxis.set_tick_params(length=0)
    ax.set_ylim(-0.55, 2.75)
    ax.set_xlim(-0.07, 0.07)
    ax.set_xlabel("Share of Follow Backs", fontsize=9)
    ax.set_ylabel("")
    ax.tick_params(axis="x", labelsize=8)
    ax.grid(axis="x", alpha=0.25, linewidth=0.6)
    ax.set_axisbelow(True)
    ax.yaxis.grid(visible=False)

    ax.legend(
        handles=[
            Line2D(
                [0],
                [0],
                marker="x",
                color=_COLORS["Yes"],
                linestyle="none",
                markersize=6,
                markeredgewidth=1.8,
                label="Yes",
            ),
            Line2D(
                [0],
                [0],
                marker="o",
                color=_COLORS["No"],
                linestyle="none",
                markersize=6,
                label="No",
            ),
        ],
        title="Controls",
        loc="lower center",
        bbox_to_anchor=(0.5, 1.01),
        ncol=3,
        fontsize=8,
        title_fontsize=8,
        frameon=False,
        handletextpad=0.3,
        columnspacing=0.6,
    )
