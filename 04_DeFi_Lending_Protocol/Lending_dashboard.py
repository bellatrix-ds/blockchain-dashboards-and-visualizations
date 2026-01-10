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

# --- SIDEBAR FILTERS ---
st.sidebar.header("🔍 Filters")

# Time Range Filter
st.sidebar.subheader("⏳ Time Range")
time_range = st.sidebar.selectbox(
    "Select Time Period:",
    options=["Last 3 Months", "Last 6 Months", "Last 12 Months"],
    index=2  # default: Last 12 Months
)

# Chain Filter
st.sidebar.subheader("🔗 Chain")
chain_options = ["All"] + sorted(df["chain"].unique())
selected_chain = st.sidebar.selectbox("Choose a chain:", chain_options)




# =============================
# 📈 Line Chart
# =============================

import matplotlib.ticker as mtick
import matplotlib.dates as mdates

if not df_filtered.empty:
    fig, ax = plt.subplots(figsize=(12, 6))

    # Plot each chain separately
    for chain in df_filtered['chain'].unique():
        chain_data = df_filtered[df_filtered['chain'] == chain]
        ax.plot(chain_data['date'], chain_data['totalLiquidityUSD'], label=chain)

    # Format x-axis as month names
    ax.xaxis.set_major_formatter(mdates.DateFormatter('%b'))
    ax.xaxis.set_major_locator(mdates.MonthLocator())

    # Format y-axis to show billions with $ sign
    ax.yaxis.set_major_formatter(mtick.FuncFormatter(lambda x, _: f'${x/1e9:.0f}B'))

    ax.set_xlabel("Date")
    ax.set_ylabel("TVL (USD)")
    ax.set_title("Total Liquidity Over Time")

    # Move legend to the right, smaller font
    ax.legend(loc='center left', bbox_to_anchor=(1.02, 0.5), fontsize='small')

    st.pyplot(fig)
else:
    st.warning("No data available for the selected filters.")

