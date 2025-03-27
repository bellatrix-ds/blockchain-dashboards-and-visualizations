

import streamlit as st
import pandas as pd
import matplotlib.pyplot as plt

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





