import pandas as pd
from matplotlib.axes import Axes
from matplotlib.lines import Line2D

from final_project_aksoltans.config import PVAL_DISPLAY_THRESHOLD


def plot_bars_with_ci(
    ax: Axes,
    df: pd.DataFrame,
    y_col: str,
    ci_low_col: str,
    ci_high_col: str,
    *,
    x_labels: list[str] | None = None,
    ylim: tuple[float, float] | None = None,
    show_value_labels: bool = True,
    bar_color: str = "#e6e6e6",
    edge_color: str = "black",
    width: float = 0.9,
    capsize: float = 6,
) -> None:
    x = range(len(df))
    y = df[y_col].to_numpy(dtype=float)
    yerr_low = (df[y_col] - df[ci_low_col]).to_numpy(dtype=float)
    yerr_high = (df[ci_high_col] - df[y_col]).to_numpy(dtype=float)
    ax.grid(axis="y", alpha=0.25)
    ax.set_axisbelow(True)
    ax.bar(x, y, edgecolor=edge_color, width=width, color=bar_color, zorder=2)
    ax.errorbar(
        x,
        y,
        yerr=[yerr_low, yerr_high],
        fmt="none",
        capsize=capsize,
        ecolor="black",
        elinewidth=1.5,
        capthick=1.5,
        zorder=3,
    )

    if show_value_labels:
        for i, v in enumerate(y):
            ax.text(i, 0.01, f"{v:.3f}", ha="center", va="bottom", fontweight="bold")

    if x_labels is not None:
        ax.set_xticks(list(x))
        ax.set_xticklabels(x_labels)

    if ylim is not None:
        ax.set_ylim(*ylim)


# plot for fig2 controls
def plot_forest(
    ax: Axes,
    df: pd.DataFrame,
    dims: list[str],
    dim_labels: dict[str, str],
    series: dict[str, dict],
    legend_title: str,
    xlim: tuple[float, float],
    ylim: tuple[float, float],
    grey_band_rows: tuple[float, float] = (0.5, 1.5),
    dim_col: str = "dim",
    x_col: str = "x",
    est_col: str = "fb",
    ci_low_col: str = "CIlow",
    ci_high_col: str = "CIhigh",
    pval_col: str = "pval",
) -> None:
    dim_to_y = {d: i for i, d in enumerate(dims)}
    ax.axhspan(*grey_band_rows, color="grey", alpha=0.12, zorder=0)
    ax.axvline(0, linestyle="--", color="black", linewidth=0.8, zorder=1)

    for x_val, cfg in series.items():
        sub = df[df[x_col] == x_val].copy()
        sub["_y"] = sub[dim_col].map(dim_to_y) + cfg["dodge"]
        xv = sub[est_col].to_numpy(dtype=float)
        xl = sub[ci_low_col].to_numpy(dtype=float)
        xh = sub[ci_high_col].to_numpy(dtype=float)
        yv = sub["_y"].to_numpy(dtype=float)
        pv = sub[pval_col].to_numpy(dtype=float)
        c, m = cfg["color"], cfg["marker"]

        ax.errorbar(
            xv,
            yv,
            xerr=[xv - xl, xh - xv],
            fmt="none",
            ecolor=c,
            elinewidth=0.9,
            capsize=2.5,
            capthick=0.9,
            zorder=2,
        )
        ax.scatter(xv, yv, marker=m, color=c, s=40, linewidths=1.5, zorder=3)

        y_off = +0.05 if cfg["annot_above"] else -0.05
        va = "bottom" if cfg["annot_above"] else "top"
        for xi, yi, pvi in zip(xv, yv, pv, strict=False):
            p_str = (
                "<{PVAL_DISPLAY_THRESHOLD}"
                if pvi < PVAL_DISPLAY_THRESHOLD
                else f"{pvi:.3f}"
            )
            ax.text(
                xi,
                yi + y_off,
                f"{xi:.3f}\n[{p_str}]",
                ha="center",
                va=va,
                fontsize=6.5,
                fontweight="bold",
                color=c,
                linespacing=0.85,
            )

    ax.set_yticks(range(len(dims)))
    ax.set_yticklabels([dim_labels[d] for d in dims], fontsize=8.5)
    ax.yaxis.set_tick_params(length=0)
    ax.set_xlim(*xlim)
    ax.set_ylim(*ylim)
    ax.set_xlabel("Share of Follow Backs", fontsize=9)
    ax.tick_params(axis="x", labelsize=8)
    ax.grid(axis="x", alpha=0.25, linewidth=0.6)
    ax.set_axisbelow(True)
    ax.yaxis.grid(visible=False)

    handles = [
        Line2D(
            [0],
            [0],
            marker=cfg["marker"],
            color=cfg["color"],
            linestyle="none",
            markersize=6,
            markeredgewidth=1.5,
            label=cfg["label"],
        )
        for cfg in series.values()
    ]
    ax.legend(
        handles=handles,
        title=legend_title,
        loc="lower center",
        bbox_to_anchor=(0.5, 1.01),
        ncol=len(series),
        fontsize=8,
        title_fontsize=8,
        frameon=False,
        handletextpad=0.3,
        columnspacing=0.5,
    )
