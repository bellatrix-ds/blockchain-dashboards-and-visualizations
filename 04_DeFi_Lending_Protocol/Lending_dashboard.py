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
st.set_page_config(page_title="Defi Lending Protocol Dashboard", layout="wide")
st.title("📊 Defi Lending Protocol Dashboard")

# --------- Box
st.markdown("### 👤 about dashboard")
with st.expander("lending dashboard"):
    st.write("""
Visualize Total Value Locked (TVL) across chains after **2025**
    """)

# --------
st.markdown("")

# Sidebar filters
with st.sidebar:
    st.header("🔍 Filters")

    chains = df['chain'].unique()
    selected_chains = st.multiselect("Select Chain(s):", chains, default=chains[:1])

    df['date'] = pd.to_datetime(df['date'])
    max_date = df['date'].max()
    last_3_months = max_date - pd.DateOffset(months=3)
    last_6_months = max_date - pd.DateOffset(months=6)
    last_12_months = max_date - pd.DateOffset(months=12)

date_filter = st.selectbox("⏳ TimeFrame ", ["Last 3 Months", "Last 6 Months", "Last 12 Months"])

if date_filter == "Last 3 Months":
    df = df[df['date'] >= last_3_months]
elif date_filter == "Last 6 Months":
    df = df[df['date'] >= last_6_months]
elif date_filter == "Last 12 Months":
    df = df[df['date'] >= last_12_months]

    
# Apply filters
filtered_df = df[
    (df['chain'].isin(selected_chains)) &
    (df['month'].isin(selected_months))
]

# -----------------------------
# Line chart
# -----------------------------

if not filtered_df.empty:
    st.markdown("### 📉 TVL Over Time")

    fig, ax = plt.subplots(figsize=(12, 6))

    for chain in selected_chains:
        chain_data = filtered_df[filtered_df['chain'] == chain].sort_values("date")
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
