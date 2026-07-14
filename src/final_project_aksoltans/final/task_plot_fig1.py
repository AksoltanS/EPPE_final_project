from pathlib import Path

import matplotlib.pyplot as plt
import pandas as pd

from final_project_aksoltans.config import FIG1_DATA, FIG1_PNG, SRC
from final_project_aksoltans.final.plot_fig1 import plot_fig1


def task_plot_fig1(
    script: Path = SRC / "final" / "task_plot_fig1.py",
    data: Path = FIG1_DATA,
    produces: Path = FIG1_PNG,
) -> None:
    """Plot and save Figure 1.

    Args:
        script: Path to this script, used for pytask dependency tracking.
        data: Path to the Figure 1 CSV file.
        produces: Path where the Figure 1 PNG is saved.
    """
    df = pd.read_csv(data)
    fig = plot_fig1(df)
    fig.savefig(produces, dpi=200)
    plt.close(fig)
