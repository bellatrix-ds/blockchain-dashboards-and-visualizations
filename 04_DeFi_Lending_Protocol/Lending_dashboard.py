import pandas as pd
import streamlit as st
import matplotlib.pyplot as plt

# -----------------------------
# Load DataFrame from file
# -----------------------------
df = pd.read_csv("https://raw.githubusercontent.com/bellatrix-ds/blockchain-dashboards-and-visualizations/refs/heads/main/04_DeFi_Lending_Protocol/final_data.csv")


# -----------------------------
# 🔍 Sidebar Filters
# -----------------------------
st.sidebar.header("🔍 Filters")

# Time Range
st.sidebar.subheader("⏳ Time Range")
time_range = st.sidebar.selectbox(
    "Select Time Period:",
    options=["Last 3 Months", "Last 6 Months", "Last 12 Months"],
    index=2  # default
)

# Chain Selector
st.sidebar.subheader("🔗 Chain")
chain_options = ["All"] + sorted(df["chain"].unique())
selected_chain = st.sidebar.selectbox("Choose a chain:", chain_options)

# -----------------------------
# 📉 Filter Data
# -----------------------------
df_filtered = df.copy()

# Time filtering
if time_range == "Last 3 Months":
    cutoff = df_filtered['date'].max() - pd.DateOffset(months=3)
elif time_range == "Last 6 Months":
    cutoff = df_filtered['date'].max() - pd.DateOffset(months=6)
else:
    cutoff = df_filtered['date'].max() - pd.DateOffset(months=12)

df_filtered = df_filtered[df_filtered['date'] >= cutoff]

# Chain filtering
if selected_chain != "All":
    df_filtered = df_filtered[df_filtered['chain'] == selected_chain]

# -----------------------------
# 📈 Plot Chart
# -----------------------------
st.subheader("📈 TVL Over Time")

if not df_filtered.empty:
    fig, ax = plt.subplots(figsize=(12, 6))

    # Plot lines
    for chain in df_filtered['chain'].unique():
        chain_data = df_filtered[df_filtered['chain'] == chain]
        ax.plot(chain_data['date'], chain_data['totalLiquidityUSD'], label=chain)

    # Format x-axis
    ax.xaxis.set_major_formatter(mdates.DateFormatter('%b'))
    ax.xaxis.set_major_locator(mdates.MonthLocator())

    # Format y-axis
    ax.yaxis.set_major_formatter(mtick.FuncFormatter(lambda x, _: f'${x/1e9:.0f}B'))

    ax.set_xlabel("Date")
    ax.set_ylabel("TVL (USD)")
    ax.set_title("Total Liquidity Over Time")

    # Format legend
    ax.legend(loc='center left', bbox_to_anchor=(1.02, 0.5), fontsize='small')
    plt.tight_layout()

    st.pyplot(fig)
else:
    st.warning("No data available for the selected filters.")
