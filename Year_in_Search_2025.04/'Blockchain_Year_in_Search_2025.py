# streamlit_app.py

import streamlit as st

# Basic page config
st.set_page_config(
    page_title="Blockchain Year in Search 2025",
    page_icon="📊",
    layout="wide",
)

# --- Title ---
st.title("Blockchain Year in Search 2025")
st.caption("Explore what people searched for in crypto and blockchain throughout the year.")

# --- Category chips ---
categories = [
    "Coins & tokens",
    "DeFi protocols",
    "Memecoins",
    "NFTs & collectibles",
    "Airdrops & farming",
    "Hacks & regulation",
]

# Use a horizontal radio as pill-style quick-access buttons
selected_category = st.radio(
    "Choose a category",
    categories,
    horizontal=True,
    label_visibility="collapsed",
)

st.divider()

# --- Placeholder content area (to be expanded later) ---
st.subheader(selected_category)

st.info(
    f"This is a placeholder section for **{selected_category}**.\n\n"
    "Later you can add charts, tables, and insights about the top searches, "
    "trending topics, and notable events for this category in 2025."
)
