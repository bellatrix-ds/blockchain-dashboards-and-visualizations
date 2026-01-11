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
st.set_page_config(layout="wide")

st.title("📊 DeFi Lending Protocol Dashboard")

st.markdown("""
<div style="
    background-color: #111111;
    padding: 20px 25px;
    border-radius: 10px;
    border: 1px solid #2a2a2a;
    color: white;
">
    <h4 style='margin-bottom: 5px;'>Upcoming Unlocks</h4>
    <p style='color: #b0b0b0; margin-top: 0;'>This dashboard visualizes the metrics of lending protocol across multiple blockchains starting from 2025.
You can filter by chain and select a time period (last 3, 6, or 12 months).</p>
</div>
""", unsafe_allow_html=True)


st.markdown("<div style='height: 50px;'></div>", unsafe_allow_html=True)

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

st.markdown("""
<hr style=" border-top: 1px solid white; margin-top: 10px;">
<h4 style="text-align: center; color: white;">💰 Protocol TVL Overview</h4>
<hr style="border: none; border-top: 1px solid white; margin-bottom: 10px;">
""", unsafe_allow_html=True)


col1, col2 = st.columns(2)

# --- Left Chart: TVL over time ---
with col1:
    fig = px.line(
        df_filtered,
        x="date",
        y="totalLiquidityUSD",
        color="chain",
        labels={"date": "Date", "totalLiquidityUSD": "TVL (USD)", "chain": "Chain"},
        hover_data={"totalLiquidityUSD": ":.3s", "chain": True, "date": False},
        title="TVL Distribution by Chain Over Time"
    )
    fig.update_layout(
        yaxis_tickformat="$~s",
        hovermode="x unified",
        showlegend=False,
        margin=dict(t=50, r=20, l=10, b=40),
        xaxis_tickangle=-45  # Rotate x labels
    )
    st.plotly_chart(fig, use_container_width=True)

# --- Right Chart: Bar chart by token ---
with col2:
    # 1. Group data
    df_yield_grouped = (
        df_yield
        .groupby(["symbol", "project"], as_index=False)["tvlUsd"]
        .sum()
    )

    # 2. Rename protocol names (for display + legend)
    rename_map = {
        "aave-v3": "Aave",
        "compound-v3": "Compound",
        "morpho-v1": "Morpho",
        "sparklend": "SparkLend"
    }

    df_yield_grouped["project"] = df_yield_grouped["project"].replace(rename_map)

    # 3. Correct color mapping (MATCHES renamed values)
    color_map = {
        "Aave": "#9391f7",
        "Compound": "#38cfa0",
        "Morpho": "#3277fe",
        "SparkLend": "#e55314"
    }

    # 4. Bar chart
    fig_bar = px.bar(
        df_yield_grouped,
        x="symbol",
        y="tvlUsd",
        color="project",
        title="TVL Distribution by Token",
        color_discrete_map=color_map,
        labels={
            "symbol": "Token",
            "tvlUsd": "TVL (USD)",
            "project": "Protocol"
        }
    )

    # 5. Layout fixes
    fig_bar.update_layout(
        barmode="stack",
        yaxis_tickformat="$~s",
        xaxis_tickangle=-45,
        legend_title_text="Protocol",
        margin=dict(t=60, r=20, l=10, b=40)
    )

    st.plotly_chart(fig_bar, use_container_width=True)
