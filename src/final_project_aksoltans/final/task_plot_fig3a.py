from pathlib import Path

import pandas as pd
from matplotlib import pyplot as plt

from final_project_aksoltans.config import FIG3A_DATA, FIG3A_PNG, SRC
from final_project_aksoltans.final.plot_fig3a import plot_fig3a


def task_plot_fig3a(
    script: Path = SRC / "final" / "task_plot_fig3a.py",
    data: Path = FIG3A_DATA,
    produces: Path = FIG3A_PNG,
) -> None:
    df = pd.read_csv(data)
    fig, axes = plt.subplots(1, 2, figsize=(17.72, 5.91), sharey=True)
    plot_fig3a(list(axes), df)
    fig.tight_layout()
    produces.parent.mkdir(parents=True, exist_ok=True)
    fig.savefig(produces, dpi=200)
    plt.close(fig)
