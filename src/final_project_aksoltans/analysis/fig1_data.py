import pandas as pd

from final_project_aksoltans.analysis.stats_helper_functions import mean_ci_t


def build_fig1_data(fb: pd.DataFrame) -> pd.DataFrame:
    rows = []
    for treat, g in fb.groupby("treat", sort=True):
        mean, ci_low, ci_high = mean_ci_t(g["FollowBacks"])
        rows.append(
            {
                "treat": int(pd.to_numeric(treat)),
                "pct_flwback": mean,
                "ciL": ci_low,
                "ciH": ci_high,
            }
        )
    return pd.DataFrame(rows).sort_values("treat").reset_index(drop=True)
