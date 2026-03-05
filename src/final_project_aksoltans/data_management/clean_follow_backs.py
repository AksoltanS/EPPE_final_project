from pathlib import Path

import pandas as pd

# need to write docstings to all functions and check again

INT_COLS: list[str] = [
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

FLOAT_COLS: list[str] = [
    "FollowBacks",
]

STR_COLS: list[str] = [
    "race",
    "gender",
    "treat_names",
    "continent",
    "profession",
]

NUM_COLS: list[str] = INT_COLS + FLOAT_COLS


def load_follow_backs_raw(path: Path) -> pd.DataFrame:
    return pd.read_csv(path, sep=";")


def check_required_columns(df: pd.DataFrame, required: set[str]) -> None:
    missing = required - set(df.columns)
    if missing:
        missing_str = ", ".join(sorted(missing))
        msg = f"Missing required columns: {missing_str}"
        raise ValueError(msg)


def to_numeric(s: pd.Series) -> pd.Series:
    return pd.to_numeric(s, errors="coerce")


def make_follow_backs_analysis_sample(raw: pd.DataFrame) -> pd.DataFrame:
    df = pd.DataFrame(index=raw.index)
    for col in NUM_COLS:
        df[col] = pd.to_numeric(raw[col], errors="coerce")
    for col in STR_COLS:
        df[col] = raw[col].astype("string")
    df = df[(df["shadow_ban"] == 0) & (df["Attr"] == 0)].copy()
    df[INT_COLS] = df[INT_COLS].astype("Int64")

    return df
