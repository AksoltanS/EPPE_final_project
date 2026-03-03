import pandas as pd

from final_project_aksoltans.analysis.stats_helper_functions import (
    aggregate_experimental_data,
)


def build_fig3a_data(df: pd.DataFrame) -> pd.DataFrame:
    out = aggregate_experimental_data(df, ["bot_gender", "bot_race", "bot_uni"])

    for c in ["bot_gender", "bot_race", "bot_uni"]:
        out[c] = pd.to_numeric(out[c], errors="coerce").astype("Int64")

    return out.sort_values(["bot_gender", "bot_race", "bot_uni"]).reset_index(drop=True)
