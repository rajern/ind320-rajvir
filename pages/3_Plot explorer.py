import streamlit as st
import pandas as pd
import matplotlib.pyplot as plt
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

# ---- Plot ----
fig, ax = plt.subplots(figsize=(10, 4))
if choice == "All columns":
    d.plot(ax=ax)
    ax.set_title("All columns")
    ax.set_ylabel("value")
else:
    d[choice].plot(ax=ax)
    ax.set_title(choice)
    ax.set_ylabel(choice)

ax.set_xlabel("time")
ax.grid(True)
st.pyplot(fig)
