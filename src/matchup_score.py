"""Matchup scoring utilities.

Combines:
- batter pitch-type weakness
- opposing pitcher pitch mix

to create a matchup weakness score.
"""

import pandas as pd


def build_pitcher_pitch_mix(df: pd.DataFrame, pitch_group_col: str = "pitch_group") -> pd.DataFrame:
    """Build pitcher pitch mix by pitch group.

    Expected input columns:
        pitcher, pitch_group
    """
    counts = (
        df.groupby(["pitcher", pitch_group_col])
        .size()
        .reset_index(name="n")
    )
    totals = counts.groupby("pitcher")["n"].transform("sum")
    counts["usage"] = counts["n"] / totals

    pitch_mix = (
        counts.pivot(index="pitcher", columns=pitch_group_col, values="usage")
        .fillna(0.0)
        .add_prefix("pitcher_")
        .add_suffix("_usage")
        .reset_index()
    )
    return pitch_mix


def compute_matchup_weakness_score(row: pd.Series, pitch_groups: list[str]) -> float:
    """Compute weighted matchup weakness score for one batter-pitcher matchup."""
    score = 0.0
    for pitch in pitch_groups:
        weakness_col = f"batter_{pitch}_weakness"
        usage_col = f"pitcher_{pitch}_usage"
        if weakness_col in row and usage_col in row:
            score += row[weakness_col] * row[usage_col]
    return score
