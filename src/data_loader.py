"""Data loading utilities for the MLB hitter forecasting project."""

from pathlib import Path
from typing import Union

import pandas as pd


PathLike = Union[str, Path]


def load_csv(path: PathLike) -> pd.DataFrame:
    """Load a CSV file into a pandas DataFrame."""
    return pd.read_csv(path)


def save_csv(df: pd.DataFrame, path: PathLike) -> None:
    """Save a DataFrame to CSV, creating parent directories when needed."""
    path = Path(path)
    path.parent.mkdir(parents=True, exist_ok=True)
    df.to_csv(path, index=False)


def load_raw_statcast(raw_data_dir: PathLike) -> pd.DataFrame:
    """Load all raw Statcast CSV files from a directory."""
    raw_data_dir = Path(raw_data_dir)
    files = sorted(raw_data_dir.glob("*.csv"))

    if not files:
        raise FileNotFoundError(f"No CSV files found in {raw_data_dir}")

    return pd.concat((pd.read_csv(file) for file in files), ignore_index=True)