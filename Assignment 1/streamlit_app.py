import streamlit as st
import pandas as pd

st.set_page_config(page_title="IND320 – MWE", page_icon="📊", layout="centered")

st.title("IND320 – Minimum Working Example")
st.write("Deployed via Streamlit Community Cloud. Repo: GitHub → Streamlit → Deploy.")

with st.expander("Sample data preview"):
    df = pd.DataFrame({"A": [1, 2, 3, 4], "B": [10, 20, 30, 40]})
    st.dataframe(df)

st.line_chart(df)