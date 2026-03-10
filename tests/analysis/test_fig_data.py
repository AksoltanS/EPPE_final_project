import numpy as np
import pandas as pd
import pytest

from final_project_aksoltans.analysis.fig1_data import build_fig1_data
from final_project_aksoltans.analysis.fig2_data import (
    build_fig2_controls_data,
    build_fig2_marginals,
)
from final_project_aksoltans.analysis.fig3a_data import build_fig3a_data
from final_project_aksoltans.analysis.fig3b_data import build_fig3b_data
from final_project_aksoltans.config import BOT_VARS

_EXPECTED_FIG3A_ROWS = 8
_EXPECTED_FIG3B_ROWS = 6


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


@pytest.fixture
def full_follow_backs_df() -> pd.DataFrame:
    rng = np.random.default_rng(42)
    n = 200
    bot_gender = rng.integers(0, 2, size=n).astype(float)
    bot_race = rng.integers(0, 2, size=n).astype(float)
    bot_uni = rng.integers(0, 2, size=n).astype(float)
    return pd.DataFrame(
        {
            "FollowBacks": np.clip(
                0.05 * bot_gender
                - 0.04 * bot_race
                + 0.06 * bot_uni
                + rng.normal(0, 0.3, n),
                0,
                1,
            ),
            "bot_gender": bot_gender,
            "bot_race": bot_race,
            "bot_uni": bot_uni,
            "wave": rng.integers(1, 6, size=n),
            "strata": rng.integers(1, 4, size=n),
            "missfit": rng.integers(0, 2, size=n),
            "treat_names": [
                f"t{int(g)}{int(r)}{int(u)}"
                for g, r, u in zip(bot_gender, bot_race, bot_uni, strict=False)
            ],
            "continent": rng.choice(["Europe", "NorthAmerica", "Other"], size=n),
            "profession": rng.choice(
                ["AssistantProf", "PhdStudent", "Researcher"], size=n
            ),
            "female": rng.integers(0, 2, size=n).astype(float),
            "above_median_year_created": rng.integers(0, 2, size=n).astype(float),
            "background_pic": rng.integers(0, 2, size=n).astype(float),
            "above_median_followers_count": rng.integers(0, 2, size=n).astype(float),
            "above_median_friends_count": rng.integers(0, 2, size=n).astype(float),
        }
    )


def test_build_fig1_data_columns(follow_backs_df: pd.DataFrame) -> None:
    out = build_fig1_data(follow_backs_df)
    assert set(out.columns) >= {"treat", "pct_flwback", "ciL", "ciH"}


def test_build_fig1_data_treat_values(follow_backs_df: pd.DataFrame) -> None:
    out = build_fig1_data(follow_backs_df)
    assert sorted(out["treat"].astype(int).tolist()) == [1, 2, 3, 4]


def test_build_fig2_marginals_keys(follow_backs_df: pd.DataFrame) -> None:
    out = build_fig2_marginals(follow_backs_df)
    assert set(out.keys()) == {"bot_gender", "bot_race", "bot_uni"}


def test_build_fig2_controls_data_columns(full_follow_backs_df: pd.DataFrame) -> None:
    out = build_fig2_controls_data(full_follow_backs_df)
    assert set(out.columns) >= {"coef", "controls", "Estimate", "pval", "ciL", "ciH"}


def test_build_fig2_controls_data_has_both_control_groups(
    full_follow_backs_df: pd.DataFrame,
) -> None:
    out = build_fig2_controls_data(full_follow_backs_df)
    assert set(out["controls"].unique()) == {"Yes", "No"}


def test_build_fig3a_data_columns(follow_backs_df: pd.DataFrame) -> None:
    out = build_fig3a_data(follow_backs_df)
    assert set(out.columns) >= {*BOT_VARS, "pct_flwback", "ciL", "ciH"}


def test_build_fig3a_data_shape(follow_backs_df: pd.DataFrame) -> None:
    out = build_fig3a_data(follow_backs_df)
    assert out.shape[0] == _EXPECTED_FIG3A_ROWS


def test_build_fig3b_data_shape(full_follow_backs_df: pd.DataFrame) -> None:
    out = build_fig3b_data(full_follow_backs_df)
    assert out.shape[0] == _EXPECTED_FIG3B_ROWS


@pytest.mark.parametrize("col", ["dim", "x", "fb", "CIlow", "CIhigh", "pval"])
def test_build_fig3b_data_columns(full_follow_backs_df: pd.DataFrame, col: str) -> None:
    out = build_fig3b_data(full_follow_backs_df)
    assert col in out.columns


def test_build_fig3b_data_x_labels(full_follow_backs_df: pd.DataFrame) -> None:
    out = build_fig3b_data(full_follow_backs_df)
    assert set(out["x"].unique()) == {"0", "1", "int"}
