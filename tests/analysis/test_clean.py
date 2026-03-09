import pandas as pd
import pytest

from final_project_aksoltans.data_management.clean_follow_backs import (
    make_follow_backs_analysis_sample,
)

_EXPECTED_FOLLOW_BACKS_ROWS = 2


@pytest.fixture
def raw_follow_backs() -> pd.DataFrame:
    return pd.DataFrame(
        {
            "shadow_ban": ["0", "0", "1", "0"],
            "Attr": ["0", "0", "0", "1"],
            "treat": ["1", "2", "3", "4"],
            "bot_gender": ["0", "1", "0", "1"],
            "bot_race": ["0", "0", "1", "1"],
            "bot_uni": ["1", "0", "1", "0"],
            "female": ["1", "0", "1", "0"],
            "follow_diversity": ["1", "0", "1", "0"],
            "above_median_followers_count": ["1", "1", "0", "0"],
            "above_median_friends_count": ["0", "1", "0", "1"],
            "above_median_year_created": ["1", "0", "0", "1"],
            "background_pic": ["1", "1", "0", "0"],
            "wave": ["1", "2", "1", "2"],
            "strata": ["1", "1", "2", "2"],
            "missfit": ["0", "0", "0", "0"],
            "FollowBacks": ["1.0", "0.0", "1.0", "0.0"],
            "race": ["White", "Black", "White", "Black"],
            "gender": ["female", "male", "female", "male"],
            "treat_names": ["A", "B", "C", "D"],
            "continent": ["Europe", "NorthAmerica", "Europe", "NorthAmerica"],
            "profession": ["AssistantProf", "Researcher", "Other", "PhdStudent"],
        }
    )


def test_follow_backs_filters_shadow_ban_and_attr(
    raw_follow_backs: pd.DataFrame,
) -> None:
    out = make_follow_backs_analysis_sample(raw_follow_backs)
    assert out.shape[0] == _EXPECTED_FOLLOW_BACKS_ROWS
    assert (out["shadow_ban"] == 0).all()
    assert (out["Attr"] == 0).all()
    assert (out["shadow_ban"] == 0).all()
    assert (out["Attr"] == 0).all()


def test_follow_backs_int_cols_dtype(raw_follow_backs: pd.DataFrame) -> None:
    out = make_follow_backs_analysis_sample(raw_follow_backs)
    assert out["bot_gender"].dtype == "Int64"
    assert out["wave"].dtype == "Int64"


def test_follow_backs_raises_on_missing_column(
    raw_follow_backs: pd.DataFrame,
) -> None:
    with pytest.raises(ValueError, match="Missing required columns"):
        make_follow_backs_analysis_sample(
            raw_follow_backs.drop(columns=["FollowBacks"])
        )
