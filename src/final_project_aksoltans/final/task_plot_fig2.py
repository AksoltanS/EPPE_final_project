from pathlib import Path

import matplotlib.pyplot as plt
import pandas as pd

from final_project_aksoltans.config import (
    FIG2_CONTROLS_DATA,
    FIG2_GENDER_DATA,
    FIG2_PNG,
    FIG2_RACE_DATA,
    FIG2_UNI_DATA,
    SRC,
)
from final_project_aksoltans.final.plot_fig2 import plot_controls, plot_marginal


def task_plot_fig2(
    script: Path = SRC / "final" / "task_plot_fig2.py",
    data: tuple[Path, ...] = (
        FIG2_GENDER_DATA,
        FIG2_RACE_DATA,
        FIG2_UNI_DATA,
        FIG2_CONTROLS_DATA,
    ),
    produces: Path = FIG2_PNG,
) -> None:
    """Plot and save Figure 2.

    Args:
        script: Path to this script, used for pytask dependency tracking.
        data: Paths to the gender, race, university, and controls CSV files.
        produces: Path where the Figure 2 PNG is saved.
    """
    gender_df = pd.read_csv(FIG2_GENDER_DATA)
    race_df = pd.read_csv(FIG2_RACE_DATA)
    uni_df = pd.read_csv(FIG2_UNI_DATA)
    ctrl_df = pd.read_csv(FIG2_CONTROLS_DATA)

    fig, axes = plt.subplots(
        1,
        4,
        figsize=(17.72, 5.91),
        gridspec_kw={"width_ratios": [1, 1, 1, 1.1]},
    )
    plot_marginal(
        axes[0], gender_df, "bot_gender", "Bot's Gender", "Share of Follow Backs"
    )
    plot_marginal(axes[1], race_df, "bot_race", "Bot's Race", "")
    plot_marginal(axes[2], uni_df, "bot_uni", "Bot's University Affiliation", "")
    plot_controls(axes[3], ctrl_df)

    fig.tight_layout(rect=(0, 0, 1, 0.93))
    fig.savefig(produces, dpi=200)
    plt.close(fig)
