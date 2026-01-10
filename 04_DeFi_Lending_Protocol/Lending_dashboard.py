import pandas as pd
import streamlit as st
import matplotlib.pyplot as plt

# -----------------------------
# Load DataFrame from file
# -----------------------------
df = pd.read_csv("https://raw.githubusercontent.com/bellatrix-ds/blockchain-dashboards-and-visualizations/refs/heads/main/04_DeFi_Lending_Protocol/final_data.csv")


# Filter data for date > 2025
df = df[df['date'] > '2025-12-31']

# -----------------------------
# Streamlit UI
# -----------------------------
st.set_page_config(page_title="AAVE TVL Dashboard", layout="wide")
st.title("📊 AAVE Lending Protocol - TVL Dashboard")
st.markdown("Visualize Total Value Locked (TVL) across chains after **2025**")

# Sidebar filters
with st.sidebar:
    st.header("🔍 Filters")

    chains = df['chain'].unique()
    selected_chains = st.multiselect("Select Chain(s):", chains, default=chains[:1])

    df['month'] = df['date'].dt.to_period('M').astype(str)
    months = df['month'].unique()
    selected_months = st.multiselect("Select Month(s):", months, default=months[-3:])

# Apply filters
filtered_df = df[
    (df['chain'].isin(selected_chains)) &
    (df['month'].isin(selected_months))
]

# -----------------------------
# Line chart
# -----------------------------
if not filtered_df.empty:
    st.subheader("📈 TVL Over Time")
    chart_data = filtered_df.sort_values("date")

    fig, ax = plt.subplots(figsize=(12, 6))
    for chain in selected_chains:
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
