import pandas as pd
import pytest

from final_project_aksoltans.data_management.clean_subject_pool import (
    _simplify_continents,
    _simplify_professions,
    make_subject_pool_analysis_sample,
)

_EXPECTED_SUBJECT_POOL_COLS_START = ["id", "continent", "profession", "gender", "race"]


@pytest.fixture
def raw_subject_pool() -> pd.DataFrame:
    return pd.DataFrame(
        {
            "id": [1, 2, 3, 4],
            "continent": ["Europe", "NorthAmerica", "Asia", "Africa"],
            "profession": ["AssistantProf", "PostDoc", "Government", "PhdStudent"],
            "gender": ["female", "male", "female", "male"],
            "race": ["White", "Black", "White", "Other"],
            "follow_diversity": [1, 0, 1, 0],
            "background_pic": [1, 0, 0, 1],
            "share_mobile": [0.5, 0.3, 0.8, 0.2],
            "profile_pic": [1, 1, 0, 1],
        }
    )


def test_simplify_professions() -> None:
    s = pd.Series(["PostDoc", "Government", "Industry", "AssistantProf"])
    out = _simplify_professions(s)
    assert out.tolist() == ["Researcher", "Other", "Other", "AssistantProf"]


def test_simplify_continents() -> None:
    s = pd.Series(["Asia", "Africa", "Europe", "NorthAmerica"])
    out = _simplify_continents(s)
    assert out.tolist() == ["Other", "Other", "Europe", "NorthAmerica"]


def test_subject_pool_simplifies_profession_and_continent(
    raw_subject_pool: pd.DataFrame,
) -> None:
    out = make_subject_pool_analysis_sample(raw_subject_pool)
    assert "PostDoc" not in out["profession"].tolist()
    assert "Asia" not in out["continent"].tolist()


def test_subject_pool_drops_rows_with_missing_string_cols(
    raw_subject_pool: pd.DataFrame,
) -> None:
    df = raw_subject_pool.copy()
    df.loc[0, "gender"] = None
    out = make_subject_pool_analysis_sample(df)
    assert out.shape[0] == raw_subject_pool.shape[0] - 1


def test_subject_pool_column_order(raw_subject_pool: pd.DataFrame) -> None:
    out = make_subject_pool_analysis_sample(raw_subject_pool)
    assert list(out.columns[: len(_EXPECTED_SUBJECT_POOL_COLS_START)]) == (
        _EXPECTED_SUBJECT_POOL_COLS_START
    )


def test_subject_pool_raises_on_missing_column(
    raw_subject_pool: pd.DataFrame,
) -> None:
    with pytest.raises(ValueError, match="is missing required columns"):
        make_subject_pool_analysis_sample(raw_subject_pool.drop(columns=["race"]))
