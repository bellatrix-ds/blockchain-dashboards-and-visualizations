import pandas as pd
import streamlit as st
import plotly.express as px

# -----------------------------
# Load TVL Data
# -----------------------------
df = pd.read_csv("https://raw.githubusercontent.com/bellatrix-ds/blockchain-dashboards-and-visualizations/refs/heads/main/04_DeFi_Lending_Protocol/final_data.csv")
df['date'] = pd.to_datetime(df['date'])
df = df[df['date'] >= '2025-01-01']

# -----------------------------
# Load Yield Data
# -----------------------------
df_yield = pd.read_csv("https://raw.githubusercontent.com/bellatrix-ds/blockchain-dashboards-and-visualizations/refs/heads/main/04_DeFi_Lending_Protocol/df_yeild_final.csv")

# -----------------------------
# Page Config
# -----------------------------
st.set_page_config(layout="wide")
st.title("📊 DeFi Lending Protocol Dashboard")

# -----------------------------
# Dashboard Header
# -----------------------------
st.markdown("""
<div style="
    background-color: #111111;
    padding: 20px 25px;
    border-radius: 10px;
    border: 1px solid #333;
    color: white;
">
    <h4 style='margin-bottom: 5px;'>📋 Overview</h4>
    <p style='color: #b0b0b0; margin-top: 0;'>This dashboard visualizes the metrics of lending protocol across multiple blockchains starting from 2025.
You can filter by chain and select a time period (last 3, 6, or 12 months).</p>
</div>
""", unsafe_allow_html=True)

# -----------------------------
# Sidebar Filters
# -----------------------------
st.sidebar.header("🔍 Filters")
time_range = st.sidebar.selectbox("Select Time Period:", ["Last 3 Months", "Last 6 Months", "Last 12 Months"], index=2)
chain_options = ["All"] + sorted(df["chain"].unique())
selected_chain = st.sidebar.selectbox("Choose a chain:", chain_options)

# -----------------------------
# Filter Main TVL Data
# -----------------------------
df_filtered = df.copy()
months_map = {"Last 3 Months": 3, "Last 6 Months": 6, "Last 12 Months": 12}
cutoff = df_filtered['date'].max() - pd.DateOffset(months=months_map[time_range])
df_filtered = df_filtered[df_filtered['date'] >= cutoff]
if selected_chain != "All":
    df_filtered = df_filtered[df_filtered["chain"] == selected_chain]

# -----------------------------
# KPI Section
# -----------------------------




st.markdown("""
<h4 style="text-align: center; color: white; margin-top: 30px;">📊 Lending TVL KPIs</h4>
<hr style="border: none; height: 0; margin: 0; padding: 0;">
""", unsafe_allow_html=True)


# ---- KPI values ----
kpi_df = df_filtered[df_filtered['metric_type'] == 'tvl'].copy()
kpi_df['protocol'] = kpi_df['protocol'].astype(str).str.strip()
tvl_sum = kpi_df.groupby('protocol')['totalLiquidityUSD'].sum()

protocols = ["Aave", "Compound", "Morpho", "SparkLend"]

# ---- CSS (once) ----
st.markdown("""
<style>
.kpi-grid {
  display: grid;
  grid-template-columns: repeat(4, 1fr);
  gap: 18px;
  margin-top: 10px;
}
.kpi-card {
  background: rgba(0,0,0,0.35);
  border: 1px solid rgba(255,255,255,0.10);
  border-radius: 14px;
  padding: 18px 16px;
  box-shadow: 0 10px 30px rgba(0,0,0,0.35);
}
.kpi-title {
  font-size: 14px;
  color: rgba(255,255,255,0.75);
  margin: 0 0 10px 0;
}
.kpi-value {
  font-size: 34px;
  font-weight: 800;
  color: white;
  margin: 0;
  line-height: 1.0;
}
</style>
""", unsafe_allow_html=True)

# ---- HTML cards ----
cards = '<div class="kpi-grid">'
for protocol in protocols:
    value = float(tvl_sum.get(protocol, 0.0))
    cards += (
        '<div class="kpi-card">'
        f'<p class="kpi-title">{protocol} TVL</p>'
        f'<p class="kpi-value">${value/1e12:.2f} T</p>'
        '</div>'
    )
cards += "</div>"

# IMPORTANT: فقط همین، نه st.code / نه st.write
st.markdown(cards, unsafe_allow_html=True)


# -----------------------------
# Section: Protocol TVL Overview
# -----------------------------
st.markdown("<div style='height: 20px;'></div>", unsafe_allow_html=True)


