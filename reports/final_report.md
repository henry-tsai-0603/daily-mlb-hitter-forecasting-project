# Daily MLB Hitter Forecasting with Batter Weakness and Matchup Adjustment

## 1. Introduction

Short-term hitter performance is difficult to evaluate because baseball outcomes are noisy. A hitter may appear hot over a few games because of favorable batted-ball luck, weak opposing pitchers, or a small number of plate appearances. Similarly, a hitter may look cold even when his underlying contact quality remains strong.

This project builds a prototype system for short-term MLB hitter evaluation. The system combines two components:

1. **Short-term hitter forecasting**: predicts each hitter's future 7-day xwOBA using rolling Statcast indicators.
2. **Batter weakness and matchup adjustment**: evaluates whether a hitter's pitch-type weaknesses align with the opposing pitcher's pitch mix.

The final goal is to generate an interpretable **daily hitter watchlist** that identifies hot candidates, bounce-back candidates, regression risks, and unfavorable matchup alerts.

---

## 2. Problem Definition

The main forecasting task is:

> Given a hitter's recent 7-day performance, recent 14-day performance, and season-to-date Statcast profile, predict his offensive quality over the next 7 days.

The target variable is:

```text
future_7d_xwOBA
```

For each hitter and prediction date, the model uses only information available before the prediction date. The target is calculated from the hitter's plate appearances over the following 7 days.

The broader applied question is:

> Can recent form, season baseline, and matchup context be combined into a useful daily hitter evaluation tool?

---

## 3. Data

The project uses public MLB Statcast data collected through `pybaseball`.

Current MVP data range:

```text
2025-04-01 to 2025-05-31
```

