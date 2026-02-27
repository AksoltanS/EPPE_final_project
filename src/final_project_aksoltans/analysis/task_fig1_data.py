from pathlib import Path

import pandas as pd

from final_project_aksoltans.analysis.fig1_data import build_fig1_data
from final_project_aksoltans.config import FIG1_DATA, FOLLOW_BACKS_ANALYSIS, SRC


def task_build_fig1_data(
    script: Path = SRC / "analysis" / "task_fig1_data.py",
    data: Path = FOLLOW_BACKS_ANALYSIS,
    produces: Path = FIG1_DATA,
) -> None:
    fb = pd.read_parquet(data)
    fig1 = build_fig1_data(fb)

    produces.parent.mkdir(parents=True, exist_ok=True)
    fig1.to_csv(produces, index=False)
