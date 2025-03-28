

import streamlit as st
import pandas as pd
import matplotlib.pyplot as plt
import streamlit as st
from datetime import datetime, timedelta

# Define the date range for the slider
start_date = datetime(2022, 1, 1)
end_date = datetime(2025, 3, 28)

# Create the slider
selected_start_date, selected_end_date = st.slider(
    "Select a date range:",
    min_value=start_date,
    max_value=end_date,
    value=(start_date, end_date),
    format="MM/DD/YYYY"
)

st.write(f"Filtering data from {selected_start_date.strftime('%Y-%m-%d')} to {selected_end_date.strftime('%Y-%m-%d')}")


import pandas as pd

# Sample DataFrame
data = pd.DataFrame({
    "date": pd.date_range(start="2022-01-01", periods=1000, freq='D'),
    "blockchain": ["Ethereum", "Bitcoin", "Binance Smart Chain"] * 333 + ["Cardano"],
    "value": range(1000)
})

# Filter data based on selections
filtered_data = data[
    (data["date"] >= selected_start_date) &
    (data["date"] <= selected_end_date) &
    (data["blockchain"].isin(selected_blockchains))
]

st.write(filtered_data)

# عنوان داشبورد
st.title("📊 DEX Dashboard – DeFi Insights")

# دیتای تستی
data = {
    "project": ["Uniswap", "Curve", "Sushiswap"],
    "volume_usd": [21000000, 3400000, 1200000],
    "tvl_usd": [120000000, 87000000, 40000000]
}
df = pd.DataFrame(data)

# جدول دیتا
st.subheader("📋 Protocol Stats")
st.dataframe(df)

# نمودار
st.subheader("📈 Volume Chart")
fig, ax = plt.subplots()
ax.bar(df["project"], df["volume_usd"])
ax.set_ylabel("Volume (USD)")
st.pyplot(fig)

# عنوان داشبورد
st.title("📊 DEX Dashboard – DeFi Insights")

# دیتای تستی
data = {
    "project": ["Uniswap", "Curve", "Sushiswap"],
    "volume_usd": [21000000, 3400000, 1200000],
    "tvl_usd": [120000000, 87000000, 40000000]
}
df = pd.DataFrame(data)

# جدول دیتا
st.subheader("📋 Protocol Stats")
st.dataframe(df)

# نمودار
st.subheader("📈 Volume Chart")
fig, ax = plt.subplots()
ax.bar(df["project"], df["volume_usd"])
ax.set_ylabel("Volume (USD)")
st.pyplot(fig)

st.title("📊 DEX Dashboard – DeFi Insights")

data = {
    "project": ["Uniswap", "Curve", "Sushiswap"],
    "volume_usd": [21000000, 3400000, 1200000],
    "tvl_usd": [120000000, 87000000, 40000000]
}
df = pd.DataFrame(data)

st.subheader("📋 Protocol Stats")
st.dataframe(df)

st.subheader("📈 Volume Chart")
fig, ax = plt.subplots()
ax.bar(df["project"], df["volume_usd"])
ax.set_ylabel("Volume (USD)")
st.pyplot(fig)





