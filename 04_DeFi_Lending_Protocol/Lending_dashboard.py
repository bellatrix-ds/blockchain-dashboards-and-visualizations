import pandas as pd
import streamlit as st
import matplotlib.pyplot as plt

# -----------------------------
# Load DataFrame from file
# -----------------------------
df = pd.read_csv("https://raw.githubusercontent.com/bellatrix-ds/blockchain-dashboards-and-visualizations/refs/heads/main/04_DeFi_Lending_Protocol/final_data.csv")


# Filter data for date > 2025
df = df[df['date'] > '2025-12-31']

df['date'] = pd.to_datetime(df['date'])

st.title("📊 DeFi Lending Protocol Dashboard")
st.markdown("Visualize Total Value Locked (TVL) across chains after **2025**")

# ✅ Always-visible About Box (not collapsible)
st.markdown("### 🧑‍💻 About This Dashboard")
st.markdown("""
This dashboard visualizes the Total Value Locked (TVL) of AAVE lending protocol 
across multiple blockchains starting from 2025.  
You can filter by chain and select a time period (last 3, 6, or 12 months).
""")

# =============================
# 🔍 Sidebar Filters
# =============================
st.sidebar.header("🔍 Filters")

# Chain Filter
selected_chains = st.sidebar.multiselect(
    "Select Chain(s):",
    df['chain'].unique(),
    default=df['chain'].unique()
)

# Time Range Filter
st.sidebar.subheader("⏳ Time Range")
time_range_option = st.sidebar.selectbox(
    "Select Time Period:",
    ["Last 3 Months", "Last 6 Months", "Last 12 Months"]
)

# Apply Time Range Filter
latest_date = df['date'].max()
if time_range_option == "Last 3 Months":
    start_date = latest_date - pd.DateOffset(months=3)
elif time_range_option == "Last 6 Months":
    start_date = latest_date - pd.DateOffset(months=6)
else:
    start_date = latest_date - pd.DateOffset(months=12)

df = df[(df['date'] >= start_date) & (df['chain'].isin(selected_chains))]

# =============================
# 📈 Line Chart
# =============================
if not df.empty:
    st.subheader("📈 TVL Over Time")

    fig, ax = plt.subplots(figsize=(12, 6))
    for chain in selected_chains:
        chain_data = df[df['chain'] == chain].sort_values("date")
        ax.plot(chain_data['date'], chain_data['totalLiquidityUSD'], label=chain)
        ax.fill_between(chain_data['date'], chain_data['totalLiquidityUSD'], alpha=0.4)

    ax.set_xlabel("Date")
    ax.set_ylabel("TVL (USD)")
    ax.set_title("Total Liquidity Over Time")
    ax.legend()
    ax.grid(alpha=0.3)
    st.pyplot(fig)
else:
    st.warning("No data available for the selected filters.")
