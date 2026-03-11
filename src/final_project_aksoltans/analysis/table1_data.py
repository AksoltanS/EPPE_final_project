import pandas as pd

from final_project_aksoltans.config import TABLE1_QUAL_VARS, TABLE1_QUANT_VARS

_QUANT_LABELS: dict[str, str] = {
    "followers_count": "Number of followers",
    "friends_count": "Number of accounts followed ('friends')",
    "statuses_count": "Number of statuses ('tweets')",
    "favourites_count": "Number of favorites ('likes')",
    "listed_count": "Number of public lists",
    "share_mobile": "Share of tweets/rts by mobile app",
}

_PROFESSION_ORDER: list[str] = [
    "profession",
    "Professor",
    "AssistantProf",
    "AssociateProf",
    "ProfUndefined",
    "PhdStudent",
    "Researcher",
    "Other",
]
_RACE_ORDER: list[str] = ["race", "White", "Black", "Other"]
_PROF_SUBTYPES: list[str] = ["ProfUndefined", "AssistantProf", "AssociateProf"]
_PROF_DOUBLE_INDENT: set[str] = set(_PROF_SUBTYPES)


def _normalize_level(val: object) -> str:
    """Return a string representation of a categorical level."""
    if isinstance(val, bool):
        return str(val).upper()
    return str(val)


def _var_block(data: pd.DataFrame, var: str) -> pd.DataFrame:
    """Build a summary block for one qualitative variable."""
    col = data[var] if var in data.columns else pd.Series(dtype=object)
    pct_classified = (
        round(100 * col.notna().mean(), 2) if len(col) > 0 else float("nan")
    )
    counts = col.value_counts(dropna=True).sort_index()
    total = int(counts.sum())

    rows: list[dict[str, object]] = [
        {
            "variable": var,
            "level": var,
            "pct_classified": pct_classified,
            "n": float("nan"),
            "share": float("nan"),
            "indent": 0,
        }
    ]
    for level_val, count in counts.items():
        level_str = _normalize_level(level_val)
        rows.append(
            {
                "variable": var,
                "level": level_str,
                "pct_classified": float("nan"),
                "n": int(count),
                "share": round(count / total * 100, 2) if total > 0 else float("nan"),
                "indent": 1,
            }
        )

    return pd.DataFrame(rows)


def build_table1a(subjects: pd.DataFrame) -> pd.DataFrame:
    """Build the qualitative summary block for Table 1a.

    Computes counts and shares for each categorical variable, with custom
    ordering and indentation for profession and race.

    Args:
        subjects: Subject pool DataFrame with qualitative columns.

    Returns:
        DataFrame with one row per variable level, ready for LaTeX export.
    """
    blocks = []
    for v in TABLE1_QUAL_VARS:
        if v not in subjects.columns:
            continue
        block = _var_block(subjects, v)

        if v == "profession":
            sub = block[block["level"].isin(_PROF_SUBTYPES)]
            prof_n = pd.to_numeric(sub["n"], errors="coerce").sum()
            prof_share = pd.to_numeric(sub["share"], errors="coerce").sum()
            block.loc[len(block)] = {
                "variable": "profession",
                "level": "Professor",
                "pct_classified": float("nan"),
                "n": int(prof_n),
                "share": round(float(prof_share), 2),
                "indent": 1,
            }
            block.loc[block["level"].isin(_PROF_DOUBLE_INDENT), "indent"] = 2
            order_map = {lv: i for i, lv in enumerate(_PROFESSION_ORDER)}
            block = (
                block.assign(_ord=block["level"].map(order_map))
                .sort_values("_ord")
                .drop(columns="_ord")
                .reset_index(drop=True)
            )

        if v == "race":
            order_map = {lv: i for i, lv in enumerate(_RACE_ORDER)}
            block = (
                block.assign(_ord=block["level"].map(order_map))
                .sort_values("_ord")
                .drop(columns="_ord")
                .reset_index(drop=True)
            )

        blocks.append(block)

    return pd.concat(blocks, ignore_index=True)


def build_table1b(scrambled: pd.DataFrame) -> pd.DataFrame:
    """Build the quantitative summary block for Table 1b.

    Computes mean, standard deviation, median, min, max, and observation
    count for each quantitative variable.

    Args:
        scrambled: Anonymized subject pool DataFrame with quantitative columns.

    Returns:
        DataFrame with one row per variable, ready for LaTeX export.
    """
    rows: list[dict[str, object]] = []
    for v in TABLE1_QUANT_VARS:
        if v not in scrambled.columns:
            continue
        x = pd.to_numeric(scrambled[v], errors="coerce").dropna()
        if x.empty:
            continue
        rows.append(
            {
                "variable": _QUANT_LABELS[v],
                "mean": round(float(x.mean()), 2),
                "sd": round(float(x.std(ddof=1)), 2),
                "median": round(float(x.median()), 2),
                "min": round(float(x.min()), 2),
                "max": round(float(x.max()), 2),
                "n": int(x.shape[0]),
            }
        )

    return pd.DataFrame(rows)
