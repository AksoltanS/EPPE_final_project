from pathlib import Path

import pandas as pd

from final_project_aksoltans.analysis.stats_helper_functions import mean_ci_t
from final_project_aksoltans.config import (
    FIG3A_DATA,
    FIG3A_PNG,
    FOLLOW_BACKS_ANALYSIS,
    SRC,
)


def task_plot_fig3a(
    script: Path = SRC / "analysis" / "task_fig3a_plot.py",
    data: Path = FOLLOW_BACKS_ANALYSIS,
    produces: tuple[Path, Path] = (FIG3A_DATA, FIG3A_PNG),
) -> None:
    df = pd.read_parquet(data)

    rows: list[dict[str, float | int]] = []
    for (gdr, race, uni), g in df.groupby(
        ["bot_gender", "bot_race", "bot_uni"],
        sort=True,
    ):
        mean, ci_low, ci_high = mean_ci_t(g["FollowBacks"])
        rows.append(
            {
                "bot_gender": int(pd.to_numeric(gdr)),
                "bot_race": int(pd.to_numeric(race)),
                "bot_uni": int(pd.to_numeric(uni)),
                "pct_flwback": mean,
                "ciL": ci_low,
                "ciH": ci_high,
            }
        )
