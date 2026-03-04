from pathlib import Path

from final_project_aksoltans.config import SRC, SUBJECT_POOL_ANALYSIS, SUBJECT_POOL_RAW
from final_project_aksoltans.data_management.clean_subject_pool import (
    load_subject_pool_raw,
    make_subject_pool_analysis_sample,
)


def task_clean_subject_pool_data(
    script: Path = SRC / "data_management" / "task_clean_subject_pool.py",
    data: Path = SUBJECT_POOL_RAW,
    produces: Path = SUBJECT_POOL_ANALYSIS,
) -> None:
    raw = load_subject_pool_raw(data)
    clean = make_subject_pool_analysis_sample(raw)

    produces.parent.mkdir(parents=True, exist_ok=True)
    clean.to_parquet(produces, index=False)
