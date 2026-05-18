"""Streamlit dashboard placeholder.

Run:
    streamlit run dashboard/app.py
"""

import streamlit as st
import pandas as pd

st.set_page_config(page_title="Daily MLB Hitter Watchlist", layout="wide")

st.title("Daily MLB Hitter Watchlist")
st.write("This dashboard will display predicted future 7-day xwOBA, matchup scores, and signal labels.")

uploaded_file = st.file_uploader("Upload a watchlist CSV", type=["csv"])

if uploaded_file is not None:
    df = pd.read_csv(uploaded_file)
    st.dataframe(df)
else:
    st.info("Upload a prediction CSV from data/predictions/ to view the watchlist.")
