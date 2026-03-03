from __future__ import annotations

import pandas as pd
import pytest

from final_project_aksoltans.analysis.fig1_data import build_fig1_data
from final_project_aksoltans.analysis.fig2_data import build_fig2_marginals


def _assert_ci_bounds(df: pd.DataFrame, mean: str, low: str, high: str) -> None:
    df = df.dropna(subset=[mean, low, high])
    assert df[low].le(df[mean]).all()
    assert df[mean].le(df[high]).all()


@pytest.fixture
def follow_backs_df() -> pd.DataFrame:
    return pd.DataFrame(
        {
            "FollowBacks": [1, 0, 1, 0, 1, 1, 0, 0],
            "treat": [1, 1, 2, 2, 3, 3, 4, 4],
            "bot_gender": [0, 0, 0, 0, 1, 1, 1, 1],
            "bot_race": [0, 0, 1, 1, 0, 0, 1, 1],
            "bot_uni": [0, 1, 0, 1, 0, 1, 0, 1],
        }
    )


Expected_groups = 2


def test_build_fig1_data(follow_backs_df: pd.DataFrame) -> None:
    out = build_fig1_data(follow_backs_df)
    assert set(out.columns) >= {"treat", "pct_flwback", "ciL", "ciH"}
    assert sorted(out["treat"].astype(int).tolist()) == [1, 2, 3, 4]
    _assert_ci_bounds(out, mean="pct_flwback", low="ciL", high="ciH")


def test_build_fig2_marginals(
    follow_backs_df: pd.DataFrame,
) -> None:
    out = build_fig2_marginals(follow_backs_df)
    assert set(out.keys()) == {"bot_gender", "bot_race", "bot_uni"}
    for k, df in out.items():
        assert df.shape[0] == Expected_groups, (
            f"{k} should have {Expected_groups} groups (0/1)"
        )
        assert set(df.columns) >= {k, "pct_flwback", "ciL", "ciH"}
        _assert_ci_bounds(df, mean="pct_flwback", low="ciL", high="ciH")
