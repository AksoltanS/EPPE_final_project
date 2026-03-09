import pandas as pd

from final_project_aksoltans.analysis.stats_helper_functions import (
    aggregate_experimental_data,
)
from final_project_aksoltans.config import BOT_VARS


def build_fig3a_data(df: pd.DataFrame) -> pd.DataFrame:
    out = aggregate_experimental_data(df, BOT_VARS)

    for c in BOT_VARS:
        out[c] = pd.to_numeric(out[c], errors="coerce").astype("Int64")

    return out.sort_values(BOT_VARS).reset_index(drop=True)
