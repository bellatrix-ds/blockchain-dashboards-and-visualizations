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

# Filter df based on selected_chain and selected_timeframe
df_filtered = df.copy()

# Filter by time
if selected_timeframe == "Last 3 Months":
    cutoff = df_filtered['date'].max() - pd.DateOffset(months=3)
elif selected_timeframe == "Last 6 Months":
    cutoff = df_filtered['date'].max() - pd.DateOffset(months=6)
else:  # Last 12 Months
    cutoff = df_filtered['date'].max() - pd.DateOffset(months=12)

df_filtered = df_filtered[df_filtered['date'] >= cutoff]

# Filter by chain
if selected_chain != "All":
    df_filtered = df_filtered[df_filtered['chain'] == selected_chain]
