"""Batter weakness profile utilities.

The first version focuses on pitch-type weakness:
    batter_pitch_type_xwOBA vs league_pitch_type_xwOBA
"""

import pandas as pd
import numpy as np


def map_pitch_group(pitch_type: str) -> str:
    """Map raw Statcast pitch types into broad pitch groups."""
    fastball = {"FF", "FA", "SI", "FC"}
    slider = {"SL", "ST"}
    curveball = {"CU", "KC", "SV"}
    changeup = {"CH", "FS", "FO"}

    if pitch_type in fastball:
        return "fastball"
    if pitch_type in slider:
        return "slider"
    if pitch_type in curveball:
        return "curveball"
    if pitch_type in changeup:
        return "changeup"
    return "other"


def build_batter_pitch_type_profile(df: pd.DataFrame) -> pd.DataFrame:
    """Build batter-level pitch-type xwOBA profile.

    Expected input columns:
        batter, pitch_type, estimated_woba_using_speedangle
    """
    df = df.copy()
    df["pitch_group"] = df["pitch_type"].apply(map_pitch_group)

    profile = (
        df.groupby(["batter", "pitch_group"])["estimated_woba_using_speedangle"]
        .mean()
        .reset_index()
        .pivot(index="batter", columns="pitch_group", values="estimated_woba_using_speedangle")
        .add_prefix("batter_")
        .add_suffix("_xwoba")
        .reset_index()
    )
    return profile


def build_league_pitch_type_average(df: pd.DataFrame) -> pd.DataFrame:
    """Compute league average xwOBA by pitch group."""
    df = df.copy()
    df["pitch_group"] = df["pitch_type"].apply(map_pitch_group)

    return (
        df.groupby("pitch_group")["estimated_woba_using_speedangle"]
        .mean()
        .reset_index(name="league_xwoba")
    )
