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
    depends_on: dict[str, Path] = _TABLE1A_DEPS,
    produces: Path = TABLE1A_TEX,
) -> None:
    subjects = pd.read_csv(depends_on["subjects"])
    scrambled = pd.read_csv(depends_on["scrambled"])
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
    depends_on: dict[str, Path] = _TABLE1B_DEPS,
    produces: Path = TABLE1B_TEX,
) -> None:
    scrambled = pd.read_csv(depends_on["scrambled"])
    subjects_raw = pd.read_csv(depends_on["subjects"])
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
