import numpy as np
import pandas as pd
from scipy import stats
from scipy.linalg import qr

_FE_GROUPS = ["wave", "strata", "missfit", "_ws", "_wm"]
_CONVERGENCE_THRESHOLD = 1e-13


def _fe_rank(df: pd.DataFrame) -> int:
    def d(s, p):
        return pd.get_dummies(s, prefix=p, drop_first=True, dtype=float)

    blocks = [
        d(df["wave"], "w"),
        d(df["strata"], "s"),
        d(df["missfit"], "m"),
        d(df["wave"].astype(str) + "_" + df["strata"].astype(str), "ws"),
        d(df["wave"].astype(str) + "_" + df["missfit"].astype(str), "wm"),
    ]
    return int(np.linalg.matrix_rank(pd.concat(blocks, axis=1).to_numpy(dtype=float)))


def _absorb_fe(data: pd.DataFrame, cols: list[str]) -> pd.DataFrame:
    prev = data[cols].to_numpy().copy()
    for _ in range(2000):
        for g in _FE_GROUPS:
            gm = data.groupby(g)[cols].transform("mean")
            for c in cols:
                data[c] = data[c] - gm[c]
        curr = data[cols].to_numpy()
        if np.max(np.abs(curr - prev)) < _CONVERGENCE_THRESHOLD:
            break
        prev = curr.copy()
    return data


def _sandwich_vcov(
    x_mat: np.ndarray,
    residuals: np.ndarray,
    clusters: np.ndarray,
    k_fe_params: int,
) -> tuple[np.ndarray, np.ndarray, int]:
    qr_res = qr(x_mat, pivoting=True)
    piv = qr_res[2]
    rank = int(np.linalg.matrix_rank(x_mat))
    keep = np.sort(piv[:rank])
    x_keep = x_mat[:, keep]

    n, k = len(residuals), rank
    unique_cl = np.unique(clusters)
    g_clusters = len(unique_cl)

    bread = np.linalg.inv(x_keep.T @ x_keep)
    meat = sum(
        x_keep[clusters == c].T
        @ np.outer(residuals[clusters == c], residuals[clusters == c])
        @ x_keep[clusters == c]
        for c in unique_cl
    )
    ssc = (g_clusters / (g_clusters - 1)) * ((n - k_fe_params) / (n - k_fe_params - k))
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
    data = df.copy().dropna(
        subset=[y, *regressors, "wave", "strata", "missfit", cluster_col]
    )
    data["_ws"] = data["wave"].astype(str) + "_" + data["strata"].astype(str)
    data["_wm"] = data["wave"].astype(str) + "_" + data["missfit"].astype(str)

    cols = [y, *regressors]
    for c in cols:
        data[c] = data[c].astype(float)

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
    k_fe = _fe_rank(data)
    vcov, _, g_clusters = _sandwich_vcov(x_full, resid, clusters, k_fe)
    se = np.sqrt(np.diag(vcov))

    t_crit = stats.t.ppf(0.975, df=g_clusters - 1)
    results = {}
    for i, name in enumerate(regressors):
        e, s = float(coef[i]), float(se[i])
        t_stat = e / s if s > 0 else np.nan
        results[name] = {
            "estimate": e,
            "ci_low": e - t_crit * s,
            "ci_high": e + t_crit * s,
            "pval": float(2 * (1 - stats.t.cdf(abs(t_stat), df=g_clusters - 1))),
        }
    return results, vcov, g_clusters
