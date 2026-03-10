import pandas as pd


def check_required_columns(df: pd.DataFrame, required: list[str], name: str) -> None:
    """Raise ValueError if any required columns are missing from DataFrame."""
    missing = set(required) - set(df.columns)
    if missing:
        missing_str = ", ".join(sorted(missing))
        msg = f"{name} is missing required columns: {missing_str}"
        raise ValueError(msg)
