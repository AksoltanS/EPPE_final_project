from pathlib import Path

import pandas as pd


def load_subject_pool_raw(path: Path) -> pd.DataFrame:
    return pd.read_csv(path)


def load_subject_pool_scrambled_raw(path: Path) -> pd.DataFrame:
    return pd.read_csv(path)


def _check_required_columns(df: pd.DataFrame, required: set[str], *, name: str) -> None:
    missing = required - set(df.columns)
    if missing:
        msg = f"{name} is missing required columns: {', '.join(sorted(missing))}"
        raise KeyError(msg)


def make_subject_pool_analysis_sample(subject_pool: pd.DataFrame) -> pd.DataFrame:
    required = {
        "id",
        "continent",
        "profession",
        "gender",
        "race",
        "follow_diversity",
        "background_pic",
        "share_mobile",
    }
    _check_required_columns(subject_pool, required, name="subject_pool.csv")

    df = subject_pool.copy()

    string_cols = ["continent", "profession", "gender", "race"]
    for c in string_cols:
        df[c] = df[c].astype("string")

    num_cols = ["follow_diversity", "background_pic", "share_mobile"]
    for c in num_cols:
        df[c] = pd.to_numeric(df[c], errors="coerce")

    indicator_cols = [
        "above_median_followers_count",
        "above_median_friends_count",
        "above_median_favourites_count",
        "above_median_statuses_count",
        "above_median_listed_count",
        "above_median_year_created",
    ]
    for c in indicator_cols:
        if c in df.columns:
            df[c] = pd.to_numeric(df[c], errors="coerce")

    keep = list(required) + [c for c in indicator_cols if c in df.columns]
    out = (
        df[keep]
        .dropna(subset=["continent", "profession", "gender", "race"])
        .reset_index(drop=True)
    )
    return out
