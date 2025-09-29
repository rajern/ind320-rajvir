import streamlit as st
import pandas as pd
from data_loader import load_data

st.title("Data table")

# Load cached data (time is index)
df = load_data()

# First month slice
first_m = df.index.min().to_period("M")
mask = (df.index.to_period("M") == first_m)
df_m = df.loc[mask]

# Build one row per variable with a sparkline of the first month
rows = []
for col in df.columns:                     # time is already index, all others are variables
    s = pd.to_numeric(df_m[col], errors="coerce").dropna()
    rows.append({
        "Variable": col,
        "Count": int(s.size),
        "First month": s.to_list()         # list for LineChartColumn
    })

table = pd.DataFrame(rows)

st.caption(f"First month shown: {first_m.start_time.date()} → {first_m.end_time.date()}")
st.dataframe(
    table,
    hide_index=True,
    use_container_width=True,
    column_config={
        "Variable": st.column_config.TextColumn("Variable"),
        "Count": st.column_config.NumberColumn("Points", format="%d"),
        "First month": st.column_config.LineChartColumn("First month"),
    },
)
