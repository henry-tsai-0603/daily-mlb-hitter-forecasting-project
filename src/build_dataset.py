"""Dataset construction utilities."""

import pandas as pd


def chronological_split(
    df: pd.DataFrame,
    date_col: str,
    train_end: str,
    val_start: str,
    val_end: str,
    test_start: str,
):
    """Split data chronologically into train, validation, and test sets."""
    df = df.copy()
    df[date_col] = pd.to_datetime(df[date_col])

    train = df[df[date_col] <= pd.to_datetime(train_end)]
    val = df[
        (df[date_col] >= pd.to_datetime(val_start))
        & (df[date_col] <= pd.to_datetime(val_end))
    ]
    test = df[df[date_col] >= pd.to_datetime(test_start)]

    return train, val, test
