import streamlit as st
import pandas as pd
from data_loader import load_data

st.title("Data table")

df = load_data()
m_df = df[df.index.to_period("M") == df.index.min().to_period("M")]

table = pd.DataFrame({
    "Variable": df.columns,
    "First month": [m_df[c].tolist() for c in df.columns],
})

st.dataframe(
    table,
    hide_index=True,
    use_container_width=True,
    column_config={"First month": st.column_config.LineChartColumn("First month")},
)