The raw data is pitch-level Statcast data. It is processed into plate-appearance-level and hitter-date-level tables.

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
launch_speed
launch_angle
estimated_woba_using_speedangle
woba_value
```

The raw data files are excluded from GitHub because they can be large.

---

## 4. Data Processing Pipeline

The data pipeline has the following structure:

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

### 4.1 Plate Appearance Filtering

Statcast data is pitch-level, so not every row represents a completed plate appearance. The project keeps rows where:

```python
events.notna()
```

These rows represent completed plate appearances.

### 4.2 xwOBA Value Construction

The project creates a working `xwoba_value` variable:

```python
xwoba_value = estimated_woba_using_speedangle.fillna(woba_value)
```

This means:

- Batted-ball events use expected value from Statcast when available.
- Walks, strikeouts, and other non-batted-ball events use their actual wOBA value.

This gives a practical approximation of offensive quality for rolling aggregation.

---

## 5. Feature Engineering

The model uses one row per hitter per prediction date.

```text
one row = one hitter on one prediction date
```

For each prediction date `t`:

```text
Past features: dates before t
Target: dates after t
```

This avoids data leakage.

### 5.1 Recent Form Features

Recent form features describe short-term hitter performance:

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

### 5.2 Season-to-Date Baseline Features

Season-to-date features represent the hitter's longer-term performance level:

```text
season_PA
season_xwOBA
season_wOBA
season_avg_exit_velocity
season_avg_launch_angle
```

### 5.3 Trend and Deviation Features

Trend features compare recent form with season baseline:

```text
xwOBA_diff_7d_vs_season
xwOBA_diff_14d_vs_season
wOBA_diff_7d_vs_season
wOBA_diff_14d_vs_season
```

These features measure whether a hitter's recent performance is above or below his season-to-date level.

---

## 6. Forecasting Models

The project compares simple baselines with machine learning models.

### 6.1 Baseline Models

The baseline models are:

```text
prediction = season_xwOBA
prediction = last_7d_xwOBA
prediction = last_14d_xwOBA
```

These baselines answer whether the machine learning models improve beyond simple recent or season-level averages.

### 6.2 Machine Learning Models

The machine learning models are:

```text
Ridge Regression
Random Forest
LightGBM
```

Ridge Regression is used as a regularized linear model. Random Forest and LightGBM are used as nonlinear tree-based comparison models.

---

## 7. Model Evaluation

The dataset is split chronologically. For the current MVP experiment:

```text
Train: prediction dates before 2025-05-11
Test: prediction dates from 2025-05-11 onward
```

This preserves the forecasting setting and avoids using future information in training.

### 7.1 Evaluation Metrics

The models are evaluated using:

```text
MAE
RMSE
R²
Spearman correlation
Top-K actual future xwOBA
```

MAE and RMSE measure numerical prediction error. Spearman correlation measures ranking quality. Top-K evaluation is important because the final application is a hitter watchlist.

---

## 8. Forecasting Results

Initial model results:

| Model | MAE | RMSE | R² | Spearman |
|---|---:|---:|---:|---:|
| Ridge Regression | 0.0823 | 0.1064 | 0.0238 | 0.1847 |
| Random Forest | 0.0828 | 0.1072 | 0.0094 | 0.1788 |
| LightGBM | 0.0838 | 0.1087 | -0.0182 | 0.1464 |
| season_xwOBA | 0.0853 | 0.1099 | -0.0419 | 0.1849 |
| last_14d_xwOBA | 0.0934 | 0.1201 | -0.2439 | 0.1521 |
| last_7d_xwOBA | 0.1058 | 0.1350 | -0.5703 | 0.1165 |

### 8.1 Interpretation

The results show that:

1. **Recent-only baselines are noisy.**  
   `last_7d_xwOBA` and `last_14d_xwOBA` perform worse than `season_xwOBA`.

2. **Season-to-date xwOBA is a strong simple baseline.**  
   It performs better than pure recent-form baselines.

3. **Ridge Regression provides the best MVP result.**  
   Ridge Regression achieves the lowest RMSE and provides a modest improvement over the season baseline.

This suggests that combining season baseline, recent form, and trend features provides more stable short-term forecasting than relying on recent performance alone.

---

## 9. Top-K Watchlist Evaluation

Because the final application is a hitter watchlist, the project also evaluates whether models can identify high-performing future hitters.

The Top-K table shows the actual average future 7-day xwOBA among the top K hitters ranked by each model.

| Model | Top 10 | Top 20 | Top 50 | Top 100 |
|---|---:|---:|---:|---:|
| pred_ridge | 0.4323 | 0.3807 | 0.3682 | 0.3784 |
| pred_random_forest | 0.3886 | 0.3819 | 0.3628 | 0.3558 |
| pred_lightgbm | 0.3709 | 0.3680 | 0.3482 | 0.3487 |
| pred_season_xwOBA | 0.3522 | 0.3387 | 0.3619 | 0.3521 |
| pred_last_14d_xwOBA | 0.3718 | 0.3802 | 0.3425 | 0.3335 |
| pred_last_7d_xwOBA | 0.3256 | 0.3491 | 0.3383 | 0.3335 |

### 9.1 Interpretation

Ridge Regression produces the strongest Top-10 and Top-100 watchlist results. This supports using Ridge Regression as the current MVP model for the daily hitter watchlist.

---

## 10. Model Interpretation

### 10.1 Ridge Coefficients

The Ridge model uses standardized features. The largest coefficient magnitudes include:

```text
last_14d_avg_launch_angle
last_7d_PA
season_avg_exit_velocity
season_avg_launch_angle
last_14d_PA
season_PA
season_xwOBA
last_14d_xwOBA
last_14d_avg_exit_velocity
```

This suggests that the model uses both:

- recent playing time and recent batted-ball profile
- season-level contact quality and offensive baseline

However, many rolling-window features are correlated, so individual coefficient signs should be interpreted cautiously.

### 10.2 LightGBM Feature Importance

LightGBM also places high importance on:

```text
season_avg_launch_angle
season_avg_exit_velocity
season_wOBA
season_xwOBA
last_14d_avg_launch_angle
season_PA
last_7d_avg_exit_velocity
last_14d_avg_exit_velocity
```

This supports the idea that underlying Statcast indicators, especially exit velocity and launch angle, contribute useful information beyond raw recent results.

---

## 11. Batter Weakness Profile

The second component of the project builds hitter pitch-type weakness profiles.

Pitch types are grouped into broader categories:

```text
fastball
sinker
cutter
slider
curveball
changeup
other
```

For each hitter and pitch group, the project calculates:

```text
PA
xwOBA
wOBA
league-average xwOBA
xwOBA vs league average
weakness score
```

The weakness score is defined as:

```text
weakness_score = league_xwOBA_against_pitch_group - hitter_xwOBA_against_pitch_group
```

Interpretation:

```text
positive weakness_score → hitter performs worse than league average
negative weakness_score → hitter performs better than league average
```

This module identifies which pitch types are likely to be a hitter's weakness or strength.

---

## 12. Matchup Adjustment Module

The matchup module combines:

```text
batter pitch-type weakness
+
pitcher pitch mix
```

For each pitcher, the project calculates pitch usage rates:

```text
pitcher_usage_fastball
pitcher_usage_slider
pitcher_usage_curveball
pitcher_usage_changeup
pitcher_usage_cutter
pitcher_usage_sinker
```

The matchup weakness score is:

```text
matchup_weakness_score =
Σ pitcher_pitch_usage[pitch_type] × batter_weakness[pitch_type]
```

A higher score means the opposing pitcher is more likely to throw pitch types that match the hitter's weaknesses.

---

## 13. Matchup Results

### 13.1 All Historical Batter-Pitcher Matchups

| Matchup Label | n_matchups | avg_matchup_PA | actual_matchup_xwOBA | actual_matchup_wOBA | avg_matchup_weakness_score |
|---|---:|---:|---:|---:|---:|
| Favorable | 8552 | 1.83 | 0.383 | 0.383 | -0.073 |
| Neutral | 17101 | 1.80 | 0.315 | 0.319 | 0.002 |
| Unfavorable | 8552 | 1.64 | 0.246 | 0.253 | 0.073 |

### 13.2 Matchups with at Least 3 PA

| Matchup Label | n_matchups | avg_matchup_PA | actual_matchup_xwOBA | actual_matchup_wOBA | avg_matchup_weakness_score |
|---|---:|---:|---:|---:|---:|
| Favorable | 2347 | 3.25 | 0.385 | 0.380 | -0.072 |
| Neutral | 4119 | 3.24 | 0.314 | 0.317 | -0.000 |
| Unfavorable | 1284 | 3.23 | 0.251 | 0.254 | 0.065 |

### 13.3 Matchups with at Least 5 PA

| Matchup Label | n_matchups | avg_matchup_PA | actual_matchup_xwOBA | actual_matchup_wOBA | avg_matchup_weakness_score |
|---|---:|---:|---:|---:|---:|
| Favorable | 183 | 5.64 | 0.377 | 0.348 | -0.068 |
| Neutral | 311 | 5.59 | 0.312 | 0.316 | -0.000 |
| Unfavorable | 90 | 5.42 | 0.266 | 0.271 | 0.062 |

### 13.4 Interpretation

The matchup module produces a clear directional pattern:

```text
Favorable matchups → highest actual xwOBA
Neutral matchups → middle actual xwOBA
Unfavorable matchups → lowest actual xwOBA
```

This pattern remains visible even when filtering to matchups with at least 3 or 5 plate appearances.

This suggests that combining batter pitch-type weaknesses with pitcher pitch mix provides useful matchup context.

However, this should not be interpreted as a standalone causal result. Batter-pitcher matchup outcomes are affected by many other factors, including pitcher quality, handedness, ballpark, count, game context, and small-sample variation.

---

## 14. Daily Watchlist Demo

The final demo combines:

```text
Ridge predicted future 7d xwOBA
season and recent-form baselines
batter matchup context
signal labels
explanation reasons
```

The watchlist classifies hitters into categories such as:

```text
Hot Candidate
Bounce-back Candidate
Regression Risk
Weakness Matchup Alert
Neutral
```

The MVP demo currently uses a historical test period rather than real daily schedule and probable starters. The next version will connect this module to actual MLB daily schedules.

---

## 15. Key Findings

### Finding 1: Recent hitter performance is noisy

Recent-only baselines perform worse than season-to-date xwOBA. This suggests that short-term hitter performance should not be evaluated using recent results alone.

### Finding 2: Ridge Regression is the best MVP forecasting model

Ridge Regression achieves the lowest RMSE and the strongest Top-K watchlist performance in the current experiment.

### Finding 3: Underlying Statcast indicators are useful

Exit velocity, launch angle, season xwOBA, and rolling contact-quality features appear important in both Ridge and LightGBM interpretation.

### Finding 4: Pitch-type matchup context is informative

The matchup weakness score separates favorable, neutral, and unfavorable historical matchups in the expected direction.

### Finding 5: The system is more useful as a decision-support tool than as a deterministic predictor

The goal is not to perfectly predict short-term performance. Instead, the system provides structured signals to support hitter evaluation and matchup interpretation.

---

## 16. Limitations

This MVP has several limitations:

1. **Limited data range**  
   The current experiment only uses data from 2025-04-01 to 2025-05-31.

2. **Short-term target noise**  
   Future 7-day xwOBA is inherently noisy because hitters may have few plate appearances in a short window.

3. **No real schedule integration yet**  
   The watchlist demo does not yet use real MLB daily schedules or probable starting pitchers.

4. **No bullpen modeling**  
   The matchup module currently focuses on pitcher pitch mix in historical data and does not model expected bullpen matchups.

5. **No handedness splits yet**  
   Batter and pitcher handedness are available but not yet fully integrated into the weakness score.

6. **No ballpark or weather context**  
   Park effects, weather, and game environment are not included.

7. **Batted-ball aggregation can be improved**  
   Exit velocity and launch angle rolling features should be weighted by batted-ball count instead of averaging daily averages.

8. **The matchup score is contextual, not causal**  
   Favorable and unfavorable labels should be interpreted as matchup context, not as proof of causal effect.

---

## 17. Future Work

Future improvements include:

1. Expand the dataset to multiple seasons, such as 2023-2025.
2. Integrate MLB schedule and probable starting pitchers.
3. Add batter and pitcher handedness splits.
4. Add zone-level batter weakness.
5. Add park factors and weather context.
6. Add pitcher quality and bullpen context.
7. Improve batted-ball feature aggregation using batted-ball-count weighting.
8. Evaluate whether matchup features improve the forecasting model directly.
9. Build an interactive Streamlit dashboard.
10. Add player name lookup tables for cleaner display.
11. Evaluate model stability across different train/test periods.
12. Add confidence or uncertainty labels for predictions.

---

## 18. Conclusion

This project builds an end-to-end prototype for short-term MLB hitter forecasting and matchup-aware hitter evaluation.

The forecasting model shows that recent hitter performance is noisy and that season-to-date baselines remain strong. Ridge Regression provides the best MVP forecasting performance by combining recent form, season baseline, and trend features.

The batter weakness and matchup adjustment module provides an additional layer of baseball context. By combining hitter pitch-type weakness with pitcher pitch mix, the system identifies favorable and unfavorable historical matchups with clear directional separation in actual xwOBA.

The current MVP demonstrates a complete workflow:

```text
Statcast data collection
→ PA-level processing
→ rolling feature engineering
→ forecasting model training
→ batter weakness profiling
→ matchup scoring
→ daily watchlist demo
```

The next step is to connect the system to real MLB daily schedules and probable starters so that the watchlist can be generated for current games.
