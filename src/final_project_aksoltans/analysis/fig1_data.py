import pandas as pd

from final_project_aksoltans.analysis.stats_helper_functions import (
    aggregate_experimental_data,
)


def build_fig1_data(fb: pd.DataFrame) -> pd.DataFrame:
    """Aggregate follow-backs by treatment level for Figure 1.

    Args:
        fb: Cleaned follow-backs DataFrame.

    Returns:
        DataFrame sorted by treat with one row per treatment level.
    """
    out = aggregate_experimental_data(fb, ["treat"])
    out["treat"] = pd.to_numeric(out["treat"], errors="raise").astype("Int64")
    return out.sort_values("treat").reset_index(drop=True)
