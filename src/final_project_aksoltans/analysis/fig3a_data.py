import pandas as pd

from final_project_aksoltans.analysis.stats_helper_functions import (
    aggregate_experimental_data,
)

_BOT_VARS = ["bot_gender", "bot_race", "bot_uni"]


def build_fig3a_data(df: pd.DataFrame) -> pd.DataFrame:
    out = aggregate_experimental_data(df, _BOT_VARS)

    for c in _BOT_VARS:
        out[c] = pd.to_numeric(out[c], errors="coerce").astype("Int64")

    return out.sort_values(_BOT_VARS).reset_index(drop=True)
