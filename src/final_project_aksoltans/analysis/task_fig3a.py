from pathlib import Path

import pandas as pd

from final_project_aksoltans.analysis.fig3a_data import build_fig3a_data
from final_project_aksoltans.config import (
    FIG3A_DATA,
    FOLLOW_BACKS_ANALYSIS,
    SRC,
)


def task_build_fig3a_data(
    script: Path = SRC / "analysis" / "task_fig3a.py",
    data: Path = FOLLOW_BACKS_ANALYSIS,
    produces: Path = FIG3A_DATA,
) -> None:
    """Build and save the aggregated data for Figure 3a.

    Args:
        script: Path to this script, used for pytask dependency tracking.
        data: Path to the cleaned follow-backs parquet file.
        produces: Path where the Figure 3a CSV is saved.
    """
    df = pd.read_parquet(data)
    produces.parent.mkdir(parents=True, exist_ok=True)
    build_fig3a_data(df).to_csv(produces, index=False)
