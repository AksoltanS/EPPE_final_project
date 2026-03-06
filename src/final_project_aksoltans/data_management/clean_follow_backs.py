from pathlib import Path

import pandas as pd

# need to write docstings to all functions

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

_NUM_COLS: list[str] = _INT_COLS + _FLOAT_COLS


def load_follow_backs_raw(path: Path) -> pd.DataFrame:
    return pd.read_csv(path, sep=";")


def _check_required_columns(df: pd.DataFrame, required: set[str]) -> None:
    missing = required - set(df.columns)
    if missing:
        missing_str = ", ".join(sorted(missing))
        msg = f"Missing required columns: {missing_str}"
        raise ValueError(msg)


def make_follow_backs_analysis_sample(raw: pd.DataFrame) -> pd.DataFrame:
    _check_required_columns(raw, set(_NUM_COLS + _STR_COLS))
    df = pd.DataFrame(index=raw.index)
    for col in _NUM_COLS:
        df[col] = pd.to_numeric(raw[col], errors="coerce")
    for col in _STR_COLS:
        df[col] = raw[col].astype("string")
    df = df[(df["shadow_ban"] == 0) & (df["Attr"] == 0)].copy()
    df[_INT_COLS] = df[_INT_COLS].astype("Int64")
    return df
