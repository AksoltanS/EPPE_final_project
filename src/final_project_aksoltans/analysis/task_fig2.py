from pathlib import Path

import pandas as pd

from final_project_aksoltans.analysis.fig2_data import (
    build_fig2_controls_data,
    build_fig2_marginals,
)
from final_project_aksoltans.config import (
    BOT_VARS,
    FIG2_CONTROLS_DATA,
    FIG2_GENDER_DATA,
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
    """Build and save the aggregated data for Figure 2.

    Args:
        script: Path to this script, used for pytask dependency tracking.
        data: Path to the cleaned follow-backs parquet file.
        produces: Tuple of paths where the Figure 2 CSV files are saved.
    """
    df = pd.read_parquet(data)

    for key, path in zip(
        BOT_VARS,
        [FIG2_GENDER_DATA, FIG2_RACE_DATA, FIG2_UNI_DATA],
        strict=False,
    ):
        build_fig2_marginals(df)[key].to_csv(path, index=False)

    build_fig2_controls_data(df).to_csv(FIG2_CONTROLS_DATA, index=False)
