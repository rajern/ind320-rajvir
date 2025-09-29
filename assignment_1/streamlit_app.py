import streamlit as st
import pandas as pd
from data_loader import load_data

st.set_page_config(page_title="IND320 App", layout="wide")

st.title("IND320 – Assignment App")

# Load cached data
df = load_data()

# Basic info
c1, c2, c3 = st.columns(3)
c1.metric("Rows", f"{len(df):,}")
c2.metric("Columns", df.shape[1])
c3.metric("Date range", f"{df.index.min().date()} → {df.index.max().date()}")

st.subheader("Preview (first 20 rows)")
st.dataframe(df.head(20), use_container_width=True)

st.subheader("Links")
st.markdown("- **GitHub:** https://github.com/rajern/ind320-rajvir")
st.markdown("- **Notebook/PDF:** https://ind320-rajvir-7xhejyuxheedg6tbdqwx3h.streamlit.app/")