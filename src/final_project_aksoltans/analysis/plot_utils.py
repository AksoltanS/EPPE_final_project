import pandas as pd
from matplotlib.axes import Axes


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
) -> None:
    x = range(len(df))
    y = df[y_col].to_numpy(dtype=float)

    yerr_low = (df[y_col] - df[ci_low_col]).to_numpy(dtype=float)
    yerr_high = (df[ci_high_col] - df[y_col]).to_numpy(dtype=float)

    ax.bar(x, y, edgecolor="black")
    ax.errorbar(x, y, yerr=[yerr_low, yerr_high], fmt="none", capsize=4)

    if show_value_labels:
        for i, v in enumerate(y):
            ax.text(i, 0.01, f"{v:.3f}", ha="center", va="bottom", fontweight="bold")

    if x_labels is not None:
        ax.set_xticks(list(x))
        ax.set_xticklabels(x_labels)

    if ylim is not None:
        ax.set_ylim(*ylim)
