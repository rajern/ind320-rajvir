# data_loader.py
from pathlib import Path
import pandas as pd
import streamlit as st

@st.cache_data(show_spinner=False)
def load_data() -> pd.DataFrame:
    base = Path(__file__).resolve().parent              # assignment_1/
    csv_path = base / "open-meteo-subset.csv"           # CSV lives here

    df = pd.read_csv(csv_path, parse_dates=["time"]).set_index("time").sort_index()
    return df
