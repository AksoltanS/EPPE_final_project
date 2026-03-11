import warnings

import numpy as np
import pandas as pd
from scipy import stats
from scipy.linalg import qr

_FE_GROUPS = ["wave", "strata", "missfit", "_ws", "_wm"]
_CONVERGENCE_THRESHOLD = 1e-13
_MAX_ITERATIONS = 2000


def _fe_rank(df: pd.DataFrame) -> int:
    """Return the number of linearly independent fixed-effect parameters.

    Builds dummies for wave, strata, missfit, wave*strata, and wave*missfit,
    then returns the rank of their concatenation. Used for the degrees-of-freedom
    correction in '_sandwich_vcov'.

    Args:
        df: DataFrame with wave, strata, and missfit columns.

    Returns:
        Rank of the concatenated dummy matrix.
    """

    def _dummies(s: pd.Series, prefix: str) -> pd.DataFrame:
        """Convert a Series to dummy variables dropping the first level."""
        return pd.get_dummies(s, prefix=prefix, drop_first=True, dtype=float)

    blocks = [
        _dummies(df["wave"], "w"),
        _dummies(df["strata"], "s"),
        _dummies(df["missfit"], "m"),
        _dummies(df["wave"].astype(str) + "_" + df["strata"].astype(str), "ws"),
        _dummies(df["wave"].astype(str) + "_" + df["missfit"].astype(str), "wm"),
    ]
    return int(np.linalg.matrix_rank(pd.concat(blocks, axis=1).to_numpy(dtype=float)))


def _absorb_fe(data: pd.DataFrame, cols: list[str]) -> pd.DataFrame:
    """Remove fixed effects via iterative within-group demeaning.

    Cycles through _FE_GROUPS subtracting each group mean until
    convergence or _MAX_ITERATIONS.

    Args:
        data: DataFrame with the columns to demean and the FE group columns.
        cols: Outcome and regressor columns to demean.

    Returns:
        DataFrame with fixed-effect variation removed from cols.
    """
    prev = data[cols].to_numpy().copy()
    for _iteration in range(_MAX_ITERATIONS):
        for g in _FE_GROUPS:
            gm = data.groupby(g)[cols].transform("mean")
            for c in cols:
                data[c] = data[c] - gm[c]
        curr = data[cols].to_numpy()
        if np.max(np.abs(curr - prev)) < _CONVERGENCE_THRESHOLD:
            break
        prev = curr.copy()
    else:
        warnings.warn(
            f"_absorb_fe did not converge after {_MAX_ITERATIONS} iterations. "
            "Results may be inaccurate.",
            stacklevel=3,
        )
    return data


def _sandwich_vcov(
    x_mat: np.ndarray,
    residuals: np.ndarray,
    clusters: np.ndarray,
) -> tuple[np.ndarray, np.ndarray, int]:
    """Compute a cluster-robust sandwich variance-covariance matrix.

    Uses pivoted QR to drop linearly dependent columns, then builds
    V = B⁻¹ M B⁻¹ with the ssc() small-sample correction
    (G/(G-1)) * ((n-1)/(n-k)).

    Args:
        x_mat: Regressor matrix after fixed-effect absorption.
        residuals: OLS residuals after fixed-effect absorption.
        clusters: Cluster assignment per observation.

    Returns:
        vcov: Variance-covariance matrix with NaN for linearly dependent columns.
        keep: Column indices retained after the rank check.
        g_clusters: Number of clusters used in the correction.
    """
    qr_res = qr(x_mat, pivoting=True)
    piv = qr_res[2]
    rank = int(np.linalg.matrix_rank(x_mat))
    keep = np.sort(piv[:rank])
    x_keep = x_mat[:, keep]
    n = len(residuals)
    k_reg = rank
    unique_cl = np.unique(clusters)
    g_clusters = len(unique_cl)
    bread = np.linalg.inv(x_keep.T @ x_keep)
    meat = sum(
        x_keep[clusters == c].T
        @ np.outer(residuals[clusters == c], residuals[clusters == c])
        @ x_keep[clusters == c]
        for c in unique_cl
    )
    ssc = (g_clusters / (g_clusters - 1)) * ((n - 1) / (n - k_reg))
    vcov_keep = ssc * bread @ meat @ bread
    p = x_mat.shape[1]
    vcov = np.full((p, p), np.nan)
    for i, ki in enumerate(keep):
        for j, kj in enumerate(keep):
            vcov[ki, kj] = vcov_keep[i, j]
    return vcov, keep, g_clusters


def fe_ols(
    df: pd.DataFrame,
    y: str,
    regressors: list[str],
    cluster_col: str = "treat_names",
) -> tuple[dict[str, dict[str, float]], np.ndarray, int]:
    """Run OLS with fixed effects absorbed and cluster-robust standard errors.

    1. Validates all required columns are present
    2. Absorbs _FE_GROUPS fixed effects via iterative demeaning (_absorb_fe)
    3. Identifies linearly independent regressors via pivoted QR
    4. Estimates OLS coefficients via least squares
    5. Computes cluster-robust sandwich VCV with ssc() correction
    6. Returns t(G-1) confidence intervals and p-values

    Args:
        df: Analysis DataFrame with all required columns.
        y: Outcome variable name.
        regressors: Regressor column names.
        cluster_col: Column to cluster standard errors on.

    Returns:
        results: Estimates for each regressor with se, ci_low, ci_high, and pval.
        vcov: Full variance-covariance matrix.
        g_clusters: Number of clusters.

    Raises:
        ValueError: If any required columns are missing from df.
    """
    required = {y, *regressors, "wave", "strata", "missfit", cluster_col}
    missing = required - set(df.columns)
    if missing:
        msg = f"fe_ols: missing columns: {sorted(missing)}"
        raise ValueError(msg)

    data = df.copy().dropna(subset=list(required))
    data["_ws"] = data["wave"].astype(str) + "_" + data["strata"].astype(str)
    data["_wm"] = data["wave"].astype(str) + "_" + data["missfit"].astype(str)

    cols = [y, *regressors]
    for c in cols:
        data[c] = data[c].astype(float)
    _fe_rank(data)
    data = _absorb_fe(data, cols)

    y_vec = data[y].to_numpy(dtype=float)
    x_full = data[regressors].to_numpy(dtype=float)
    qr_res = qr(x_full, pivoting=True)
    piv = qr_res[2]
    rank = int(np.linalg.matrix_rank(x_full))
    keep = np.sort(piv[:rank])
    x_mat = x_full[:, keep]

    coef_keep, *_ = np.linalg.lstsq(x_mat, y_vec, rcond=None)
    resid = y_vec - x_mat @ coef_keep
    coef = np.full(x_full.shape[1], np.nan)
    coef[keep] = coef_keep

    clusters = data[cluster_col].to_numpy()
    vcov, _, g_clusters = _sandwich_vcov(x_full, resid, clusters)
    se = np.sqrt(np.diag(vcov))

    t_crit = stats.t.ppf(0.975, df=g_clusters - 1)
    results: dict[str, dict[str, float]] = {}
    for i, name in enumerate(regressors):
        e, s = float(coef[i]), float(se[i])
        t_stat = e / s if s > 0 else np.nan
        results[name] = {
            "estimate": e,
            "se": float(s),
            "ci_low": float(e - t_crit * s),
            "ci_high": float(e + t_crit * s),
            "pval": float(2 * (1 - stats.t.cdf(abs(t_stat), df=g_clusters - 1))),
        }
    return results, vcov, g_clusters
