from pathlib import Path

import pandas as pd

from final_project_aksoltans.analysis.fig3b_data import build_fig3b_data
from final_project_aksoltans.config import (
    FIG3B_DATA,
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
