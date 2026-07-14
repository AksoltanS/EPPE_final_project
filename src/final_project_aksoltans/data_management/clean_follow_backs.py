import pandas as pd

from final_project_aksoltans.data_management.utils import check_required_columns

_INT_COLS: list[str] = [
    "shadow_ban",
    "Attr",
    "treat",
    "bot_gender",
    "bot_race",
    "bot_uni",
    "female",
    "follow_diversity",
    "above_median_followers_count",
    "above_median_friends_count",
    "above_median_year_created",
    "background_pic",
    "wave",
    "strata",
    "missfit",
]

_FLOAT_COLS: list[str] = [
    "FollowBacks",
]

_STR_COLS: list[str] = [
    "race",
    "gender",
    "treat_names",
    "continent",
    "profession",
]
_KEY_COLS: list[str] = [
    "FollowBacks",
    "treat",
    "bot_gender",
    "bot_race",
    "bot_uni",
    "treat_names",
]

_REQUIRED_COLS: list[str] = _INT_COLS + _FLOAT_COLS + _STR_COLS


def make_follow_backs_analysis_sample(raw: pd.DataFrame) -> pd.DataFrame:
    """Clean the raw follow-backs data into the analysis sample.

    Checks for required columns, coerces dtypes, drops shadow-banned and
    attribute-flagged rows, and removes rows with missing values in the key
    analysis columns.

    Args:
       raw: Raw follow-backs DataFrame loaded from follow_backs.csv.

    Returns:
        Cleaned DataFrame ready to use to create figures and tables.

    Raises:
        ValueError: If any required columns are missing.
    """
    check_required_columns(raw, _REQUIRED_COLS, name="follow_backs.csv")
    df = pd.DataFrame(index=raw.index)
    for col in _INT_COLS:
        df[col] = pd.to_numeric(raw[col], errors="coerce")
    for col in _FLOAT_COLS:
        df[col] = pd.to_numeric(raw[col], errors="coerce")
    for col in _STR_COLS:
        df[col] = raw[col].astype("string")

    df = df[(df["shadow_ban"] == 0) & (df["Attr"] == 0)].copy()
    df[_INT_COLS] = df[_INT_COLS].astype("Int64")
    df[_FLOAT_COLS] = df[_FLOAT_COLS].astype("Float64")
    df[_STR_COLS] = df[_STR_COLS].astype("string")
    return df.dropna(subset=_KEY_COLS).reset_index(drop=True)
