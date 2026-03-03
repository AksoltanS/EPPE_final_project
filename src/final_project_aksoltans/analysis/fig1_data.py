import pandas as pd

from final_project_aksoltans.analysis.stats_helper_functions import (
    aggregate_experimental_data,
)


def build_fig1_data(fb: pd.DataFrame) -> pd.DataFrame:
    out = aggregate_experimental_data(fb, ["treat"])
    out["treat"] = pd.to_numeric(out["treat"], errors="raise").astype("Int64")
    return out.sort_values("treat").reset_index(drop=True)
