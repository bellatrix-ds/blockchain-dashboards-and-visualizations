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
st.subheader("📈 TVL Over Time")

if df_filtered.empty:
    st.warning("No data available for the selected filters.")
else:
    fig, ax = plt.subplots(figsize=(12, 6))

    for chain in df_filtered['chain'].unique():
        chain_data = df_filtered[df_filtered['chain'] == chain]
        ax.plot(
            chain_data['date'],
            chain_data['totalLiquidityUSD'],
            label=chain,
            linewidth=2
        )

    # X axis → month names
    ax.xaxis.set_major_locator(mdates.MonthLocator())
    ax.xaxis.set_major_formatter(mdates.DateFormatter('%b'))

    # Y axis → $ billions
    ax.yaxis.set_major_formatter(
        mtick.FuncFormatter(lambda x, _: f'${x/1e9:.0f}B')
    )

    ax.set_xlabel("")
    ax.set_ylabel("TVL (USD)")
    ax.set_title("Total Value Locked Over Time")

    # Legend outside chart
    ax.legend(
        loc='center left',
        bbox_to_anchor=(1.02, 0.5),
        fontsize='small',
        frameon=False
    )

    ax.grid(False)
    plt.tight_layout()
    st.pyplot(fig)
