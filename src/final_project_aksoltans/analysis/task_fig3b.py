from pathlib import Path

import matplotlib.pyplot as plt
import pandas as pd

from final_project_aksoltans.analysis.fig3b_data import build_fig3b_data
from final_project_aksoltans.analysis.plot_fig3b import plot_fig3b
from final_project_aksoltans.config import (
    FIG3B_DATA,
    FIG3B_PNG,
    FOLLOW_BACKS_ANALYSIS,
    SRC,
)


def task_build_fig3b_data(
    script: Path = SRC / "analysis" / "task_fig3b.py",
    data: Path = FOLLOW_BACKS_ANALYSIS,
    produces: Path = FIG3B_DATA,
) -> None:
    fb = pd.read_parquet(data)
    produces.parent.mkdir(parents=True, exist_ok=True)
    build_fig3b_data(fb).to_csv(produces, index=False)


def task_plot_fig3b(
    script: Path = SRC / "analysis" / "task_fig3b.py",
    data: Path = FIG3B_DATA,
    produces: Path = FIG3B_PNG,
) -> None:
    df = pd.read_csv(data)
    fig, ax = plt.subplots(figsize=(9.84, 6.5))
    plot_fig3b(ax, df)
    fig.tight_layout(rect=(0, 0, 1, 0.88))
    produces.parent.mkdir(parents=True, exist_ok=True)
    fig.savefig(produces, dpi=200)
    plt.close(fig)
