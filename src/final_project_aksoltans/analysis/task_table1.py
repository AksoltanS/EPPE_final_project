from __future__ import annotations

from pathlib import Path

import pandas as pd

from final_project_aksoltans.analysis.table1_data import build_table1a, build_table1b
from final_project_aksoltans.config import (
    SRC,
    SUBJECT_POOL_ANALYSIS,
    SUBJECT_POOL_SCRAMBLED_RAW,
    TABLE1A_TEX,
    TABLE1B_TEX,
)


def task_build_table1(
    script: Path = SRC / "analysis" / "task_table1.py",
    data: tuple[Path, Path] = (SUBJECT_POOL_ANALYSIS, SUBJECT_POOL_SCRAMBLED_RAW),
    produces: tuple[Path, Path] = (TABLE1A_TEX, TABLE1B_TEX),
) -> None:
    subjects_path, scrambled_path = data
    out_a, out_b = produces

    subjects = pd.read_parquet(subjects_path)
    scrambled = pd.read_csv(scrambled_path)

    t1a = build_table1a(subjects)
    t1b = build_table1b(scrambled)

    out_a.parent.mkdir(parents=True, exist_ok=True)
    out_b.parent.mkdir(parents=True, exist_ok=True)

    t1a.to_latex(out_a, index=False)
    t1b.to_latex(out_b, index=False)
