import pandas as pd


def build_table1a(subjects: pd.DataFrame) -> pd.DataFrame:
    cat_vars = ["gender", "continent", "profession", "race"]
    rows: list[dict[str, object]] = []

    for v in cat_vars:
        if v not in subjects.columns:
            continue
        counts = subjects[v].value_counts(dropna=False)
        total = int(counts.sum())

        for level, n in counts.items():
            share = float(n) / total if total > 0 else float("nan")
            rows.append(
                {
                    "variable": v,
                    "level": str(level),
                    "share": share,
                    "n": int(n),
                }
            )
    return pd.DataFrame(rows)


def build_table1b(scrambled: pd.DataFrame) -> pd.DataFrame:
    num_vars = [
        "followers_count",
        "friends_count",
        "statuses_count",
        "favourites_count",
        "listed_count",
        "year_created",
    ]
    rows: list[dict[str, object]] = []

    for v in num_vars:
        if v not in scrambled.columns:
            continue
        x = pd.to_numeric(scrambled[v], errors="coerce").dropna()
        if x.empty:
            continue
        rows.append(
            {
                "variable": v,
                "mean": float(x.mean()),
                "sd": float(x.std(ddof=1)),
                "median": float(x.median()),
                "min": float(x.min()),
                "max": float(x.max()),
                "n": int(x.shape[0]),
            }
        )
    return pd.DataFrame(rows)
