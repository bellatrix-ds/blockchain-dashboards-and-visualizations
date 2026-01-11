import pandas as pd
import streamlit as st
import plotly.express as px

# -----------------------------
# Load TVL Data
# -----------------------------
df = pd.read_csv("https://raw.githubusercontent.com/bellatrix-ds/blockchain-dashboards-and-visualizations/refs/heads/main/04_DeFi_Lending_Protocol/final_data.csv")
df['date'] = pd.to_datetime(df['date'])
df = df[df['date'] >= '2025-01-01']
df = df[df['date'] <= '2026-01-01']


# -----------------------------
# Load Yield Data
# -----------------------------
df_yield = pd.read_csv("https://raw.githubusercontent.com/bellatrix-ds/blockchain-dashboards-and-visualizations/refs/heads/main/04_DeFi_Lending_Protocol/df_yeild_final.csv")

# -----------------------------
# Page Config
# -----------------------------
st.set_page_config(layout="wide")
st.title("🏦 DeFi Lending Protocol Dashboard")
st.subheader("Liquidity, TVL, and Yield Across Top 5 Lending Protocols 🧮")


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
# About Me
# -----------------------------


with st.sidebar:
    st.markdown("---")
    st.image("04_DeFi_Lending_Protocol/JGqdjaIW_400x400.jpg", width=100)  
    st.markdown("**My name is Bella**")
    st.caption("Blockchain Research Analyst")
    st.caption("**Get in touch: 👇🏼**")

    c1, c2 = st.columns(2)
    with c1:
        st.link_button("Portfolio", "https://bellabahrami.carrd.co/")
    with c2:
        st.link_button("GitHub", "https://github.com/bellatrix-ds")

    st.link_button("x.com", "https://x.com/Bella52496")
    st.markdown("---")


# -----------------------------
# KPI Section
# -----------------------------
st.markdown(" ")


st.markdown("""
<h4 style="
    text-align: center;
    color: white;
    margin-top: 10px;
    margin-bottom: 1px;
" 📊 Total TVL""", unsafe_allow_html=True)

st.markdown("""
<style>
hr { display: none; }
</style>
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
  margin-top: 1px;
}
.kpi-card {
  background: rgba(0,0,0,0.35);
  border: 1px solid rgba(255,255,255,0.10);
  border-radius: 14px;
  padding: 18px 16px;
  box-shadow: 0 10px 30px rgba(0,0,0,0.35);
}
.kpi-title {
  font-size: 40px;
  color: rgba(255,255,255,0.75);
  margin: 0 0 10px 0;
}
.kpi-value {
  font-size: 70px;
  font-weight: 600;
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
<h4 style="text-align: center; color: white; margin-top: 60px;">💰⛓️‍💥 Protocol TVL By Chain</h4>
<hr style="border-top: 1px solid gray; margin-top: 4px;">
""", unsafe_allow_html=True)



col1, col2 = st.columns(2)

# --- Left Chart: TVL Trend Over Time ---


df_plot = df_filtered.copy()
df_plot["chain"] = df_plot["chain"].astype(str).str.strip()

# if you only want TVL:
df_plot = df_plot[df_plot["metric_type"] == "tvl"]

df_plot = (
    df_plot.groupby(["date", "chain"], as_index=False)["totalLiquidityUSD"]
    .sum()
    .sort_values(["chain", "date"])
)


with col1:
    fig = px.line(
    df_plot,
    x="date",
    y="totalLiquidityUSD",
    color="chain",
    title="TVL Distribution by Chain Over Time",
    labels={"date": "Date", "totalLiquidityUSD": "TVL (USD)", "chain": "Chain"},
)
    fig.update_yaxes(
    type="log",
        tickvals=[2e7, 5e7, 1e8, 2e8, 5e8, 1e9, 2e9, 5e9, 1e10, 2e10 ,6e10],
        ticktext=["$20M", "$50M", "$100M", "$200M" , "$500M",
              "$1B", "$2B", "$5B", "$10B", "$20B", "$60B"]
)
    fig.update_layout(
    hovermode="x unified",
    showlegend=False,
    margin=dict(t=50, r=20, l=10, b=40),
    xaxis_tickangle=-45
)
    st.plotly_chart(fig, use_container_width=True)        





