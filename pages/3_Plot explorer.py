import streamlit as st
import pandas as pd
import plotly.express as px
from data_loader import load_open_meteo

st.title("Plot explorer")

# Load data with cache function from data_loader.py
df = load_open_meteo() 

# ---- Controls ----
options = ["All columns"] + list(df.columns)
choice = st.selectbox("Select column", options, index=0)

months = sorted(df.index.to_period("M").unique())
labels = [str(m) for m in months]

start_label, end_label = st.select_slider(
    "Select months",
    options=labels,
    value=(labels[0], labels[0])  # default = first month
)

# ---- Subset by month range ----
start_p = pd.Period(start_label, freq="M")
end_p   = pd.Period(end_label,   freq="M")
mask = (df.index.to_period("M") >= start_p) & (df.index.to_period("M") <= end_p)
d = df.loc[mask]

# ---- Plot using plotly ----
if choice == "All columns":
    fig = px.line(
        d,
        x=d.index,
        y=d.columns,
        title="All columns",
        labels={"value": "Value", "variable": "Variable", "x": "Time"},
    )
else:
    fig = px.line(
        d,
        x=d.index,
        y=choice,
        title=choice,
        labels={"value": choice, "x": "Time"},
    )

fig.update_layout(
    template="plotly_white",
    xaxis_title="Time",
    yaxis_title="Value",
    legend_title_text="",
    margin=dict(l=20, r=20, t=40, b=20),
    height=450,
)

st.plotly_chart(fig, use_container_width=True)
