import streamlit as st
import pandas as pd
import matplotlib.pyplot as plt
from data_loader import load_data

st.title("Plot explorer")

# Data
df = load_data()                     # time index

# --- Controls ---
cols = ["All columns"] + list(df.columns)
col_choice = st.selectbox("Select column", cols, index=0)

# Build month options from data
months = pd.Index(sorted(df.index.to_period("M").unique()))
# show as YYYY-MM strings
month_labels = months.astype(str).tolist()

# Range of months (subset), default = first month only
m_start, m_end = st.select_slider(
    "Select months",
    options=month_labels,
    value=(month_labels[0], month_labels[0])
)

# --- Subset by month range ---
start_p = pd.Period(m_start, freq="M")
end_p   = pd.Period(m_end,   freq="M")
mask = (df.index.to_period("M") >= start_p) & (df.index.to_period("M") <= end_p)
d = df.loc[mask]
st.caption(f"Showing: {start_p.start_time.date()} → {end_p.end_time.date()}  (rows: {len(d):,})")

# --- Plot ---
fig, ax = plt.subplots(figsize=(10, 4))

if col_choice == "All columns":
    # Optionally standardize to make scales comparable
    standardize = st.checkbox("Standardize (z-score)", value=True)
    plot_df = d.copy()
    if standardize and len(plot_df) > 0:
        plot_df = (plot_df - plot_df.mean()) / plot_df.std(ddof=0)

    plot_df.plot(ax=ax, linewidth=1)
    ax.set_title("All columns" + (" (standardized)" if standardize else ""))
    ax.set_ylabel("z-score" if standardize else "value")
else:
    d[col_choice].plot(ax=ax, linewidth=1)
    ax.set_title(col_choice)
    ax.set_ylabel(col_choice)

ax.set_xlabel("time")
ax.grid(True)
st.pyplot(fig, clear_figure=True)