# --- Right Chart: TVL by Chain (stacked by protocol) ---

with col2:
    bar_df = df_filtered.copy()
    bar_df["chain"] = bar_df["chain"].astype(str).str.strip()
    bar_df["protocol"] = bar_df["protocol"].astype(str).str.strip()

    # keep TVL only + respect filters (df_filtered already filtered)
    bar_df = bar_df[bar_df["metric_type"] == "tvl"]

    # total TVL per chain for each protocol over the selected time range
    bar_df = (
        bar_df.groupby(["chain", "protocol"], as_index=False)["totalLiquidityUSD"]
        .sum()
        .sort_values(["totalLiquidityUSD"], ascending=False)
    )

    fig_bar = px.bar(
        bar_df,
        x="chain",
        y="totalLiquidityUSD",
        color="protocol",
        barmode="stack",
        title="Total TVL by Chain (Stacked by Protocol)",
        labels={"chain": "Chain", "totalLiquidityUSD": "Total TVL (USD)", "protocol": "Protocol"},
        hover_data={"totalLiquidityUSD": ":.3s"}
    )

    fig_bar.update_layout(
        yaxis_tickformat="$~s",
        hovermode="x unified",
        margin=dict(t=50, r=20, l=10, b=40)
    )

    st.plotly_chart(fig_bar, use_container_width=True)
  

# --------------
st.markdown("""
<h4 style="text-align: center; color: white; margin-top: 30px;">💰💎 Protocol TVL By Token</h4>
<hr style="border-top: 1px solid gray; margin-top: 4px;">
""", unsafe_allow_html=True)


col1, col2 = st.columns(2)

with col1:
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


with col2:
    df_token_pie = (
        df_yield_grouped.groupby("symbol", as_index=False)["tvlUsd"]
        .sum()
        .sort_values("tvlUsd", ascending=False)
    )

    fig_pie = px.pie(
        df_token_pie,
        names="symbol",
        values="tvlUsd",
        title="Total TVL Locked by Token",
        hole=0.45
    )

    fig_pie.update_traces(
        textposition="inside",
        textinfo="percent+label",
        hovertemplate="<b>%{label}</b><br>TVL: %{value:$,.2s}<br>Share: %{percent}<extra></extra>"
    )

    fig_pie.update_layout(
        height=380,
        margin=dict(t=40, r=20, l=10, b=20),
        title_x=0.5,
        showlegend=False
    )

    st.plotly_chart(fig_pie, use_container_width=True)


# -----------------------------
# Section: Yield Table
# -----------------------------
st.markdown("""
<h4 style="text-align: center; color: white; margin-top: 30px;">🔦 APY Table with 🟢 Positive/🔴 Negative Coloring</h4>
<hr style="border: none; height: 0; margin: 0; padding: 0;">
""", unsafe_allow_html=True)


# Prepare APY table
df_apy = df_yield.copy()
df_apy["project"] = df_apy["project"].replace(rename_map)

# Sort by tvlUsd
df_apy = df_apy.sort_values(by="tvlUsd", ascending=False)

# Rename columns (display names)
df_apy = df_apy.rename(columns={
    "project": "Protocol",
    "tvlUsd": "Total TVL ($)",
    "apy": "APY BASE",
    "apyMean30d": "APY 30 Days Avg"
})

# Style color based on positive/negative
def color_apy(val):
    if val > 0:
        return "background-color: #2ecc71; color: white;"
    elif val <= 0:
        return "background-color: #e74c3c; color: white;"
    return ""

df_apy_view = df_apy[["Protocol", "chain", "symbol", "Total TVL ($)", "APY BASE", "APY 30 Days Avg"]]

df_apy_styled = (
    df_apy_view.style
    .applymap(color_apy, subset=["APY BASE", "APY 30 Days Avg"])
    .format({
        "Total TVL ($)": "${:,.0f}",
        "APY BASE": "{:.2%}",
        "APY 30D AVG": "{:.2%}",
    })
    .hide(axis="index")  # remove index column
)

st.dataframe(df_apy_styled, use_container_width=True)


# ---- Footage ----



