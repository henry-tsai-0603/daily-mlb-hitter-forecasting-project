"""Daily prediction utilities."""

import pandas as pd


def assign_signal_label(row: pd.Series) -> str:
    """Assign an interpretable daily watchlist signal.

    This is an initial heuristic and should be refined after experiments.
    """
    pred = row.get("predicted_future_7d_xwoba")
    matchup = row.get("matchup_weakness_score", 0)

    if pd.isna(pred):
        return "Unknown"

    if pred >= 0.370 and matchup < 0.02:
        return "Hot Candidate"
    if pred >= 0.340 and matchup < 0.01:
        return "Bounce-back Candidate"
    if matchup >= 0.04:
        return "Weakness Matchup Alert"
    if pred < 0.300:
        return "Regression Risk"
    return "Neutral"


def generate_watchlist(df: pd.DataFrame) -> pd.DataFrame:
    """Generate a daily hitter watchlist with signal labels."""
    df = df.copy()
    df["signal"] = df.apply(assign_signal_label, axis=1)
    return df
