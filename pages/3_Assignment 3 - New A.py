import streamlit as st
import matplotlib.pyplot as plt
from statsmodels.tsa.seasonal import STL
import pandas as pd

from src.data_loader import load_elhub_api_data

st.title("Assignment 3 – STL and spectrogram")

# ---- Functions created in assignment3.ipynb ----

# Function for STL decomposition (LOESS) on Elhub production data
def plot_stl_elhub(
    df,
    area="NO3",
    group="hydro",
    period=24,
    seasonal=13,
    trend=365,
    robust=True,
    time_col="starttime",
    value_col="quantitykwh",
):
    # Filter for the chosen price area and production group
    sub = df[(df["pricearea"] == area) & (df["productiongroup"] == group)].copy()
    if sub.empty:
        raise ValueError("No data for this price area and production group.")

    # Make sure we have a sorted datetime index
    sub[time_col] = pd.to_datetime(sub[time_col])
    sub = sub.sort_values(time_col)
    series = sub.set_index(time_col)[value_col]

    # Force regular hourly frequency and fill small gaps
    series = series.asfreq("h")
    series = series.interpolate(limit_direction="both")

    # Run STL (Seasonal-Trend decomposition using LOESS)
    stl = STL(
        series,
        period=period,
        seasonal=seasonal,
        trend=trend,
        robust=robust,
    )
    result = stl.fit()

    # Standard decomposition plot from statsmodels
    fig = result.plot()
    fig.set_size_inches(9, 4)
    fig.suptitle(f"STL decomposition – {area}, {group}", fontsize=10)
    fig.tight_layout()

    return fig, result

# Function for creating a spectrogram from Elhub production data
def plot_spectrogram_elhub(
    df,
    area="NO4",
    group="hydro",
    window_length=24*7,   # window length in hours
    window_overlap=0.5,   # fraction of overlap between windows
):

    # Filter data for selected price area and production group
    mask = (df["pricearea"] == area) & (df["productiongroup"] == group)
    df_sel = df.loc[mask].sort_values("starttime")

    # Extract production series as numpy array
    x = df_sel["quantitykwh"].to_numpy(dtype=float)

    # Convert window parameters to integers for spectrogram
    nperseg = int(window_length)
    noverlap = int(window_length * window_overlap)

    # Create figure and axis
    fig, ax = plt.subplots(figsize=(10, 4))

    # Compute and plot the spectrogram 
    ax.specgram(x, NFFT=nperseg, Fs=1.0, noverlap=noverlap)

    # Add labels
    ax.set_title(f"Spectrogram – {area}, {group}")
    ax.set_xlabel("Time window")
    ax.set_ylabel("Frequency [cycles per hour]")

    return fig, ax

# ---- Load Elhub data and use price area from page 2 ----

df = load_elhub_api_data()

# Find available price areas
areas = sorted(df["pricearea"].dropna().unique().tolist())

# Use selection from "Production explorer" if available
current_area = st.session_state.get("pricearea", areas[0])
if current_area not in areas:
    current_area = areas[0]

st.write(f"Current price area: **{current_area}**")

# All production groups in this price area
groups = sorted(
    df.loc[df["pricearea"] == current_area, "productiongroup"]
      .dropna()
      .unique()
      .tolist()
)

# ---- Tabs for STL and Spectrogram ----
tab_stl, tab_spec = st.tabs(["STL", "Spectrogram"])

# ---------------- STL tab ----------------
with tab_stl:
    st.subheader("STL decomposition")

    group = st.selectbox("Production group", groups)

    period = st.number_input("Period (hours)", min_value=1, value=24, step=1)
    seasonal = st.number_input("Seasonal smoother", min_value=3, value=13, step=1)
    trend = st.number_input("Trend smoother", min_value=3, value=365, step=1)
    robust = st.checkbox("Robust", value=True)

    try:
        fig_stl, result = plot_stl_elhub(
            df,
            area=current_area,
            group=group,
            period=period,
            seasonal=seasonal,
            trend=trend,
            robust=robust,
        )
        st.pyplot(fig_stl, use_container_width=False)
    except ValueError as e:
        st.warning(str(e))

# ---------------- Spectrogram tab ----------------
with tab_spec:
    st.subheader("Spectrogram")

    group_spec = st.selectbox("Production group", groups, key="spec_group")

    window_length = st.number_input(
        "Window length (hours)",
        min_value=24,
        max_value=24 * 60,
        value=24 * 7,
        step=24,
    )
    window_overlap = st.slider(
        "Window overlap",
        min_value=0.0,
        max_value=0.9,
        value=0.5,
        step=0.1,
    )

    try:
        fig_spec, ax_spec = plot_spectrogram_elhub(
            df,
            area=current_area,
            group=group_spec,
            window_length=window_length,
            window_overlap=window_overlap,
        )
        st.pyplot(fig_spec)
    except ValueError as e:
        st.warning(str(e))
