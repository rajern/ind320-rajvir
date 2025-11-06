from pathlib import Path
import pandas as pd
import streamlit as st

# Cache function for loading the Open-Meteo subset data
@st.cache_data(show_spinner=False)
def load_open_meteo() -> pd.DataFrame:
    data_path = Path(__file__).parent.parent / "data" / "open-meteo-subset.csv"
    df = pd.read_csv(data_path, parse_dates=["time"])
    df.set_index("time", inplace=True)
    return df

