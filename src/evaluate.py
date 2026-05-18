"""Evaluation utilities."""

import numpy as np
from scipy.stats import spearmanr
from sklearn.metrics import mean_absolute_error, mean_squared_error, r2_score


def regression_metrics(y_true, y_pred) -> dict:
    """Compute standard regression metrics."""
    rmse = float(np.sqrt(mean_squared_error(y_true, y_pred)))
    return {
        "mae": float(mean_absolute_error(y_true, y_pred)),
        "rmse": rmse,
        "r2": float(r2_score(y_true, y_pred)),
        "spearman": float(spearmanr(y_true, y_pred, nan_policy="omit").correlation),
    }


def top_k_actual_mean(df, pred_col: str, actual_col: str, k: int = 20) -> float:
    """Mean actual value among top-k predicted rows."""
    top = df.sort_values(pred_col, ascending=False).head(k)
    return float(top[actual_col].mean())
