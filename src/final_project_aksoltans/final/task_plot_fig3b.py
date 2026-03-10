from pathlib import Path

import matplotlib.pyplot as plt
import pandas as pd

from final_project_aksoltans.config import FIG3B_DATA, FIG3B_PNG, SRC
from final_project_aksoltans.final.plot_fig3b import plot_fig3b


def task_plot_fig3b(
    script: Path = SRC / "final" / "task_plot_fig3b.py",
    data: Path = FIG3B_DATA,
    produces: Path = FIG3B_PNG,
) -> None:
    """Plot and save Figure 3b.

    Args:
        script: Path to this script, used for pytask dependency tracking.
        data:data: Path to the Figure 3b CSV file.
        produces: Path where the Figure 3b PNG is saved.
    """
    df = pd.read_csv(data)
    fig, ax = plt.subplots(figsize=(9.84, 6.5))
    plot_fig3b(ax, df)
    fig.tight_layout(rect=(0, 0, 1, 0.88))
    produces.parent.mkdir(parents=True, exist_ok=True)
    fig.savefig(produces, dpi=200)
    plt.close(fig)
