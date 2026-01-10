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

if not filtered_df.empty:
    st.subheader("📈 TVL Over Time")
    chart_data = filtered_df.sort_values("date")

    # Handle single or all chains
    chains_to_plot = chart_data['chain'].unique() if selected_chain == "All" else [selected_chain]

    fig, ax = plt.subplots(figsize=(12, 6))
    for chain in chains_to_plot:
        chain_data = chart_data[chart_data['chain'] == chain]
        ax.plot(chain_data['date'], chain_data['totalLiquidityUSD'], label=chain)

    ax.set_xlabel("Date")
    ax.set_ylabel("TVL (USD)")
    ax.set_title("Total Liquidity Over Time")
    ax.legend()
    ax.grid(True)

    st.pyplot(fig)

else:
    st.warning("No data available for the selected filters.")
