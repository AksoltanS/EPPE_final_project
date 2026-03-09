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
    df = pd.read_csv(data)
    fig = plot_fig1(df)
    produces.parent.mkdir(parents=True, exist_ok=True)
    fig.savefig(produces, dpi=200)
    plt.close(fig)
