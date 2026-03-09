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
    fb = pd.read_parquet(data)

    for key, path in zip(
        BOT_VARS,
        [FIG2_GENDER_DATA, FIG2_RACE_DATA, FIG2_UNI_DATA],
        strict=False,
    ):
        path.parent.mkdir(parents=True, exist_ok=True)
        build_fig2_marginals(fb)[key].to_csv(path, index=False)

    FIG2_CONTROLS_DATA.parent.mkdir(parents=True, exist_ok=True)
    build_fig2_controls_data(fb).to_csv(FIG2_CONTROLS_DATA, index=False)
