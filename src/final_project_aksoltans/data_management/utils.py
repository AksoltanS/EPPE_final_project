import pandas as pd


def check_required_columns(df: pd.DataFrame, required: list[str], name: str) -> None:
    missing = set(required) - set(df.columns)
    if missing:
        missing_str = ", ".join(sorted(missing))
        msg = f"{name} is missing required columns: {missing_str}"
        raise ValueError(msg)
