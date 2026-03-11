from pathlib import Path

import pandas as pd

from final_project_aksoltans.analysis.table1_data import build_table1a, build_table1b
from final_project_aksoltans.config import (
    SRC,
    SUBJECT_POOL_RAW,
    SUBJECT_POOL_SCRAMBLED_RAW,
    TABLE1A_TEX,
    TABLE1B_TEX,
)

_TABLE1A_DEPS = {
    "subjects": SUBJECT_POOL_RAW,
    "scrambled": SUBJECT_POOL_SCRAMBLED_RAW,
}

_TABLE1B_DEPS = {
    "scrambled": SUBJECT_POOL_SCRAMBLED_RAW,
    "subjects": SUBJECT_POOL_RAW,
}


def task_build_table1a(
    script: Path = SRC / "analysis" / "task_table1.py",
    data: dict[str, Path] = _TABLE1A_DEPS,
    produces: Path = TABLE1A_TEX,
) -> None:
    """Build and save Table 1a as a LaTeX file.

    Merges TopUni_10, verified, and continent from the scrambled dataset
    into the subject pool before building the table.

    Args:
        script: Path to this script, used for pytask dependency tracking.
        data: Paths to the subject pool and scrambled CSV files.
        produces: Path where the Table 1a LaTeX file is saved.
    """
    subjects = pd.read_csv(data["subjects"])
    scrambled = pd.read_csv(data["scrambled"])
    for col in ("TopUni_10", "verified", "continent"):
        if col in scrambled.columns and col not in subjects.columns:
            subjects[col] = scrambled[col].to_numpy()

    t1a = build_table1a(subjects)
    produces.parent.mkdir(parents=True, exist_ok=True)
    t1a.drop(columns=["variable", "indent"]).to_latex(
        produces,
        index=False,
        header=["Variables", "% Classified", "N", "%"],
        na_rep="",
        float_format="%.2f",
    )


def task_build_table1b(
    script: Path = SRC / "analysis" / "task_table1.py",
    data: dict[str, Path] = _TABLE1B_DEPS,
    produces: Path = TABLE1B_TEX,
) -> None:
    """Build and save Table 1b as a LaTeX file.

    Pulls share_mobile from the subject pool and scales it to percentages
    before building the table.

    Args:
        script: Path to this script, used for pytask dependency tracking.
        data: Paths to the scrambled and subject pool CSV files.
        produces: Path where the Table 1b LaTeX file is saved.
    """
    scrambled = pd.read_csv(data["scrambled"])
    subjects_raw = pd.read_csv(data["subjects"])
    if "share_mobile" in subjects_raw.columns:
        scrambled["share_mobile"] = (
            pd.to_numeric(subjects_raw["share_mobile"], errors="coerce").to_numpy()
            * 100
        )

    t1b = build_table1b(scrambled)
    produces.parent.mkdir(parents=True, exist_ok=True)
    t1b.to_latex(
        produces,
        index=False,
        header=["Variables", "Mean", "Std. Deviation", "Median", "Min", "Max", "Obs."],
        na_rep="",
    )
