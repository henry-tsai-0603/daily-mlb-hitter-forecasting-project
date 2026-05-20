# Daily MLB Hitter Forecasting with Batter Weakness and Matchup Adjustment

## Project Overview

This project builds a schedule-aware MLB hitter forecasting system using public Statcast data. The goal is to predict a hitter's short-term offensive performance and combine that prediction with pitch-type matchup context.

The system has three main components:

1. **Short-term hitter forecasting model**  
   Predicts each hitter's future 7-day xwOBA using rolling 7-day, rolling 14-day, season-to-date, and trend-based Statcast features.

2. **Batter weakness and matchup adjustment module**  
   Measures each hitter's pitch-type weaknesses and combines them with opposing pitcher pitch-mix tendencies to identify favorable and unfavorable matchups.

3. **Schedule-aware daily watchlist prototype**  
   Uses the MLB schedule API to retrieve games and probable starting pitchers for a selected date, identifies hitter candidates by team, merges model predictions and matchup scores, and generates an interpretable daily hitter watchlist.

The final output is a prototype **daily hitter watchlist** that categorizes hitters into signals such as:

```text
Hot Candidate
Bounce-back Candidate
Regression Risk
Neutral
```

---

## Research Questions

This project investigates the following questions:

1. Can rolling Statcast indicators predict a hitter's future 7-day xwOBA?
2. Are recent 7-day or 14-day hitter statistics more useful than season-to-date baselines?
3. Can a simple machine learning model improve short-term hitter forecasting over baseline approaches?
4. Can batter pitch-type weakness and pitcher pitch mix provide useful matchup context?
5. Can the forecasting model and matchup module be combined into a schedule-aware daily hitter watchlist?

---

## Data

The project uses public MLB Statcast data collected through `pybaseball`.

Current MVP data range:

```text
2025-04-01 to 2025-05-31
```

The raw Statcast data is pitch-level. It is converted into plate-appearance-level, hitter-date-level, pitcher pitch-mix, and matchup-level tables.

Important fields include:

```text
game_date
batter
pitcher
events
description
pitch_type
stand
p_throws
inning_topbot
home_team
away_team
launch_speed
launch_angle
estimated_woba_using_speedangle
woba_value
```

Large raw data files are excluded from GitHub through `.gitignore`.

---

## Target Variable

The main prediction target is:

```text
future_7d_xwOBA
```

For each hitter and prediction date, the model predicts the hitter's xwOBA over the following 7 days.

xwOBA is used because it better reflects underlying offensive quality than raw outcomes such as batting average or hits.

---

## Data Processing Pipeline

The data pipeline follows this structure:

```text
Raw Statcast pitch-level data
        ↓
Plate appearance rows
        ↓
xwOBA value construction
        ↓
Daily hitter aggregation
        ↓
Rolling feature construction
        ↓
Model-ready forecasting dataset
```

Because Statcast is pitch-level, not every row represents a completed plate appearance. The project keeps rows where:

```python
events.notna()
```

The project also creates a practical offensive value variable:

```python
xwoba_value = estimated_woba_using_speedangle.fillna(woba_value)
```

This means:

- Batted-ball events use expected wOBA when available.
- Walks, strikeouts, and other non-batted-ball events use their actual wOBA value.

---

## Feature Engineering

The forecasting model uses one row per hitter per prediction date:

```text
one row = one hitter on one prediction date
```

For each prediction date:

```text
features = information before the prediction date
target = future 7-day xwOBA after the prediction date
```

This prevents data leakage.

### Recent Form Features

```text
last_7d_PA
last_7d_xwOBA
last_7d_wOBA
last_7d_avg_exit_velocity
last_7d_avg_launch_angle

last_14d_PA
last_14d_xwOBA
last_14d_wOBA
last_14d_avg_exit_velocity
last_14d_avg_launch_angle
```

### Season-to-Date Baseline Features

```text
season_PA
season_xwOBA
season_wOBA
season_avg_exit_velocity
season_avg_launch_angle
```

### Trend / Deviation Features

```text
xwOBA_diff_7d_vs_season
xwOBA_diff_14d_vs_season
wOBA_diff_7d_vs_season
wOBA_diff_14d_vs_season
```

These features measure whether a hitter's recent performance is above or below his season-to-date baseline.

---

## Models

The project compares simple baselines and machine learning models.

### Baselines

```text
season_xwOBA
last_7d_xwOBA
last_14d_xwOBA
```

### Machine Learning Models

```text
Ridge Regression
Random Forest
LightGBM
```

Ridge Regression is selected as the current MVP forecasting model because it achieved the best overall RMSE and strongest Top-K watchlist performance in the initial experiment.

---

## Model Evaluation

Evaluation metrics include:

```text
MAE
RMSE
R²
Spearman correlation
Top-K actual future xwOBA
```

The data is split chronologically:

```text
Train: prediction dates before 2025-05-11
Test: prediction dates from 2025-05-11 onward
```

### Initial Model Results

