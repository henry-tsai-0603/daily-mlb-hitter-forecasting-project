# Final Report Draft

## 1. Introduction

This project studies short-term MLB hitter performance forecasting using Statcast data.

## 2. Problem Definition

The main target is future 7-day xwOBA.

## 3. Data

Primary data comes from Statcast / Baseball Savant through pybaseball.

## 4. Feature Engineering

- Rolling recent-form features
- Season-to-date baseline features
- Trend/deviation features
- Batter pitch-type weakness profiles
- Matchup weakness scores

## 5. Models

- Season-to-date baseline
- Last 7-day baseline
- Last 14-day baseline
- Ridge Regression
- Random Forest
- XGBoost / LightGBM

## 6. Evaluation

- MAE
- RMSE
- R²
- Spearman correlation
- Top-K ranking analysis

## 7. Daily Watchlist Demo

This section will show daily hitter predictions and signal labels.

## 8. Limitations

- Short-term hitter performance is noisy.
- Playing time uncertainty is not fully modeled.
- First version focuses on hitters only.
- First version does not include bullpen, injury news, weather, or live-game updates.

## 9. Future Work

- Add probable starters and schedule integration.
- Add zone-level weakness.
- Add park factor and weather.
- Add pitcher and bullpen effects.
- Build Streamlit dashboard.
