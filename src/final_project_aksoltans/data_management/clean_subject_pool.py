from pathlib import Path

import pandas as pd

from final_project_aksoltans.data_management.utils import check_required_columns

_REQUIRED_COLS: list[str] = [
    "id",
    "continent",
    "profession",
    "gender",
    "race",
    "follow_diversity",
    "background_pic",
    "share_mobile",
    "profile_pic",
]

_STRING_COLS: list[str] = ["continent", "profession", "gender", "race"]
_NUM_COLS: list[str] = ["follow_diversity", "background_pic", "share_mobile"]

_INDICATOR_COLS: list[str] = [
    "above_median_followers_count",
    "above_median_friends_count",
    "above_median_favourites_count",
    "above_median_statuses_count",
    "above_median_listed_count",
    "above_median_year_created",
]

_PROFESSION_MAP: dict[str, str] = {
    "PostDoc": "Researcher",
    "Government": "Other",
    "Industry": "Other",
    "Journalist": "Other",
    "MultilateralOrg": "Other",
}

_CONTINENT_OTHER: set[str] = {"Africa", "Asia", "LatinAmerica", "Oceania"}


def load_subject_pool_raw(path: Path) -> pd.DataFrame:
    """Load the raw subject pool dataset from a CSV.

    Args:
        path: Path to the subject_pool.csv file.

    Returns:
        Raw subject pool data as a DataFrame.
    """
    return pd.read_csv(path)


def load_subject_pool_scrambled_raw(path: Path) -> pd.DataFrame:
    """Load the scrambled subject pool dataset from a CSV.

    Args:
        path: Path to the scrambled subject pool CSV file.

    Returns:
        Raw scrambled subject pool data as a DataFrame
    """
    return pd.read_csv(path)


def _simplify_professions(s: pd.Series) -> pd.Series:
    """Simplify some professions by merging to Other.

    Args:
        s: Series of raw profession strings.

    Returns:
        Series with professions remapped using `_PROFESSION_MAP`.
    """
    return s.map(lambda x: _PROFESSION_MAP.get(x, x))


def _simplify_continents(s: pd.Series) -> pd.Series:
    """Merge some continents into 'Other'.

    Args:
        s: Series of raw continent strings.

    Returns:
        Series where continents in `_CONTINENT_OTHER` are replaced with 'Other'.
    """
    return s.map(lambda x: "Other" if x in _CONTINENT_OTHER else x)


def make_subject_pool_analysis_sample(subject_pool: pd.DataFrame) -> pd.DataFrame:
    """Clean the raw subject pool data into the analysis sample.

    Checks for required columns, coerces dtypes, simplifies profession and
    continent labels, and drops rows with missing values in string columns.

    Args:
        subject_pool: Raw subject pool DataFrame from `load_subject_pool_raw`.

    Returns:
        Cleaned DataFrame ready to use to create figures and tables.

    Raises:
        ValueError: If any required columns are missing.
    """
    check_required_columns(subject_pool, _REQUIRED_COLS, name="subject_pool.csv")
    df = subject_pool.copy()

    for c in _STRING_COLS:
        df[c] = df[c].astype("string")
    df["profession"] = _simplify_professions(df["profession"])
    df["continent"] = _simplify_continents(df["continent"])

    for c in _NUM_COLS:
        df[c] = pd.to_numeric(df[c], errors="coerce")

    for c in _INDICATOR_COLS:
        if c in df.columns:
            df[c] = pd.to_numeric(df[c], errors="coerce")

    keep = _REQUIRED_COLS + [col for col in _INDICATOR_COLS if col in df.columns]
    return df[keep].dropna(subset=_STRING_COLS).reset_index(drop=True)