| Model | MAE | RMSE | R² | Spearman |
|---|---:|---:|---:|---:|
| Ridge Regression | 0.0823 | 0.1064 | 0.0238 | 0.1847 |
| Random Forest | 0.0828 | 0.1072 | 0.0094 | 0.1788 |
| LightGBM | 0.0838 | 0.1087 | -0.0182 | 0.1464 |
| season_xwOBA | 0.0853 | 0.1099 | -0.0419 | 0.1849 |
| last_14d_xwOBA | 0.0934 | 0.1201 | -0.2439 | 0.1521 |
| last_7d_xwOBA | 0.1058 | 0.1350 | -0.5703 | 0.1165 |

### Interpretation

Initial results suggest that pure recent-form baselines are noisy. Season-to-date xwOBA is a stronger simple baseline, while Ridge Regression provides a modest improvement in RMSE.

---

## Top-K Watchlist Evaluation

Because the final application is a hitter watchlist, ranking quality is also evaluated.

Top-K actual future 7-day xwOBA:

| Model | Top 10 | Top 20 | Top 50 | Top 100 |
|---|---:|---:|---:|---:|
| pred_ridge | 0.4323 | 0.3807 | 0.3682 | 0.3784 |
| pred_random_forest | 0.3886 | 0.3819 | 0.3628 | 0.3558 |
| pred_lightgbm | 0.3709 | 0.3680 | 0.3482 | 0.3487 |
| pred_season_xwOBA | 0.3522 | 0.3387 | 0.3619 | 0.3521 |
| pred_last_14d_xwOBA | 0.3718 | 0.3802 | 0.3425 | 0.3335 |
| pred_last_7d_xwOBA | 0.3256 | 0.3491 | 0.3383 | 0.3335 |

Ridge Regression produced the strongest Top-10 and Top-100 watchlist performance in the MVP experiment.

---

## Model Interpretation

Ridge coefficients and LightGBM feature importance suggest that the model uses both recent and season-level Statcast indicators.

Important feature groups include:

```text
season_xwOBA
season_wOBA
season_avg_exit_velocity
season_avg_launch_angle
last_14d_xwOBA
last_14d_avg_exit_velocity
last_14d_avg_launch_angle
last_7d_PA
last_14d_PA
season_PA
```

The interpretation should be cautious because rolling-window features are correlated. However, the results suggest that underlying contact quality features, such as exit velocity and launch angle, provide useful context beyond raw recent outcomes.

---

## Batter Weakness Module

The batter weakness module measures each hitter's performance against broad pitch groups:

```text
fastball
sinker
cutter
slider
curveball
changeup
other
```

For each hitter and pitch group, the system calculates:

```text
PA
xwOBA
wOBA
league-average xwOBA
xwOBA difference relative to league average
weakness score
```

The weakness score is defined as:

```text
weakness_score = league_xwOBA_against_pitch_group - hitter_xwOBA_against_pitch_group
```

Interpretation:

```text
positive weakness_score = hitter performs worse than league average
negative weakness_score = hitter performs better than league average
```

This module identifies which pitch types are likely to be a hitter's weakness or strength.

---

## Matchup Adjustment Module

The matchup module combines batter pitch-type weaknesses with pitcher pitch-mix tendencies.

For each pitcher, the project calculates pitch usage rates:

```text
pitcher_usage_fastball
pitcher_usage_slider
pitcher_usage_curveball
pitcher_usage_changeup
pitcher_usage_cutter
pitcher_usage_sinker
```

The matchup weakness score is calculated as:

```text
matchup_weakness_score =
Σ pitcher_pitch_usage[pitch_type] × batter_weakness[pitch_type]
```

A higher score means the opposing pitcher is more likely to attack the hitter's weaknesses.

### Historical Matchup Summary

| Matchup Label | n_matchups | avg_matchup_PA | actual_matchup_xwOBA | avg_matchup_weakness_score |
|---|---:|---:|---:|---:|
| Favorable | 8552 | 1.83 | 0.383 | -0.073 |
| Neutral | 17101 | 1.80 | 0.315 | 0.002 |
| Unfavorable | 8552 | 1.64 | 0.246 | 0.073 |

### Reliable Matchups with at Least 3 PA

| Matchup Label | n_matchups | avg_matchup_PA | actual_matchup_xwOBA | avg_matchup_weakness_score |
|---|---:|---:|---:|---:|
| Favorable | 2347 | 3.25 | 0.385 | -0.072 |
| Neutral | 4119 | 3.24 | 0.314 | -0.000 |
| Unfavorable | 1284 | 3.23 | 0.251 | 0.065 |

### Reliable Matchups with at Least 5 PA

| Matchup Label | n_matchups | avg_matchup_PA | actual_matchup_xwOBA | avg_matchup_weakness_score |
|---|---:|---:|---:|---:|
| Favorable | 183 | 5.64 | 0.377 | -0.068 |
| Neutral | 311 | 5.59 | 0.312 | -0.000 |
| Unfavorable | 90 | 5.42 | 0.266 | 0.062 |

The matchup score shows a consistent directional pattern: favorable matchups produce higher actual xwOBA, while unfavorable matchups produce lower actual xwOBA.

