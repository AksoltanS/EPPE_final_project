from pathlib import Path

import pandas as pd

from final_project_aksoltans.config import SRC, SUBJECT_POOL_ANALYSIS, SUBJECT_POOL_RAW
from final_project_aksoltans.data_management.clean_subject_pool import (
    make_subject_pool_analysis_sample,
)


def task_clean_subject_pool_data(
    script: Path = SRC / "data_management" / "task_clean_subject_pool.py",
    data: Path = SUBJECT_POOL_RAW,
    produces: Path = SUBJECT_POOL_ANALYSIS,
) -> None:
    """Load and clean the raw subject pool data, saving the result to parquet.

    Args:
        script: Path to this script, used for pytask dependency tracking.
        data: Path to the raw subject_pool.csv file.
        produces: Path where the cleaned parquet file is saved.

    """
    raw = pd.read_csv(data)
    clean = make_subject_pool_analysis_sample(raw)
    clean.to_parquet(produces, index=False)
