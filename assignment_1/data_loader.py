# data_loader.py
from pathlib import Path
import pandas as pd
import streamlit as st

CSV_PATH = Path("open-meteo-subset.csv")  # local CSV in repo root

@st.cache_data(show_spinner=False)  # caches the returned DataFrame for speed
def load_data() -> pd.DataFrame:
    """Read CSV, parse 'time', set as index; cached by Streamlit."""
    df = pd.read_csv(CSV_PATH, parse_dates=["time"])
    df = df.set_index("time").sort_index()
    return df
