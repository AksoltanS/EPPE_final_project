import pandas as pd
from matplotlib.axes import Axes

from final_project_aksoltans.final.plot_utils import plot_forest

_DIMS = ["bot_race", "bot_gender"]
_DIM_LABELS = {
    "bot_gender": "Bot's Gender\n(1=Female)",
    "bot_race": "Bot's Race\n(1=Black)",
}
_SERIES = {
    "0": {
        "label": "Lower-Ranked",
        "color": "steelblue",
        "marker": "x",
        "dodge": 0.18,
        "annot_above": True,
    },
    "1": {
        "label": "Top-Ranked",
        "color": "darkred",
        "marker": "o",
        "dodge": 0.00,
        "annot_above": True,
    },
    "int": {
        "label": "Difference (Top-Lower)",
        "color": "black",
        "marker": "P",
        "dodge": -0.18,
        "annot_above": False,
    },
}


def plot_fig3b(ax: Axes, df: pd.DataFrame) -> None:
    """Plot heterogeneity in bot_uni effect by gender and race for Figure 3b.

    Args:
        ax: Axes to draw on.
        df: Estimates data from 'build_fig3b_data'.
    """
    plot_forest(
        ax=ax,
        df=df,
        dims=_DIMS,
        dim_labels=_DIM_LABELS,
        series=_SERIES,
        legend_title="Bot's University Affiliation",
        xlim=(-0.09, 0.09),
        ylim=(-0.6, 1.9),
        grey_band_rows=(0.5, 1.5),
    )
