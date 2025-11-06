from pathlib import Path
import pandas as pd
import streamlit as st

DATAFILE = Path(__file__).with_name("open-meteo-subset.csv")

@st.cache_data(show_spinner=False)
def load_data() -> pd.DataFrame:
    """Load local CSV, parse time, set as index, and return a tidy DataFrame."""
    if not DATAFILE.exists():
        st.error(f"Missing data file: {DATAFILE}")
        st.stop()

    df = pd.read_csv(DATAFILE, parse_dates=["time"])
    df.set_index("time", inplace=True)
    df.sort_index(inplace=True)
    return df
