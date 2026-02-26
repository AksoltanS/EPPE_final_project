from pathlib import Path

import pandas as pd

# need to write docstings to all functions and check again


# Load function
def load_follow_backs_raw(path: Path) -> pd.DataFrame:
    """Read follow_backs.csv and return a DataFrame (semicolon-delimited)."""
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
    required = {"shadow_ban", "Attr", "treat", "FollowBacks"}
    check_required_columns(raw, required)

    df = pd.DataFrame(index=raw.index)

    df["shadow_ban"] = to_numeric(raw["shadow_ban"])
    df["Attr"] = to_numeric(raw["Attr"])
    df["treat"] = to_numeric(raw["treat"])
    df["FollowBacks"] = to_numeric(raw["FollowBacks"])

    df = df[(df["shadow_ban"] == 0) & (df["Attr"] == 0)].copy()
    return df
