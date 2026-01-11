import pandas as pd
import streamlit as st
import matplotlib.pyplot as plt
import matplotlib.dates as mdates
import matplotlib.ticker as mtick
import plotly.express as px

# -----------------------------
# Load Main TVL Data
# -----------------------------
df = pd.read_csv(
    "https://raw.githubusercontent.com/bellatrix-ds/blockchain-dashboards-and-visualizations/main/04_DeFi_Lending_Protocol/final_data.csv")

df['date'] = pd.to_datetime(df['date'])
df = df[df['date'] >= '2025-01-01']

# -----------------------------
# Load Yield TVL Token-level Data
# -----------------------------
df_yield = pd.read_csv("https://raw.githubusercontent.com/bellatrix-ds/blockchain-dashboards-and-visualizations/refs/heads/main/04_DeFi_Lending_Protocol/df_yeild_final.csv")

# -----------------------------
# Title & Description
# -----------------------------
st.title("📊 DeFi Lending Protocol Dashboard")


with st.container():
    st.markdown("### 🧑‍💻 About This Dashboard")
    st.info("""
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
# Layout with Two Columns
# -----------------------------
st.subheader("📈 TVL Metrics")

col1, col2 = st.columns(2)

# ---- Left: Line Chart ----
with col1:
    if df_filtered.empty:
        st.warning("No data available for the selected filters.")
    else:
        fig_line = px.line(
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
                "totalLiquidityUSD": ":.3s",
                "chain": True,
                "date": False
            }
        )
        fig_line.update_layout(
            yaxis_tickformat="$~s",
            hovermode="x unified",
            showlegend=False,
            margin=dict(t=40, r=20, l=10, b=40)
        )
        st.plotly_chart(fig_line, use_container_width=True)

# ---- Right: Bar Chart ----
with col2:
    fig_bar = px.bar(
        df_yield,
        x="symbol",
        y="tvlUsd",
        color="project",
        hover_data=["chain"],
        labels={
            "symbol": "Token",
            "tvlUsd": "TVL (USD)",
            "project": "Protocol"
        },
        title="TVL by Token & Protocol"
    )
    fig_bar.update_layout(yaxis_tickformat="$~s", xaxis_tickangle=-45)
    st.plotly_chart(fig_bar, use_container_width=True)
