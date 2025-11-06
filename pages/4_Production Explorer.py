import streamlit as st
import pandas as pd
import matplotlib.pyplot as plt
from datetime import datetime
from pymongo import MongoClient

st.title("Production explorer")

# Read URI from secrets.
client = MongoClient(st.secrets["MONGODB_URI"])
db = client["elhub2021"]

# Try the common collection name first, then a fallback
col_name = "production_per_group_hour"
if col_name not in db.list_collection_names():
    col_name = "prod_by_group_hour"
col = db[col_name]

# Get available areas (fall back to NO1–NO5 if not found)
try:
    AREAS = sorted([a for a in col.distinct("pricearea") if a])
except Exception:
    AREAS = ["NO1", "NO2", "NO3", "NO4", "NO5"]

# Controls 
area = st.radio("Price area", AREAS, horizontal=True, index=AREAS.index("NO3") if "NO3" in AREAS else 0)
left, right = st.columns(2)

# Piechart: total 2021 by production group
with left:
    st.subheader("Share by group (2021)")
    pipe = [
        {"$match": {
            "pricearea": area,
            "starttime": {"$gte": datetime(2021, 1, 1), "$lt": datetime(2022, 1, 1)}
        }},
        {"$group": {"_id": "$productiongroup", "kwh": {"$sum": "$quantitykwh"}}},
        {"$sort": {"kwh": -1}}
    ]
    rows = list(col.aggregate(pipe))
    if not rows:
        st.warning("No data found for 2021.")
    else:
        labels = [r["_id"] for r in rows]
        sizes = [r["kwh"] for r in rows]
        fig, ax = plt.subplots()
        ax.pie(sizes, labels=labels, autopct="%1.1f%%", startangle=90)
        ax.set_title(f"{area} – 2021")
        ax.axis("equal")
        st.pyplot(fig, clear_figure=True)

# Linechart: hourly in one month, one line per group
with right:
    st.subheader("Hourly lines by month")
    month = st.selectbox("Month", list(range(1, 13)), format_func=lambda m: f"{m:02d}")

    # Let user pick groups for this area
    groups = sorted([g for g in col.distinct("productiongroup", {"pricearea": area}) if g])
    pick = st.multiselect("Production group(s)", groups, default=groups)

    start = datetime(2021, month, 1)
    end = datetime(2022, 1, 1) if month == 12 else datetime(2021, month + 1, 1)

    match = {"pricearea": area, "starttime": {"$gte": start, "$lt": end}}
    if pick:
        match["productiongroup"] = {"$in": pick}

    pipe = [
        {"$match": match},
        {"$group": {"_id": {"t": "$starttime", "g": "$productiongroup"},
                    "kwh": {"$sum": "$quantitykwh"}}}
    ]
    rows = list(col.aggregate(pipe))

    if not rows:
        st.info("No hourly data for this selection.")
    else:
        # Make a small DataFrame and pivot to wide format for plotting
        data = [{"time": r["_id"]["t"], "group": r["_id"]["g"], "kwh": r["kwh"]} for r in rows]
        df = pd.DataFrame(data)
        wide = df.pivot(index="time", columns="group", values="kwh").sort_index()

        fig, ax = plt.subplots()
        wide.plot(ax=ax)  
        ax.set_title(f"{area} – {2021}-{month:02d}")
        ax.set_xlabel("Time")
        ax.set_ylabel("kWh")
        ax.grid(True)
        st.pyplot(fig, clear_figure=True)

# Small note
with st.expander("About"):
    st.write("Data: Elhub 2021.")