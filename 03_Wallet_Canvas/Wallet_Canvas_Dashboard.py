#!/usr/bin/env python
# coding: utf-8

import streamlit as st
import pandas as pd
from datetime import datetime

df = pd.read_csv('https://raw.githubusercontent.com/bellatrix-ds/blockchain-dashboards-and-visualizations/refs/heads/main/03_Wallet_Canvas/01%2602_df.csv',on_bad_lines='skip')

st.title("📊 ETH Wallet Insights & Patterns")

# Wallet selector
wallet = st.selectbox("🔎 Select a Wallet Address", df['wallet_address'])
wallet_data = df[df['wallet_address'] == wallet].iloc[0]


# 🧾 Basic Wallet Information
st.header("📘 Basic Wallet Information")
st.write(f"**🔐 Wallet Address:** `{wallet_data['wallet_address']}`")
st.write("💰 **ETH Balance:**", f"{wallet_data['eth']} ETH")
st.write("📦 **Total Transactions (All Time):**", wallet_data['tx_count'])
st.write("📆 **Transactions in Last 3 Months:**", wallet_data['total_tx'])
st.write(f"🕒 **First Transaction:** {wallet_data['first_tx']}")
st.write(f"🕓 **Last Transaction:** {wallet_data['last_tx']}")

# 🔁 Transaction Behavior
st.header("📊 Transaction Behavior")
st.write("📈 **Avg TX Value (ETH):**", f"{wallet_data['avg_tx_value']:.6f}")
st.write("💵 **Avg TX Value (USD):**", f"${wallet_data['avg_value_usd']:.2f}")
st.write("🗓️ **Avg TX per Day:**", f"{wallet_data['tx_per_day']:.2f}")
st.write("📅 **Avg TX per Month:**", f"{wallet_data['tx_per_month']:.2f}")
st.write("⏳ **Avg Time Gap (days):**", f"{wallet_data['avg_time_gap_days']}")

# New Metric: TX activity rate
tx_activity_rate = round(wallet_data['total_tx'] / wallet_data['tx_count'] * 100, 2)
st.write("📊 **Recent Activity Rate (Last 3mo vs All):**", f"{tx_activity_rate}%")

# ______________________________________________________
# Part 3
import altair as alt

filtered_df3 = pd.read_csv('https://raw.githubusercontent.com/bellatrix-ds/blockchain-dashboards-and-visualizations/refs/heads/main/03_Wallet_Canvas/03_df.csv')
st.header("📈 Wallet Activity Overview")

# filtered_df3['month'] = pd.to_datetime(filtered_df3['month'])
df_wallet = filtered_df3[filtered_df3['wallet_address'] == wallet]

# Monthly Transaction Count
st.subheader("🔁 Monthly Transaction Count")
tx_chart = alt.Chart(df_wallet).mark_line(point=True).encode(
    x=alt.X('month:T', title='Month'),
    y=alt.Y('tx_count:Q', title='Transactions'),
    tooltip=['month:T', 'tx_count']
).properties(height=300)
st.altair_chart(tx_chart, use_container_width=True)

# ETH Balance Over Time
st.subheader("💰 ETH Balance Over Time")
balance_chart = alt.Chart(df_wallet).mark_line(point=True).encode(
    x=alt.X('month:T', title='Month'),
    y=alt.Y('eth_balance:Q', title='ETH Balance'),
    tooltip=['month:T', 'eth_balance']
).properties(height=300)
st.altair_chart(balance_chart, use_container_width=True)


# 📜 Top Contract Interactions

df_contracts = pd.read_csv('https://raw.githubusercontent.com/bellatrix-ds/blockchain-dashboards-and-visualizations/refs/heads/main/03_Wallet_Canvas/04_df_01.csv',on_bad_lines='skip')

st.header("🧑‍💻 Most Frequent Tx Targets (Mixed)")

wallet_contracts = df_contracts[df_contracts['wallet'] == wallet.lower()]
# Get top 10 by tx_count
top_contracts = (
    wallet_contracts
    .sort_values(by='tx_count', ascending=False)
    .head(10)
    [['counterparty', 'tx_count']]
)

# Display two-column table
st.dataframe(top_contracts, use_container_width=True)


# Part 4_2

df_contracts = pd.read_csv(
    'https://raw.githubusercontent.com/bellatrix-ds/blockchain-dashboards-and-visualizations/refs/heads/main/03_Wallet_Canvas/04_df_02.csv',
    on_bad_lines='skip'
)

st.header("📄 Top Interacted Contracts")

# Filter contracts for the selected wallet
wallet_contracts = df_contracts[df_contracts['wallet'] == wallet.lower()]

# Get top 10 contracts based on rank
top_contracts = (
    wallet_contracts
    .sort_values(by='rnk')
    .head(10)
    [['contract', 'tx_count']]
)

# Show as a table
st.dataframe(top_contracts, use_container_width=True)


# ـــ
st.markdown("---")
st.caption("📧 Contact me: bellabahramii@gmail.com")


