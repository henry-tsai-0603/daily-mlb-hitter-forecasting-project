# Daily MLB Hitter Forecasting with Batter Weakness and Matchup Adjustment

## Project Overview

This project builds a daily MLB hitter forecasting system using Statcast data. The goal is to predict a hitter's short-term offensive performance and provide interpretable matchup context.

The system has two main components:

1. **Short-term hitter forecasting model**  
   Predicts each hitter's future 7-day xwOBA using rolling 7-day, rolling 14-day, season-to-date, and trend-based Statcast features.

2. **Batter weakness and matchup adjustment module**  
   Measures each hitter's pitch-type weaknesses and combines them with opposing pitcher pitch-mix tendencies to identify favorable and unfavorable matchups.

The final output is a prototype **daily hitter watchlist** that categorizes hitters into interpretable signals such as hot candidates, bounce-back candidates, regression risks, and matchup alerts.

---

## Research Questions

This project investigates the following questions:

1. Can rolling Statcast indicators predict a hitter's future 7-day xwOBA?
2. Are recent 7-day or 14-day hitter statistics more useful than season-to-date baselines?
3. Can a simple machine learning model improve short-term hitter forecasting over baseline approaches?
4. Can batter pitch-type weakness and pitcher pitch mix provide useful matchup context?
5. Can the forecasting model and matchup module be combined into an interpretable daily hitter watchlist?

---

## Data

The project uses public MLB Statcast data collected through `pybaseball`.

Current MVP data range:

```text
2025-04-01 to 2025-05-31