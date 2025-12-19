# streamlit_app.py

import streamlit as st

# ---------- Page config ----------
st.set_page_config(
    page_title="Blockchain Year in Search 2025",
    page_icon="🎄",
    layout="wide",
)

# ---------- Global styles ----------
st.markdown(
    """
    <style>
    /* Center content a bit */
    main .block-container {
        max-width: 900px;
        padding-top: 2rem;
    }

    /* Pill-style buttons */
    .stButton > button {
        border-radius: 999px;
        background-color: #e9f0ff;
        color: #2157d5;
        border: none;
        padding: 0.35rem 1.1rem;
        font-weight: 500;
        font-size: 0.95rem;
    }

    .stButton > button:hover {
        background-color: #d7e3ff;
        color: #1742a3;
    }
    </style>
    """,
    unsafe_allow_html=True,
)

# ---------- Header ----------
st.title("Blockchain Year in Search 2025")
st.caption("Explore what people searched for in crypto and blockchain throughout the year.")

st.write("")  # small spacer

# ---------- Category chips ----------
categories = [
    "Coins & tokens",
    "DeFi protocols",
    "Memecoins",
    "NFTs & collectibles",
    "Airdrops & farming",
    "Hacks & regulation",
]

# remember last clicked category
if "selected_category" not in st.session_state:
    st.session_state.selected_category = categories[0]

cols = st.columns(len(categories))

for col, cat in zip(cols, categories):
    with col:
        if st.button(cat, key=f"btn_{cat}"):
            st.session_state.selected_category = cat

st.divider()

# ---------- Placeholder content ----------
selected = st.session_state.selected_category
st.subheader(selected)
st.info(
    f"This is a placeholder area for **{selected}**.\n\n"
    "Later you can add charts, tables, and insights about the top searches "
    "and trends for this category in 2025."
)
