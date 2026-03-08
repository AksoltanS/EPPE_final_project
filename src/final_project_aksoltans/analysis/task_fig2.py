from pathlib import Path

import matplotlib.pyplot as plt
import pandas as pd

from final_project_aksoltans.analysis.fig2_data import (
    build_fig2_controls_data,
    build_fig2_marginals,
)
from final_project_aksoltans.analysis.plot_fig2 import plot_controls, plot_marginal
from final_project_aksoltans.config import (
    FIG2_CONTROLS_DATA,
    FIG2_GENDER_DATA,
    FIG2_PNG,
    FIG2_RACE_DATA,
    FIG2_UNI_DATA,
    FOLLOW_BACKS_ANALYSIS,
    SRC,
)


def task_build_fig2_data(
    script: Path = SRC / "analysis" / "task_fig2.py",
    data: Path = FOLLOW_BACKS_ANALYSIS,
    produces: tuple[Path, ...] = (
        FIG2_GENDER_DATA,
        FIG2_RACE_DATA,
        FIG2_UNI_DATA,
        FIG2_CONTROLS_DATA,
    ),
) -> None:
    fb = pd.read_parquet(data)

    for key, path in zip(
        ["bot_gender", "bot_race", "bot_uni"],
        [FIG2_GENDER_DATA, FIG2_RACE_DATA, FIG2_UNI_DATA],
        strict=False,
    ):
        path.parent.mkdir(parents=True, exist_ok=True)
        build_fig2_marginals(fb)[key].to_csv(path, index=False)

    FIG2_CONTROLS_DATA.parent.mkdir(parents=True, exist_ok=True)
    build_fig2_controls_data(fb).to_csv(FIG2_CONTROLS_DATA, index=False)


def task_plot_fig2(
    script: Path = SRC / "analysis" / "task_fig2.py",
    data: tuple[Path, ...] = (
        FIG2_GENDER_DATA,
        FIG2_RACE_DATA,
        FIG2_UNI_DATA,
        FIG2_CONTROLS_DATA,
    ),
    produces: Path = FIG2_PNG,
) -> None:
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
    produces.parent.mkdir(parents=True, exist_ok=True)
    fig.savefig(produces, dpi=200)
    plt.close(fig)