---

## Historical Daily Watchlist Demo

`07_daily_watchlist_demo.ipynb` creates a historical watchlist demo using the test period.

This notebook combines:

```text
Ridge predicted future 7d xwOBA
season and recent-form baselines
batter matchup context
signal labels
explanation reasons
```

The historical demo validates that model predictions and matchup context can be combined into one interpretable watchlist table.

---

## Schedule-Aware Daily Watchlist

`08_daily_schedule_watchlist.ipynb` extends the historical demo by integrating MLB schedule and probable starting pitcher information.

For a selected target date, the pipeline:

1. Retrieves MLB games and probable starting pitchers.
2. Maps MLB schedule team names to Statcast team abbreviations.
3. Identifies hitter candidates based on each hitter's latest team before the target date.
4. Merges Ridge-based future 7-day xwOBA predictions.
5. Merges batter pitch-type weakness profiles.
6. Merges the opposing probable pitcher's pitch mix.
7. Computes matchup weakness scores.
8. Assigns daily hitter signal labels.
9. Adds batter name lookup for readability.

The final schedule-aware watchlist includes:

```text
game_date
team
team_abbr
opponent_team
opponent_team_abbr
home_away
batter_name
batter
opposing_probable_pitcher
opposing_pitcher_id
pred_ridge
pred_season_xwOBA
pred_last_14d_xwOBA
matchup_weakness_score
matchup_label
signal
```

This turns the project from a historical evaluation workflow into a practical prototype for daily baseball analysis.

---

## Key Findings

1. **Short-term hitter performance is noisy.**  
   Recent 7-day and 14-day xwOBA baselines performed worse than season-to-date xwOBA.

2. **Ridge Regression is the best MVP forecasting model.**  
   It achieved the lowest RMSE and strongest Top-K watchlist results in the current experiment.

3. **Underlying Statcast indicators are useful.**  
   Ridge coefficients and LightGBM feature importance suggest that season-level contact quality and recent batted-ball profile contribute to prediction.

4. **Pitch-type matchup context is informative.**  
   The matchup weakness score produced clear separation between favorable, neutral, and unfavorable historical matchups.

5. **The final system is best viewed as a decision-support tool.**  
   It is not meant to perfectly predict short-term outcomes, but to organize model-based and matchup-based signals for hitter evaluation.

---

## Limitations

This MVP has several limitations:

1. The dataset currently covers only 2025-04-01 to 2025-05-31.
2. Short-term future 7-day xwOBA is inherently noisy.
3. The current hitter candidate pool uses latest team assignment, not confirmed starting lineups.
4. Probable pitcher data can be missing or change before game time.
5. The matchup module does not yet include bullpen pitchers.
6. Batter and pitcher handedness splits are not fully modeled.
7. Park factors, weather, injuries, lineup position, and batting order are not included.
8. Exit velocity and launch angle rolling features should be improved using batted-ball-count weighting.
9. The matchup score is contextual, not causal.

---

## Future Work

Planned improvements include:

1. Expand data to multiple seasons, such as 2023-2025.
2. Add confirmed daily lineups when available.
3. Add batter and pitcher handedness splits.
4. Add zone-level batter weakness.
5. Add park factor and weather context.
6. Add pitcher quality and bullpen context.
7. Improve batted-ball feature aggregation with batted-ball-count weighting.
8. Build a Streamlit dashboard for interactive daily watchlists.
9. Cache player name lookup tables for repeatable watchlist generation.
10. Evaluate whether matchup features improve the forecasting model directly.

---

## Repository Structure

```text
daily-mlb-hitter-forecasting/
│
├── data/
│   ├── raw/
│   ├── processed/
│   ├── features/
│   └── predictions/
│
├── notebooks/
│   ├── 01_data_collection.ipynb
│   ├── 02_rolling_features.ipynb
│   ├── 03_batter_weakness_profiles.ipynb
│   ├── 04_matchup_features.ipynb
│   ├── 05_model_training.ipynb
│   ├── 07_daily_watchlist_demo.ipynb
│   └── 08_daily_schedule_watchlist.ipynb
│
├── src/
├── reports/
├── dashboard/
├── README.md
├── requirements.txt
└── config.yaml
```

---

## Status

Current status: MVP complete.

Completed:

- Statcast data collection
- Plate-appearance-level data processing
- Rolling 7-day, 14-day, and season-to-date feature construction
- Future 7-day xwOBA target construction
- Baseline model evaluation
- Ridge Regression, Random Forest, and LightGBM training
- Top-K hitter watchlist evaluation
- Batter pitch-type weakness profile construction
- Pitcher pitch-mix construction
- Historical matchup weakness scoring
- Historical daily watchlist demo
- MLB schedule and probable pitcher integration
- Schedule-aware daily hitter watchlist prototype
- Batter name lookup for readable watchlist output

Next steps:

- Expand the dataset to multiple seasons
- Add handedness splits
- Add park factors and lineup position
- Improve batted-ball feature aggregation
- Build an interactive dashboard
