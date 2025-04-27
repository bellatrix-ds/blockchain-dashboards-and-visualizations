#!/usr/bin/env python
# coding: utf-8

# In[ ]:


import pandas as pd
import plotly.express as px
import streamlit as st

# Load data from GitHub
@st.cache_data
def load_data():
    url = 'https://raw.githubusercontent.com/bellatrix-ds/blockchain-dashboards-and-visualizations/refs/heads/main/02_NFT/part2_collection_analysis.csv.csv'
    df = pd.read_csv(url)
    return df

df = load_data()

# Sidebar for date filter
st.sidebar.title('Select Date Range')
date_filter = st.sidebar.radio(
    "Date Range:",
    ('7 days', '30 days', '90 days')
)

# Filter data based on selected date
today = pd.to_datetime('now')
if date_filter == '7 days':
    start_date = today - pd.Timedelta(days=7)
elif date_filter == '30 days':
    start_date = today - pd.Timedelta(days=30)
elif date_filter == '90 days':
    start_date = today - pd.Timedelta(days=90)

df_filtered = df[df['BLOCK_TIMESTAMP'] >= start_date]

# Group by Category
df_usd = df_filtered.groupby('CATEGORY').agg({'USD': 'sum'}).reset_index()
df_eth = df_filtered.groupby('CATEGORY').agg({'ETH': 'sum'}).reset_index()

# Title
st.title("Category Market Cap")

# First chart - Volume in USD
st.subheader("Volume by Category (USD)")
fig_usd = px.bar(
    df_usd.sort_values('USD', ascending=False),
    x='CATEGORY',
    y='USD',
    labels={'USD': 'Volume (USD)'},
    title='Volume by Category in USD',
    text_auto=True
)
st.plotly_chart(fig_usd)

# Second chart - Volume in ETH
st.subheader("Volume by Category (ETH)")
fig_eth = px.bar(
    df_eth.sort_values('ETH', ascending=False),
    x='CATEGORY',
    y='ETH',
    labels={'ETH': 'Volume (ETH)'},
    title='Volume by Category in ETH',
    text_auto=True
)
st.plotly_chart(fig_eth)

