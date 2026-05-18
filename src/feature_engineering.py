"""Feature engineering utilities.

This module will build:
- rolling recent-form features
- season-to-date baseline features
- trend/deviation features
- future 7-day xwOBA target
"""

import pandas as pd
import numpy as np


def prepare_statcast_dates(df: pd.DataFrame) -> pd.DataFrame:
    """Ensure game_date is a datetime column."""
    df = df.copy()
    df["game_date"] = pd.to_datetime(df["game_date"])
    return df


def safe_mean(series: pd.Series) -> float:
    """Return mean while ignoring missing values."""
    return float(series.dropna().mean()) if series.dropna().shape[0] > 0 else np.nan


def build_placeholder_rolling_features(df: pd.DataFrame) -> pd.DataFrame:
    """Placeholder for rolling feature generation.

    TODO:
    1. Aggregate pitch-level data to batter-date level.
    2. Build last 7-day and last 14-day features.
    3. Build season-to-date features.
    4. Build trend/deviation features.
    """
    raise NotImplementedError("Implement rolling feature construction here.")


def build_future_target(df: pd.DataFrame, target_window: int = 7) -> pd.DataFrame:
    """Placeholder for future target generation.

    Target:
        future_7d_xwoba
    """
    raise NotImplementedError("Implement future target construction here.")
