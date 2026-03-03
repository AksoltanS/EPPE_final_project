import pandas as pd

from final_project_aksoltans.analysis.stats_helper_functions import (
    aggregate_experimental_data,
)


def build_fig2_marginals(df: pd.DataFrame) -> dict[str, pd.DataFrame]:
    outs: dict[str, pd.DataFrame] = {}

    for col in ["bot_gender", "bot_race", "bot_uni"]:
        out = aggregate_experimental_data(df, [col])
        out[col] = pd.to_numeric(out[col], errors="coerce").astype("Int64")
        outs[col] = out.sort_values(col).reset_index(drop=True)

    return outs
