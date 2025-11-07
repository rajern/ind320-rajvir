from pathlib import Path
import pandas as pd
import streamlit as st
from pymongo import MongoClient

# Cache function for loading the Open-Meteo subset data
@st.cache_data(show_spinner=False)
def load_open_meteo() -> pd.DataFrame:
    data_path = Path(__file__).parent.parent / "data" / "open-meteo-subset.csv"
    df = pd.read_csv(data_path, parse_dates=["time"])
    df.set_index("time", inplace=True)
    return df

# Cache function for loading production data from MongoDB (elhub2021 / production_per_group_hour)
@st.cache_data
def load_elhub_api_data():
    client = MongoClient(st.secrets["MONGODB_URI"])
    db = client["elhub2021"]
    col = db["production_per_group_hour"]

    # Read all documents, drop the internal MongoDB _id field
    records = list(col.find({}, {"_id": 0}))
    client.close()

    # Convert to DataFrame and ensure starttime is a proper datetime column
    df = pd.DataFrame(records)
    df["starttime"] = pd.to_datetime(df["starttime"])
    return df