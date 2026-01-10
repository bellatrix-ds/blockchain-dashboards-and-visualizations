import pandas as pd
import streamlit as st
import matplotlib.pyplot as plt
import matplotlib.dates as mdates
import matplotlib.ticker as mtick

# -----------------------------
# Load Data
# -----------------------------
df = pd.read_csv(
    "https://raw.githubusercontent.com/bellatrix-ds/blockchain-dashboards-and-visualizations/main/04_DeFi_Lending_Protocol/final_data.csv"
)

df['date'] = pd.to_datetime(df['date'])

# Keep data after 2025
df = df[df['date'] >= '2025-01-01']

# -----------------------------
# Title & Description
# -----------------------------
st.title("📊 DeFi Lending Protocol Dashboard")
st.markdown("Visualize Total Value Locked (TVL) across chains after **2025**")

st.markdown("### 🧑‍💻 About This Dashboard")
st.markdown("""
This dashboard visualizes the metrics of lending protocol 
across multiple blockchains starting from 2025.  
You can filter by chain and select a time period (last 3, 6, or 12 months).
""")



# -----------------------------
# Sidebar Filters
# -----------------------------
st.sidebar.header("🔍 Filters")

# Time Range
st.sidebar.subheader("⏳ Time Range")
time_range = st.sidebar.selectbox(
    "Select Time Period:",
    ["Last 3 Months", "Last 6 Months", "Last 12 Months"],
    index=2
)

# Chain Selector
st.sidebar.subheader("🔗 Chain")
chain_options = ["All"] + sorted(df["chain"].unique())
selected_chain = st.sidebar.selectbox("Choose a chain:", chain_options)

# -----------------------------
# Filter Data
# -----------------------------
df_filtered = df.copy()

# Time filter
months_map = {
    "Last 3 Months": 3,
    "Last 6 Months": 6,
    "Last 12 Months": 12
}

cutoff = df_filtered['date'].max() - pd.DateOffset(months=months_map[time_range])
df_filtered = df_filtered[df_filtered['date'] >= cutoff]

# Chain filter
if selected_chain != "All":
    df_filtered = df_filtered[df_filtered['chain'] == selected_chain]

# -----------------------------
# Plot
# -----------------------------

import plotly.express as px

st.subheader("📈 TVL Over Time")

if df_filtered.empty:
    st.warning("No data available for the selected filters.")
else:
    fig = px.line(
        df_filtered,
        x="date",
        y="totalLiquidityUSD",
        color="chain",
        labels={
            "date": "Date",
            "totalLiquidityUSD": "TVL (USD)",
            "chain": "Chain"
        },
        hover_data={
            "totalLiquidityUSD": ":.3s",  # e.g., 3.25B
            "chain": True,
            "date": False  # already shown
        }
    )

    # Format y-axis (e.g., $5B)
    fig.update_layout(
        yaxis_tickformat="$~s",
        hovermode="x unified",
        showlegend=False,  # 🔥 hide legend
        margin=dict(t=50, r=20, l=10, b=40)
    )

    st.plotly_chart(fig, use_container_width=True)
