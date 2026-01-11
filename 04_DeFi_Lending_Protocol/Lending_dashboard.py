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


st.markdown("<div style='height: 20px;'></div>", unsafe_allow_html=True)




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




import pandas as pd
import streamlit as st
import plotly.express as px

# ===== Load Dataframes =====
df_tvl = df_all_final  # historical TVL data
df_yield = df_yield_final  # token-level TVL + APY

# ================= Page Config
st.set_page_config(layout="wide")

# ===== Header & Description =====
st.title("📊 DeFi Lending Market Dashboard")

st.markdown(
    """
    This dashboard shows lending market metrics across multiple protocols and blockchains.
    You can filter data by chain and time period, and explore TVL & yield statistics.
    """
)

# ===== Sidebar Filters =====
st.sidebar.header("🔍 Filters")

# Time Range
time_range = st.sidebar.selectbox(
    "Select Time Period:",
    ["Last 3 Months", "Last 6 Months", "Last 12 Months"],
    index=2
)

# Chain Filter
chain_options = ["All"] + sorted(df_tvl["chain"].unique())
selected_chain = st.sidebar.selectbox("Choose a chain:", chain_options)

# ===== Filter TVL Based on Sidebar =====
df_tvl_filtered = df_tvl.copy()

months_map = {"Last 3 Months": 3, "Last 6 Months": 6, "Last 12 Months": 12}
cutoff = df_tvl_filtered['date'].max() - pd.DateOffset(months=months_map[time_range])
df_tvl_filtered = df_tvl_filtered[df_tvl_filtered['date'] >= cutoff]

if selected_chain != "All":
    df_tvl_filtered = df_tvl_filtered[df_tvl_filtered['chain'] == selected_chain]

# ===== Section 1: Key Metrics =====
st.subheader("📊 Key Lending Metrics")

col1, col2, col3, col4 = st.columns(4)

# Latest TVL total across all
latest_data = df_tvl_filtered[df_tvl_filtered['date'] == df_tvl_filtered['date'].max()]
total_tvl = latest_data['totalLiquidityUSD'].sum()

col1.metric("🏦 Total TVL", f"${total_tvl/1e9:.2f} B")

# Protocol-specific TVL
protocol_tvls = latest_data.groupby("protocol")["totalLiquidityUSD"].sum().reset_index()

for idx, row in protocol_tvls.iterrows():
    value = row["totalLiquidityUSD"]
    col = col2 if idx == 0 else col3 if idx == 1 else col4
    col.metric(f"{row['protocol']} TVL", f"${value/1e9:.2f} B")

# ===== Section 2: TVL Trend Over Time =====
st.subheader("📈 TVL Trend Over Time")

if not df_tvl_filtered.empty:
    fig_trend = px.line(
        df_tvl_filtered,
        x="date",
        y="totalLiquidityUSD",
        color="protocol",
        labels={"date": "Date", "totalLiquidityUSD": "TVL (USD)"},
        hover_data={"totalLiquidityUSD": ":,.0f"},
        title="TVL Over Time by Protocol"
    )
    fig_trend.update_layout(yaxis_tickformat="$~s", legend_title="Protocol")
    st.plotly_chart(fig_trend, use_container_width=True)
else:
    st.warning("No TVL data to show.")

# ===== Section 3: TVL Distribution by Token =====
st.subheader("📦 TVL Distribution by Token")

df_tokens_grouped = df_yield.groupby(["symbol", "project"], as_index=False)["tvlUsd"].sum()

# Rename protocols for better display
protocol_map = {
    "aave-v3": "Aave",
    "compound-v3": "Compound",
    "morpho-v1": "Morpho",
    "sparklend": "SparkLend"
}
df_tokens_grouped["project"] = df_tokens_grouped["project"].replace(protocol_map)

color_map = {
    "Aave": "#9391f7",
    "Compound": "#38cfa0",
    "Morpho": "#3277fe",
    "SparkLend": "#e55314"
}

fig_tokens = px.bar(
    df_tokens_grouped,
    x="symbol",
    y="tvlUsd",
    color="project",
    color_discrete_map=color_map,
    labels={"symbol": "Token", "tvlUsd": "TVL (USD)", "project": "Protocol"},
    title="TVL Distribution by Token"
)
fig_tokens.update_layout(
    yaxis_tickformat="$~s",
    xaxis_tickangle=-45,
    barmode="stack",
    title_x=0.5
)
st.plotly_chart(fig_tokens, use_container_width=True)

# ===== Section 4: Yield Table =====
st.subheader("📋 Yield Stats (APY) by Token")

df_yield_display = df_yield.copy()
df_yield_display["project"] = df_yield_display["project"].replace(protocol_map)

st.dataframe(
    df_yield_display[
        ["project", "chain", "symbol", "tvlUsd", "apy", "apyMean30d"]
    ].sort_values(by="tvlUsd", ascending=False)
)