st.markdown("""
<h4 style="text-align: center; color: white; margin-top: 20px;">💰 Protocol TVL Overview</h4>
<hr style="border-top: 1px solid gray; margin-top: 4px;">
""", unsafe_allow_html=True)



col1, col2 = st.columns(2)

# --- Left Chart: TVL Trend Over Time ---
with col1:
    fig = px.line(
        df_filtered,
        x="date",
        y="totalLiquidityUSD",
        color="chain",
        title="TVL Distribution by Chain Over Time",
        labels={"date": "Date", "totalLiquidityUSD": "TVL (USD)", "chain": "Chain"},
        hover_data={"totalLiquidityUSD": ":.3s", "chain": True, "date": False}
    )
    fig.update_layout(
        yaxis_tickformat="$~s",
        hovermode="x unified",
        showlegend=False,
        margin=dict(t=50, r=20, l=10, b=40),
        xaxis_tickangle=-45
    )
    st.plotly_chart(fig, use_container_width=True)

# --- Right Chart: TVL by Token ---
with col2:
    df_yield_grouped = df_yield.groupby(["symbol", "project"], as_index=False)["tvlUsd"].sum()
    rename_map = {
        "aave-v3": "Aave",
        "compound-v3": "Compound",
        "morpho-v1": "Morpho",
        "sparklend": "SparkLend"
    }
    df_yield_grouped["project"] = df_yield_grouped["project"].replace(rename_map)

    color_map = {
        "Aave": "#9391f7",
        "Compound": "#38cfa0",
        "Morpho": "#3277fe",
        "SparkLend": "#e55314"
    }

    fig_bar = px.bar(
        df_yield_grouped,
        x="symbol",
        y="tvlUsd",
        color="project",
        title="TVL Distribution by Token",
        color_discrete_map=color_map,
        labels={"symbol": "Token", "tvlUsd": "TVL (USD)", "project": "Protocol"}
    )
    fig_bar.update_layout(
        barmode="stack",
        yaxis_tickformat="$~s",
        xaxis_tickangle=-45,
        legend_title_text="Protocol",
        margin=dict(t=60, r=20, l=10, b=40),
        title_x=0.5
    )
    st.plotly_chart(fig_bar, use_container_width=True)

# -----------------------------
# Section: Yield Table
# -----------------------------
st.markdown("<hr style='margin: 40px 0;'>", unsafe_allow_html=True)
st.subheader("📋 Yield Table")

df_yield_display = df_yield.copy()
df_yield_display["project"] = df_yield_display["project"].replace(rename_map)
st.dataframe(df_yield_display[["project", "chain", "symbol", "tvlUsd", "apy", "apyMean30d"]].sort_values(by="tvlUsd", ascending=False))



# ---- Protocol Share Pie Chart ----
st.subheader("📊 Protocol Share of TVL (Latest)")

# Latest date TVL (according to filtered timeframe)
latest_date = df_filtered['date'].max()
df_latest = df_filtered[df_filtered['date'] == latest_date]

protocol_share = (
    df_latest.groupby("protocol")["totalLiquidityUSD"]
    .sum()
    .reset_index()
    .rename(columns={"totalLiquidityUSD":"TVL"})
)

fig_pie = px.pie(
    protocol_share,
    names="protocol",
    values="TVL",
    title="Percentage of TVL by Protocol",
    color="protocol",
    color_discrete_map={
        "Aave": "#9391f7",
        "Compound": "#38cfa0",
        "Morpho": "#3277fe",
        "SparkLend": "#e55314"
    }
)

fig_pie.update_traces(textposition="inside", textinfo="percent+label")
st.plotly_chart(fig_pie, use_container_width=True, key="protocol_share_pie")



st.subheader("📋 APY Table with Positive/Negative Coloring")

# Prepare APY table
df_apy = df_yield.copy()
df_apy["project"] = df_apy["project"].replace(rename_map)

# Sort by tvlUsd
df_apy = df_apy.sort_values(by="tvlUsd", ascending=False)

# Style color based on positive/negative
def color_apy(val):
    if val > 0:
        return 'background-color: #2ecc71; color: white;'  # green
    elif val < 0:
        return 'background-color: #e74c3c; color: white;'  # red
    return ''

df_apy_styled = df_apy[["project","chain","symbol","tvlUsd","apy","apyMean30d"]].style.applymap(color_apy, subset=["apy","apyMean30d"])

st.dataframe(df_apy_styled, use_container_width=True)
