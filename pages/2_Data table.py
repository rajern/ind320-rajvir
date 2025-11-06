import streamlit as st
import pandas as pd
from data_loader import load_open_meteo

st.title("Data table")

# Load data with cache function from data_loader.py
df = load_open_meteo()

# Keep only the first month in the data
m_df = df[df.index.to_period("M") == df.index.min().to_period("M")]

# Build a small table: one row per column + sparkline data for that month
table = pd.DataFrame({
    "Variable": df.columns,
    "First month": [m_df[c].tolist() for c in df.columns],
})

# Show the table with a line chart cell for each row
st.dataframe(
    table,
    hide_index=True,
    use_container_width=True,
    column_config={"First month": st.column_config.LineChartColumn("First month")},
)
