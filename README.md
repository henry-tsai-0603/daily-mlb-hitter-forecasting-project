# Daily MLB Hitter Forecasting with Batter Weakness and Matchup Adjustment

## Project Overview

This project builds a daily MLB hitter forecasting system that predicts each hitter's future 7-day xwOBA using rolling Statcast indicators, season-to-date baselines, and trend features.

The project also includes a batter weakness and matchup-adjustment module that evaluates whether today's opposing pitcher profile creates a favorable or unfavorable matchup.

## Research Questions

1. Can recent 7-day and 14-day Statcast features predict a hitter's future 7-day xwOBA?
2. Do rolling Statcast indicators outperform simple season-to-date or recent-form baselines?
3. Can batter pitch-type weakness and opposing pitcher pitch mix improve daily matchup interpretation?
4. Which hitters should be classified as hot candidates, bounce-back candidates, regression risks, or weakness-matchup alerts?

## Project Phases

### Phase 1: Short-Term Hitter Forecasting Core

Goal: Predict future 7-day xwOBA using:
- Recent 7-day features
- Recent 14-day features
- Season-to-date baseline features
- Trend/deviation features

Models:
- Season-to-date baseline
- Last 7-day baseline
- Last 14-day baseline
- Ridge Regression
- Random Forest
- XGBoost / LightGBM

Evaluation:
- MAE
- RMSE
- R²
- Spearman correlation
- Top-K hitter ranking analysis

### Phase 2: Batter Weakness and Matchup Adjustment

Goal: Build a daily matchup module using:
- Batter pitch-type weakness profiles
- Opposing pitcher pitch-mix profiles
- Matchup weakness score

Output:
- Daily hitter watchlist
- Hot Candidate
- Bounce-back Candidate
- Regression Risk
- Weakness Matchup Alert

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
│   ├── 06_model_evaluation.ipynb
│   └── 07_daily_watchlist_demo.ipynb
│
├── src/
│   ├── data_loader.py
│   ├── feature_engineering.py
│   ├── weakness_profile.py
│   ├── matchup_score.py
│   ├── build_dataset.py
│   ├── train_model.py
│   ├── evaluate.py
│   └── predict_today.py
│
├── models/
│   └── saved_models/
│
├── reports/
│   ├── figures/
│   └── final_report.md
│
├── dashboard/
│   └── app.py
│
├── config.yaml
├── requirements.txt
└── README.md
```

## Data Sources

Primary:
- Statcast / Baseball Savant
- pybaseball

Optional for Phase 2:
- MLB Stats API for schedule and probable pitchers

## MVP Scope

The first MVP focuses on:
1. Hitters only
2. Future 7-day xwOBA prediction
3. Rolling 7-day and 14-day features
4. Season-to-date baselines
5. Baseline and ML model comparison
6. Pitch-type batter weakness module
7. Daily hitter watchlist demo

## Planned Output

Example daily hitter watchlist:

| Player | Team | Opponent SP | Predicted 7d xwOBA | Matchup Score | Signal | Reason |
|---|---|---|---:|---:|---|---|
| Player A | NYY | Pitcher X | .385 | Favorable | Hot Candidate | Recent contact quality is strong and matchup avoids weakness |
| Player B | LAD | Pitcher Y | .345 | Favorable | Bounce-back | Recent result is poor but xwOBA and hard-hit rate remain strong |
| Player C | CHC | Pitcher Z | .302 | Unfavorable | Weakness Alert | Opposing pitcher throws many sliders, hitter's main weakness |

## How to Run

```bash
pip install -r requirements.txt
```

Then run notebooks in order:

```text
01_data_collection.ipynb
02_rolling_features.ipynb
05_model_training.ipynb
06_model_evaluation.ipynb
```

Phase 2 notebooks:

```text
03_batter_weakness_profiles.ipynb
04_matchup_features.ipynb
07_daily_watchlist_demo.ipynb
```

## Resume Description

Built a daily MLB hitter forecasting system using Statcast data to predict future 7-day xwOBA from rolling 7-day, 14-day, and season-to-date features.

Developed a batter weakness and matchup-adjustment module by combining hitter pitch-type performance profiles with opposing pitcher pitch-mix tendencies.

Generated interpretable daily hitter watchlists categorizing players into hot candidates, bounce-back candidates, regression risks, and weakness-matchup alerts.
