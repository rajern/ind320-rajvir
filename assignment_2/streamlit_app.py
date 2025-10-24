import streamlit as st
import pandas as pd
from data_loader import load_data

st.set_page_config(page_title="IND320 App", layout="wide")

st.title("IND320 – Assignment App")

# Load cached data
df = load_data()

st.subheader("Preview (first 20 rows)")
st.dataframe(df.head(20), use_container_width=True)

st.subheader("Links")
st.markdown("- **GitHub:** <https://github.com/rajern/ind320-rajvir>")