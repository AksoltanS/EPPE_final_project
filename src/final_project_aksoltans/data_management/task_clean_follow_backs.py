from pathlib import Path

from final_project_aksoltans.config import FOLLOW_BACKS_ANALYSIS, FOLLOW_BACKS_RAW, SRC
from final_project_aksoltans.data_management.clean_follow_backs import (
    load_follow_backs_raw,
    make_follow_backs_analysis_sample,
)


def task_clean_follow_backs_data(
    script: Path = SRC / "data_management" / "task_clean_follow_backs.py",
    data: Path = FOLLOW_BACKS_RAW,
    produces: Path = FOLLOW_BACKS_ANALYSIS,
) -> None:
    """Load and clean the raw follow-backs data, saving the result to parquet.

    Args:
        script: Path to this script, used for pytask dependency tracking.
        data: Path to the raw follow_backs.csv file.
        produces: Path where the cleaned parquet file is saved.

    """
    raw = load_follow_backs_raw(data)
    clean = make_follow_backs_analysis_sample(raw)
    produces.parent.mkdir(parents=True, exist_ok=True)
    clean.to_parquet(produces, index=False)
