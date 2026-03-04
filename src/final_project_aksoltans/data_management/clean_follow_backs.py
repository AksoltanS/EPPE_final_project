from pathlib import Path

import pandas as pd

# need to write docstings to all functions and check again


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
    num_cols = [
        "shadow_ban",
        "Attr",
        "treat",
        "FollowBacks",
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
    str_cols = ["race", "gender", "treat_names", "continent", "profession"]

    df = pd.DataFrame(index=raw.index)
    for col in num_cols:
        df[col] = pd.to_numeric(raw[col], errors="coerce")
    for col in str_cols:
        df[col] = raw[col].astype("string")

    df = df[(df["shadow_ban"] == 0) & (df["Attr"] == 0)].copy()
    return df.dropna(subset=num_cols)
