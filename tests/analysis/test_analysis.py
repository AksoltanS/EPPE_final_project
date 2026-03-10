import numpy as np
import pandas as pd
import pytest

from final_project_aksoltans.analysis.fe_ols import fe_ols
from final_project_aksoltans.analysis.stats_helper_functions import (
    _mean_ci_t,
    aggregate_experimental_data,
)

_BOT_VARS = ["bot_gender", "bot_race", "bot_uni"]
_RESULT_KEYS = {"estimate", "se", "ci_low", "ci_high", "pval"}


@pytest.fixture
def synthetic_fb() -> pd.DataFrame:
    rng = np.random.default_rng(42)
    n = 200
    wave = rng.integers(1, 6, size=n)
    strata = rng.integers(1, 4, size=n)
    missfit = rng.integers(0, 2, size=n)
    bot_gender = rng.integers(0, 2, size=n).astype(float)
    bot_race = rng.integers(0, 2, size=n).astype(float)
    bot_uni = rng.integers(0, 2, size=n).astype(float)
    treat_names = [
        f"t{int(g)}{int(r)}{int(u)}"
        for g, r, u in zip(bot_gender, bot_race, bot_uni, strict=False)
    ]
    y = np.clip(
        0.05 * bot_gender - 0.04 * bot_race + 0.06 * bot_uni + rng.normal(0, 0.3, n),
        0,
        1,
    )
    return pd.DataFrame(
        {
            "FollowBacks": y,
            "bot_gender": bot_gender,
            "bot_race": bot_race,
            "bot_uni": bot_uni,
            "wave": wave,
            "strata": strata,
            "missfit": missfit,
            "treat_names": treat_names,
        }
    )


def test_mean_ci_t_ordering() -> None:
    x = pd.Series([0, 1, 0, 1, 1, 0, 1])
    mean, ci_low, ci_high = _mean_ci_t(x)
    assert ci_low <= mean <= ci_high


def test_aggregate_experimental_data_ci_ordering() -> None:
    df = pd.DataFrame(
        {
            "bot_gender": [0, 0, 0, 1, 1, 1],
            "FollowBacks": [0, 1, 0, 1, 1, 0],
        }
    )
    out = aggregate_experimental_data(df, ["bot_gender"])
    assert (out["ciL"] <= out["pct_flwback"]).all()
    assert (out["pct_flwback"] <= out["ciH"]).all()


def test_fe_ols_returns_correct_keys(synthetic_fb: pd.DataFrame) -> None:
    results, _, _ = fe_ols(synthetic_fb, "FollowBacks", _BOT_VARS)
    assert set(results.keys()) == set(_BOT_VARS)
    for name in _BOT_VARS:
        assert set(results[name].keys()) == _RESULT_KEYS


def test_fe_ols_raises_on_missing_column(synthetic_fb: pd.DataFrame) -> None:
    with pytest.raises(ValueError, match="fe_ols: missing columns"):
        fe_ols(synthetic_fb.drop(columns=["wave"]), "FollowBacks", _BOT_VARS)
