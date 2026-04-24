import streamlit as st
import pandas as pd
import plotly.graph_objects as go
import requests
from io import StringIO
import os
import base64

# ── PAGE CONFIG ───────────────────────────────────────────────────────────────
st.set_page_config(
    page_title="ACS Campaign Report",
    page_icon="📊",
    layout="wide",
    initial_sidebar_state="expanded",
)

# ── PALETTE ───────────────────────────────────────────────────────────────────
BG      = "#0a0a0f"
SURFACE = "#111118"
CARD    = "#16161f"
BORDER  = "#2a2a3a"
PINK    = "#e8198b"
BLUE    = "#00b4ff"
CYAN    = "#00e5cc"
GREEN   = "#10b981"
AMBER   = "#f59e0b"
RED     = "#ef4444"
WHITE   = "#f4f4f8"
MUTED   = "#9494b8"
PURPLE  = "#8b5cf6"
GRID    = "#13131c"
DIVIDER = "#2a2a3a"

FONT_DISPLAY = "'Playfair Display', Georgia, serif"
FONT_BODY    = "'Calibri', 'Trebuchet MS', sans-serif"

# ── DATA ──────────────────────────────────────────────────────────────────────
GITHUB   = "https://raw.githubusercontent.com/bellatrix-ds/blockchain-dashboards-and-visualizations/refs/heads/main/05_Astar/data"
DATA_DIR = os.path.join(os.path.dirname(os.path.abspath(__file__)), "data")

@st.cache_data(ttl=3600)
def load(filename):
    local = os.path.join(DATA_DIR, filename)
    if os.path.exists(local):
        return pd.read_csv(local)
    try:
        r = requests.get(f"{GITHUB}/{filename}", timeout=10)
        r.raise_for_status()
        return pd.read_csv(StringIO(r.text))
    except Exception:
        pass
    return _sample(filename)

def _sample(f):
    if f == "tvl_trajectory.csv":
        # Correct chronological order: pre-ACS months, then ACS seasons, then post-ACS months
        return pd.DataFrame({
            "period":     ["Nov'24","Dec'24","Jan'25","Feb'25","Mar'25","Apr'25","May'25","Jun'25","Jul'25","Aug'25","Sep'25","Oct'25","Nov'25","Dec'25","Jan'26","Feb'26","Mar'26","Apr'26"],
            "tvl_usd_m":  [2,       5,       12,      60,      100,     140,     226,     152,     80,      45,      30,      22,      18,      15,      12,      11,      10,      9.5],
            "acs_active": [0,       0,       0,       0,       1,       1,       1,       0,       0,       0,       0,       0,       0,       0,       0,       0,       0,       0],
        })
    if f == "season_metrics.csv":
        return pd.DataFrame({
            "season":       ["S1","S2","S3","S4","S5","S6","S7","S8","S9","Post-ACS"],
            "tvs_usd_m":    [73,108,119,154,137,125,175,199,220,10],
            "daily_tx_k":   [1600,1155,1564,1457,991,1042,1115,819,901,175],
            "new_wallets_k":[584,340,292,121,364,389,231,510,529,None],
        })
    if f == "protocol_tvl.csv":
        return pd.DataFrame({
            "protocol":       ["Kyo Finance","Untitled Bank","SakeFinance","SoneX","QuickSwap","Velodrome"],
            "acs_peak_tvl_m": [55,40,28,42,15,20],
            "current_tvl_m":  [0.99,0.25,1.32,0.086,1.79,0.50],
            "retention_pct":  [1.8,0.6,4.7,0.2,11.9,2.5],
            "verdict":        ["gone","gone","holds","gone","holds","weak"],
        })
    if f == "astr_bridge.csv":
        return pd.DataFrame({
            "season":   ["S1","S2","S3","S4","S5","S6","S7","S8","S9"],
            "inflow_m": [133.7,128.0,0.08,0.11,0.10,0.02,0.02,0.09,0.05],
        })
    if f == "gas_per_tx.csv":
        return pd.DataFrame({
            "season":      ["S1","S2","S3","S4","S5","S6","S7","S8","S9"],
            "gas_per_tx_k":[262,295,286,447,207,280,124,110,110],
        })
    if f == "asset_retention.csv":
        return pd.DataFrame({
            "asset":      ["SolvBTC.BBN","ASTR","vASTR","USDC","wstASTR"],
            "pct_change": [-62,-23,2.7,0.9,19.8],
        })
    if f == "gaming_defi_retention.csv":
        return pd.DataFrame({
            "protocol":      ["Yoki Legacy","Evermoon","SakeFinance","Kyo Finance","Untitled Bank"],
            "retention_pct": [13,6,4.7,1.8,0.6],
            "type":          ["gaming","gaming","defi","defi","defi"],
        })
    return pd.DataFrame()

def chart_style(fig, height=380):
    fig.update_layout(
        height=height,
        paper_bgcolor=CARD,
        plot_bgcolor=CARD,
        font=dict(family=FONT_BODY, color=WHITE, size=13),
        margin=dict(l=16, r=16, t=24, b=16),
        legend=dict(bgcolor="rgba(0,0,0,0)", font=dict(size=12, color=MUTED),
                    orientation="h", yanchor="bottom", y=1.02, xanchor="left", x=0),
        xaxis=dict(gridcolor=GRID, linecolor=BORDER, tickfont=dict(size=11, color=MUTED), showgrid=True),
        yaxis=dict(gridcolor=GRID, linecolor=BORDER, tickfont=dict(size=11, color=MUTED), showgrid=True),
    )
    return fig

def img_to_b64(path):
    try:
        with open(path, "rb") as f:
            return base64.b64encode(f.read()).decode()
    except Exception:
        return None

# ── LOAD DATA ─────────────────────────────────────────────────────────────────
df_tvl     = load("tvl_trajectory.csv")
df_seasons = load("season_metrics.csv")
df_proto   = load("protocol_tvl.csv")
df_bridge  = load("astr_bridge.csv")
df_gas     = load("gas_per_tx.csv")
df_assets  = load("asset_retention.csv")
df_gaming  = load("gaming_defi_retention.csv")

# ── GLOBAL CSS ────────────────────────────────────────────────────────────────
st.markdown(f"""
<style>
@import url('https://fonts.googleapis.com/css2?family=Playfair+Display:wght@400;600;700;800&display=swap');

html, body, [class*="css"] {{
    background: {BG} !important;
    color: {WHITE} !important;
}}
.stApp {{ background: {BG} !important; }}
.block-container {{ padding: 0 !important; max-width: 100% !important; }}
header[data-testid="stHeader"] {{ background: transparent !important; border-bottom: none !important; }}
footer {{ display: none !important; }}
#MainMenu {{ visibility: hidden !important; }}

/* Sidebar */
[data-testid="stSidebar"] {{
    background: {SURFACE} !important;
    border-right: 1px solid {BORDER} !important;
    width: 270px !important;
}}
section[data-testid="stSidebarContent"] {{
    padding: 0 !important;
    background: {SURFACE} !important;
}}

/* Typography */
h1, h2, h3, .display-font {{
    font-family: {FONT_DISPLAY} !important;
}}
p, span, div, td, th, label {{
    font-family: {FONT_BODY} !important;
}}

/* Cards */
.card {{
    background: {CARD};
    border: 1px solid {BORDER};
    border-radius: 12px;
    padding: 28px;
    height: 100%;
}}
.card-sm {{
    background: {CARD};
    border: 1px solid {BORDER};
    border-radius: 10px;
    padding: 20px 24px;
}}

/* Section */
.section-wrap {{
    padding: 60px 64px 48px;
}}
.section-divider {{
    border: none;
    border-top: 1px solid {DIVIDER};
    margin: 0;
}}

/* KPI */
.kpi-label {{
    font-family: {FONT_BODY} !important;
    font-size: 11px; font-weight: 700;
    text-transform: uppercase; letter-spacing: 0.1em;
    color: {MUTED}; margin-bottom: 10px;
}}
.kpi-number {{
    font-family: {FONT_DISPLAY} !important;
    font-size: 40px; font-weight: 800;
    line-height: 1; margin-bottom: 8px;
}}
.kpi-sub {{
    font-family: {FONT_BODY} !important;
    font-size: 13px; color: {MUTED}; line-height: 1.5;
}}

/* Caption */
.caption {{
    font-family: {FONT_BODY} !important;
    font-size: 13px; color: {MUTED}; line-height: 1.65;
    margin-top: 14px; padding: 14px 18px;
    background: rgba(255,255,255,0.02);
    border-left: 3px solid {BORDER};
    border-radius: 0 6px 6px 0;
}}

/* Insight box */
.insight-box {{
    background: rgba(0,229,204,0.05);
    border: 1px solid rgba(0,229,204,0.2);
    border-radius: 10px; padding: 20px 22px; margin-bottom: 14px;
}}
.insight-label {{
    font-family: {FONT_BODY} !important;
    font-size: 10px; font-weight: 700;
    text-transform: uppercase; letter-spacing: 0.1em;
    color: {CYAN}; margin-bottom: 8px;
}}

/* Rec card */
.rec-card {{
    background: {CARD}; border: 1px solid {BORDER};
    border-top: 3px solid {BLUE};
    border-radius: 0 0 12px 12px; padding: 24px; height: 100%;
}}
.rec-num {{
    font-family: {FONT_BODY} !important;
    font-size: 11px; font-weight: 700;
    text-transform: uppercase; letter-spacing: 0.1em;
    color: {BLUE}; margin-bottom: 8px;
}}
.rec-metric {{
    font-family: {FONT_BODY} !important;
    font-size: 12px; color: {CYAN}; font-weight: 600;
    border-top: 1px solid {BORDER}; padding-top: 12px;
}}

/* Nav links hover */
.nav-link:hover {{ color: {WHITE} !important; }}

/* Plotly */
.stPlotlyChart {{ border-radius: 10px; overflow: hidden; }}
</style>
""", unsafe_allow_html=True)

# ── LOAD IMAGES ───────────────────────────────────────────────────────────────
profile_path = os.path.join(DATA_DIR, "profile.jpg")
logo_path    = os.path.join(DATA_DIR, "astar_logo.png")
profile_b64  = img_to_b64(profile_path)
logo_b64     = img_to_b64(logo_path)

# ══════════════════════════════════════════════════════════════════════════════
# SIDEBAR
# ══════════════════════════════════════════════════════════════════════════════
with st.sidebar:

    # ── NAVIGATION FIRST ─────────────────────────────────────────────────────
    nav_link = f"display:block;padding:10px 0;font-size:13px;font-family:{FONT_BODY};color:{MUTED};text-decoration:none;border-bottom:1px solid {BORDER}22;transition:color 0.2s;"
    st.markdown(f"""
    <div style="padding:32px 24px 16px;">
      <div style="font-family:{FONT_BODY};font-size:11px;font-weight:700;text-transform:uppercase;
                  letter-spacing:0.12em;color:{MUTED};margin-bottom:16px;">
        Report Sections
      </div>
      <a href="#campaign-summary" class="nav-link" style="{nav_link}">01 &nbsp; Campaign Summary</a>
      <a href="#tvl-activity"     class="nav-link" style="{nav_link}">02 &nbsp; TVL &amp; Activity</a>
      <a href="#protocol-autopsy" class="nav-link" style="{nav_link}">03 &nbsp; Protocol Autopsy</a>
      <a href="#astr-token"       class="nav-link" style="{nav_link}">04 &nbsp; ASTR Token</a>
      <a href="#gaming-vs-defi"   class="nav-link" style="{nav_link}">05 &nbsp; Gaming vs DeFi</a>
      <a href="#insights-recs"    class="nav-link" style="{nav_link}">06 &nbsp; Insights &amp; Recommendations</a>
    </div>
    <hr style="border:none;border-top:1px solid {BORDER};margin:8px 0 0;">
    """, unsafe_allow_html=True)

    # ── PROFILE ───────────────────────────────────────────────────────────────
    if profile_b64:
        photo_html = f'<img src="data:image/jpeg;base64,{profile_b64}" style="width:130px;height:130px;border-radius:12px;object-fit:cover;border:2px solid {BORDER};display:block;margin-bottom:16px;">'
    else:
        photo_html = f"""<div style="width:120px;height:120px;border-radius:12px;
            background:linear-gradient(135deg,{BLUE}33,{PINK}33);
            border:2px solid {BORDER};margin-bottom:16px;
            display:flex;align-items:center;justify-content:center;">
          <span style="font-size:40px;">👤</span>
        </div>"""

    btn = f"display:block;width:100%;padding:11px 16px;background:{CARD};border:1px solid {BORDER};border-radius:9px;color:{WHITE};font-size:13px;font-family:{FONT_BODY};font-weight:600;text-decoration:none;text-align:center;margin-bottom:9px;"

    st.markdown(f"""
    <div style="padding:24px 24px 36px;">
      {photo_html}
      <div style="font-family:{FONT_DISPLAY};font-size:20px;font-weight:700;color:{WHITE};margin-bottom:4px;">My name is Bella</div>
      <div style="font-family:{FONT_BODY};font-size:13px;color:{MUTED};margin-bottom:24px;line-height:1.5;">Blockchain Research Analyst</div>
      <div style="font-family:{FONT_BODY};font-size:11px;font-weight:700;text-transform:uppercase;letter-spacing:0.1em;color:{MUTED};margin-bottom:14px;">Get in touch</div>
      <a href="https://bellabahrami.carrd.co/" target="_blank" style="{btn}">🌐 &nbsp;Portfolio</a>
      <a href="https://github.com/bellatrix-ds"  target="_blank" style="{btn}">🐙 &nbsp;GitHub</a>
      <a href="https://x.com/Bella52496"         target="_blank" style="{btn}">𝕏 &nbsp;x.com</a>
      <a href="https://t.me/bella_trickss"       target="_blank" style="{btn}">✈️ &nbsp;Telegram</a>
      <a href="mailto:bellabahramii@gmail.com"               style="{btn}">✉️ &nbsp;Email</a>
      <div style="font-family:{FONT_BODY};font-size:10px;color:{BORDER};line-height:1.8;margin-top:20px;">
        Analysis as of April 2026<br>
        Data: DeFiLlama, Blockscout, Astar Forum
      </div>
    </div>
    """, unsafe_allow_html=True)

# ══════════════════════════════════════════════════════════════════════════════
# DASHBOARD TITLE HEADER
# ══════════════════════════════════════════════════════════════════════════════
if logo_b64:
    logo_html = f'<img src="data:image/png;base64,{logo_b64}" style="height:44px;object-fit:contain;margin-right:16px;vertical-align:middle;">'
else:
    logo_html = f'<div style="width:44px;height:44px;border-radius:8px;background:{BLUE}33;border:1px solid {BLUE}44;display:inline-flex;align-items:center;justify-content:center;margin-right:16px;vertical-align:middle;"><span style="font-size:22px;">⭐</span></div>'

st.markdown(f"""
<div style="background:{SURFACE};border-bottom:1px solid {BORDER};padding:36px 64px 28px;">
  <div style="text-align:center;">
    <div style="display:inline-flex;align-items:center;justify-content:center;gap:16px;margin-bottom:14px;">
      {logo_html}
      <div style="font-family:{FONT_DISPLAY};font-size:34px;font-weight:800;color:{WHITE};line-height:1.2;">
        ACS Campaign Performance Report
      </div>
    </div>
    <div style="font-family:{FONT_BODY};font-size:15px;color:{MUTED};margin-bottom:20px;">
      Feb 20 &ndash; May 30, 2025 &nbsp;&nbsp;|&nbsp;&nbsp; Soneium Ecosystem &nbsp;&nbsp;|&nbsp;&nbsp; Analysis as of April 2026
    </div>
    <div style="display:flex;gap:8px;flex-wrap:wrap;justify-content:center;">
      <span style="background:rgba(16,185,129,0.12);color:{GREEN};border:1px solid rgba(16,185,129,0.25);font-size:11px;font-family:{FONT_BODY};font-weight:700;padding:5px 14px;border-radius:5px;letter-spacing:0.06em;">PRE-ACS</span>
      <span style="background:rgba(0,180,255,0.12);color:{BLUE};border:1px solid rgba(0,180,255,0.25);font-size:11px;font-family:{FONT_BODY};font-weight:700;padding:5px 14px;border-radius:5px;letter-spacing:0.06em;">ACS ACTIVE</span>
      <span style="background:rgba(245,158,11,0.12);color:{AMBER};border:1px solid rgba(245,158,11,0.25);font-size:11px;font-family:{FONT_BODY};font-weight:700;padding:5px 14px;border-radius:5px;letter-spacing:0.06em;">POST-ACS</span>
      <span style="background:rgba(239,68,68,0.12);color:{RED};border:1px solid rgba(239,68,68,0.25);font-size:11px;font-family:{FONT_BODY};font-weight:700;padding:5px 14px;border-radius:5px;letter-spacing:0.06em;">CURRENT</span>
    </div>
  </div>
</div>
""", unsafe_allow_html=True)


# ── HELPER: section header ────────────────────────────────────────────────────
def section_header(anchor_id, eyebrow, heading, body=None):
    body_html = f'<div style="font-family:{FONT_BODY};font-size:15px;color:{MUTED};line-height:1.75;max-width:760px;margin:0 auto 36px;">{body}</div>' if body else ""
    st.markdown(f"""
    <div id="{anchor_id}" style="text-align:center;padding:60px 64px 8px;">
      <div style="font-family:{FONT_BODY};font-size:11px;font-weight:700;text-transform:uppercase;
                  letter-spacing:0.14em;color:{BLUE};margin-bottom:10px;">{eyebrow}</div>
      <div style="font-family:{FONT_DISPLAY};font-size:30px;font-weight:800;color:{WHITE};
                  line-height:1.25;margin-bottom:14px;">{heading}</div>
      {body_html}
    </div>
    """, unsafe_allow_html=True)

def gray_divider():
    st.markdown(f'<hr style="border:none;border-top:1px solid {DIVIDER};margin:0;">', unsafe_allow_html=True)


# ══════════════════════════════════════════════════════════════════════════════
# SECTION 1 — CAMPAIGN SUMMARY
# ══════════════════════════════════════════════════════════════════════════════
section_header(
    "campaign-summary",
    "01 — Campaign Summary",
    "What happened, and what didn't.",
    "The ACS campaign delivered impressive headline numbers: $226M TVL, 3.57M wallets, 147M transactions. But 95.8% of that TVL vanished within 90 days of the reward claim date. This report quantifies what stuck, what left, and what Astar should do differently next time."
)

with st.container():
    st.markdown("<div style='padding:0 64px;'>", unsafe_allow_html=True)

    k1, k2, k3, k4 = st.columns(4)
    for col, label, val, sub, color in [
        (k1, "Peak TVL Reached",  "$226M", "Season 9, May 2025",                WHITE),
        (k2, "TVL Today",         "$9.5M", "95.8% collapse in 90 days",         RED),
        (k3, "Wallets Retained",  "3-5%",  "Of 3.57M unique campaign wallets",  AMBER),
        (k4, "Daily Tx Drop",     "87%",   "Post-ACS vs campaign average",      RED),
    ]:
        with col:
            st.markdown(f"""<div class="card">
              <div class="kpi-label">{label}</div>
              <div class="kpi-number" style="color:{color};">{val}</div>
              <div class="kpi-sub">{sub}</div>
            </div>""", unsafe_allow_html=True)

    st.markdown("<div style='height:16px'></div>", unsafe_allow_html=True)

    k5, k6, k7, k8 = st.columns(4)
    for col, label, val, sub in [
        (k5, "ASTR Bridged In",       "674.9M", "23% left within 30 days of claim"),
        (k6, "ASTR Distributed",      "80.3M",  "Of 100M budget, 19.7M unspent"),
        (k7, "ASTR vs All-Time High", "65%",    "$0.0084 price, $71.9M market cap"),
        (k8, "Pre-ACS Baseline TVL",  "$60M",   "ACS added 267% at its peak"),
    ]:
        with col:
            st.markdown(f"""<div class="card-sm">
              <div class="kpi-label">{label}</div>
              <div style="font-family:{FONT_DISPLAY};font-size:26px;font-weight:700;color:{WHITE};margin-bottom:6px;">{val}</div>
              <div class="kpi-sub">{sub}</div>
            </div>""", unsafe_allow_html=True)

    st.markdown("<div style='height:48px'></div>", unsafe_allow_html=True)

gray_divider()

# ══════════════════════════════════════════════════════════════════════════════
# SECTION 2 — TVL & ACTIVITY
# ══════════════════════════════════════════════════════════════════════════════
section_header(
    "tvl-activity",
    "02 — TVL and Activity",
    "The campaign created a mountain, not a foundation.",
    "TVL grew 267% during ACS. It collapsed 96% after. The charts below show exactly when activity became artificial and what the organic baseline actually looks like."
)

with st.container():
    st.markdown("<div style='padding:0 64px 60px;'>", unsafe_allow_html=True)

    # TVL chart — correct chronological x-axis, two clearly separated traces
    fig_tvl = go.Figure()

    acs_mask   = df_tvl["acs_active"] == 1
    pre_mask   = df_tvl["acs_active"] == 0

    x_all = df_tvl["period"].tolist()
    y_all = df_tvl["tvl_usd_m"].tolist()

    # Shaded ACS region
    x_acs = df_tvl.loc[acs_mask, "period"].tolist()
    y_acs = df_tvl.loc[acs_mask, "tvl_usd_m"].tolist()

    # Full TVL line
    fig_tvl.add_trace(go.Scatter(
        x=x_all, y=y_all,
        mode="lines",
        line=dict(color=PINK, width=3),
        fill="tozeroy",
        fillcolor="rgba(232,25,139,0.07)",
        name="Total TVL",
        hovertemplate="<b>%{x}</b><br>TVL: $%{y:.0f}M<extra></extra>",
    ))

    # ACS shading overlay
    fig_tvl.add_trace(go.Scatter(
        x=x_acs, y=y_acs,
        mode="none",
        fill="tozeroy",
        fillcolor="rgba(0,180,255,0.10)",
        name="ACS Active Period",
        hoverinfo="skip",
        showlegend=True,
    ))

    # Peak annotation
    fig_tvl.add_annotation(
        x="May'25", y=226,
        text="<b>Peak $226M</b>",
        showarrow=True, arrowhead=2, arrowcolor=PINK,
        font=dict(color=PINK, size=13, family=FONT_BODY),
        ax=0, ay=-44,
    )

    # Current annotation
    fig_tvl.add_annotation(
        x="Apr'26", y=9.5,
        text="<b>$9.5M today</b>",
        showarrow=False,
        font=dict(color=RED, size=12, family=FONT_BODY),
        xanchor="right", yshift=18,
    )

    # ACS label on chart
    fig_tvl.add_annotation(
        x="Apr'25", y=180,
        text="ACS Campaign Period",
        showarrow=False,
        font=dict(color=BLUE, size=11, family=FONT_BODY),
        bgcolor="rgba(0,180,255,0.1)",
        bordercolor=BLUE,
        borderwidth=1,
        borderpad=5,
    )

    chart_style(fig_tvl, height=440)
    fig_tvl.update_xaxes(tickangle=-35, tickfont=dict(size=11), tickmode="array",
                          tickvals=x_all, ticktext=x_all)
    fig_tvl.update_yaxes(tickprefix="$", ticksuffix="M", range=[0, 260])
    st.plotly_chart(fig_tvl, use_container_width=True, config={"displayModeBar": False})
    st.markdown(f"""<div class="caption"><b>What happened:</b> TVL grew from $60M (pre-ACS) to $226M peak, driven by SolvBTC.BBN deposits.
    When rewards ended May 30, SolvBTC.BBN exited 62% within 30 days of the June 10 claim date, accounting for the majority of the $216M collapse.
    The organic floor was always around $9-12M.</div>""", unsafe_allow_html=True)

    st.markdown("<div style='height:40px'></div>", unsafe_allow_html=True)

    col_l, col_r = st.columns([1.1, 1])
    with col_l:
        st.markdown(f"<div style='font-family:{FONT_BODY};font-size:12px;font-weight:700;color:{MUTED};text-transform:uppercase;letter-spacing:0.1em;margin-bottom:16px;'>Season-by-Season Breakdown</div>", unsafe_allow_html=True)
        rows = ""
        for _, row in df_seasons.iterrows():
            s   = str(row["season"])
            tvs = f"${row['tvs_usd_m']:.0f}M"
            dtx = f"{row['daily_tx_k']:.0f}K" if pd.notna(row.get("daily_tx_k")) else "--"
            nw  = f"{row['new_wallets_k']:.0f}K" if pd.notna(row.get("new_wallets_k")) else "--"
            is_post = s == "Post-ACS"
            sc  = RED if is_post else BLUE
            rows += f"""<tr style="border-bottom:1px solid {BORDER};{'background:rgba(239,68,68,0.04);' if is_post else ''}">
              <td style="padding:12px 16px;font-family:{FONT_BODY};font-size:13px;font-weight:700;color:{sc};">{s}</td>
              <td style="padding:12px 16px;font-family:{FONT_DISPLAY};font-size:15px;font-weight:700;color:{WHITE};">{tvs}</td>
              <td style="padding:12px 16px;font-family:{FONT_BODY};font-size:13px;color:{MUTED};">{dtx}</td>
              <td style="padding:12px 16px;font-family:{FONT_BODY};font-size:13px;color:{MUTED};">{nw}</td>
            </tr>"""
        st.markdown(f"""<div style="background:{CARD};border:1px solid {BORDER};border-radius:12px;overflow:hidden;">
          <table style="width:100%;border-collapse:collapse;">
            <thead><tr style="background:{SURFACE};border-bottom:2px solid {BORDER};">
              <th style="padding:12px 16px;font-family:{FONT_BODY};font-size:11px;color:{MUTED};text-align:left;font-weight:700;text-transform:uppercase;letter-spacing:0.08em;">Season</th>
              <th style="padding:12px 16px;font-family:{FONT_BODY};font-size:11px;color:{MUTED};text-align:left;font-weight:700;text-transform:uppercase;letter-spacing:0.08em;">TVS</th>
              <th style="padding:12px 16px;font-family:{FONT_BODY};font-size:11px;color:{MUTED};text-align:left;font-weight:700;text-transform:uppercase;letter-spacing:0.08em;">Daily Txns</th>
              <th style="padding:12px 16px;font-family:{FONT_BODY};font-size:11px;color:{MUTED};text-align:left;font-weight:700;text-transform:uppercase;letter-spacing:0.08em;">New Wallets</th>
            </tr></thead><tbody>{rows}</tbody>
          </table></div>""", unsafe_allow_html=True)

    with col_r:
        st.markdown(f"<div style='font-family:{FONT_BODY};font-size:12px;font-weight:700;color:{MUTED};text-transform:uppercase;letter-spacing:0.1em;margin-bottom:16px;'>Gas Per Transaction: Economic Depth Signal</div>", unsafe_allow_html=True)
        pt_colors = [RED if i == 3 else AMBER for i in range(len(df_gas))]
        fig_gas = go.Figure()
        fig_gas.add_trace(go.Scatter(
            x=df_gas["season"], y=df_gas["gas_per_tx_k"],
            mode="lines+markers", line=dict(color=AMBER, width=3),
            marker=dict(color=pt_colors, size=[16 if i==3 else 9 for i in range(len(df_gas))],
                        line=dict(color=BG, width=2)),
            fill="tozeroy", fillcolor="rgba(245,158,11,0.07)",
            hovertemplate="<b>%{x}</b><br>Gas/tx: %{y:.0f}K gas<extra></extra>",
        ))
        fig_gas.add_annotation(x="S4", y=447, text="<b>447K</b><br>Real DeFi",
            showarrow=True, arrowhead=2, arrowcolor=RED, font=dict(color=RED, size=12, family=FONT_BODY), ax=44, ay=-28)
        fig_gas.add_annotation(x="S5", y=207, text="Hollow farming begins",
            showarrow=False, font=dict(color=MUTED, size=11, family=FONT_BODY), yshift=16)
        chart_style(fig_gas, height=360)
        fig_gas.update_yaxes(ticksuffix="K gas", range=[0, 540])
        st.plotly_chart(fig_gas, use_container_width=True, config={"displayModeBar": False})
        st.markdown(f"""<div class="caption"><b>Key insight:</b> Gas/tx dropped 2.2x in Season 5 (447K to 207K). This is the exact moment activity shifted from genuine DeFi to low-complexity farming loops. Astar never published this signal.</div>""", unsafe_allow_html=True)

    st.markdown("</div>", unsafe_allow_html=True)

gray_divider()

# ══════════════════════════════════════════════════════════════════════════════
# SECTION 3 — PROTOCOL AUTOPSY
# ══════════════════════════════════════════════════════════════════════════════
section_header(
    "protocol-autopsy",
    "03 — Protocol Autopsy",
    "Which protocols built something real?",
    "Six protocols received significant ACS allocation. Below is what each looked like at peak vs. today and an honest verdict on whether ACS helped them build a lasting user base or just rented temporary attention."
)

with st.container():
    st.markdown("<div style='padding:0 64px 60px;'>", unsafe_allow_html=True)

    df_p = df_proto.sort_values("acs_peak_tvl_m", ascending=False)
    fig_proto = go.Figure()
    fig_proto.add_trace(go.Bar(name="ACS Peak TVL", x=df_p["protocol"], y=df_p["acs_peak_tvl_m"],
        marker=dict(color=BLUE, opacity=0.7, line=dict(width=0)),
        hovertemplate="<b>%{x}</b><br>Peak: $%{y:.0f}M<extra></extra>", width=0.38))
    fig_proto.add_trace(go.Bar(name="Current TVL (Apr 2026)", x=df_p["protocol"], y=df_p["current_tvl_m"],
        marker=dict(color=PINK, opacity=0.9, line=dict(width=0)),
        hovertemplate="<b>%{x}</b><br>Current: $%{y:.2f}M<extra></extra>", width=0.38))
    fig_proto.update_layout(barmode="group", bargap=0.25)
    chart_style(fig_proto, height=380)
    fig_proto.update_yaxes(tickprefix="$", ticksuffix="M")
    fig_proto.update_xaxes(tickfont=dict(size=13))
    st.plotly_chart(fig_proto, use_container_width=True, config={"displayModeBar": False})
    st.markdown(f"""<div class="caption"><b>The collapse:</b> Kyo Finance $55M to $987K (98.2% drop). Untitled Bank $40M to $248K (99.4% drop). SoneX $42M to $86K (99.8% drop). QuickSwap and SakeFinance show the only meaningful retention, but both are multi-chain protocols whose TVL reflects their broader ecosystem, not Soneium-native demand.</div>""", unsafe_allow_html=True)

    st.markdown("<div style='height:40px'></div>", unsafe_allow_html=True)
    c_bar, c_cards = st.columns([1, 1.2])

    with c_bar:
        st.markdown(f"<div style='font-family:{FONT_BODY};font-size:12px;font-weight:700;color:{MUTED};text-transform:uppercase;letter-spacing:0.1em;margin-bottom:16px;'>90-Day Post-ACS TVL Retention Rate</div>", unsafe_allow_html=True)
        df_ret = df_proto.sort_values("retention_pct", ascending=True)
        bar_colors = [{"gone": RED, "weak": AMBER, "holds": GREEN}.get(v, MUTED) for v in df_ret["verdict"]]
        fig_ret = go.Figure(go.Bar(
            x=df_ret["retention_pct"], y=df_ret["protocol"], orientation="h",
            marker=dict(color=bar_colors, line=dict(width=0)),
            text=[f"  {v:.1f}%" for v in df_ret["retention_pct"]],
            textposition="outside", textfont=dict(size=13, color=WHITE, family=FONT_BODY),
            hovertemplate="<b>%{y}</b><br>Retention: %{x:.1f}%<extra></extra>", width=0.6,
        ))
        chart_style(fig_ret, height=360)
        fig_ret.update_xaxes(ticksuffix="%", range=[0, 16])
        fig_ret.update_yaxes(tickfont=dict(size=13))
        fig_ret.update_layout(margin=dict(l=8, r=60, t=20, b=16))
        st.plotly_chart(fig_ret, use_container_width=True, config={"displayModeBar": False})

    with c_cards:
        st.markdown(f"<div style='font-family:{FONT_BODY};font-size:12px;font-weight:700;color:{MUTED};text-transform:uppercase;letter-spacing:0.1em;margin-bottom:16px;'>Protocol Verdicts</div>", unsafe_allow_html=True)
        for name, verdict, change, desc in [
            ("Kyo Finance",   "gone",  "98.2%", "DEX with $55M ACS peak. Only 19 active wallets in April 2026. ACS bought temporary liquidity, not users."),
            ("Untitled Bank", "gone",  "99.4%", "Lending platform. Growth was entirely incentive-driven. No organic borrowing demand emerged post-rewards."),
            ("SakeFinance",   "holds", "95.3%", "Best DeFi retention at 4.7%. Existing LP base from other chains provided a non-zero organic floor."),
            ("QuickSwap",     "holds", "88.1%", "11.9% retention is misleading. Reflects global QuickSwap liquidity, not Soneium-native demand."),
            ("Velodrome",     "weak",  "97.5%", "Protocol-owned liquidity showed some resilience but could not survive removal of ASTR yield incentives."),
            ("SoneX",         "gone",  "99.8%", "Effectively zero TVL remaining. Worst retention of all ACS participants."),
        ]:
            vc = RED if verdict == "gone" else (GREEN if verdict == "holds" else AMBER)
            st.markdown(f"""<div style="background:{CARD};border:1px solid {BORDER};border-radius:10px;padding:14px 18px;margin-bottom:10px;display:flex;align-items:flex-start;gap:14px;">
              <div style="min-width:115px;">
                <div style="font-family:{FONT_DISPLAY};font-size:13px;font-weight:700;color:{WHITE};margin-bottom:6px;">{name}</div>
                <div style="display:flex;gap:6px;align-items:center;flex-wrap:wrap;">
                  <span style="background:rgba(0,0,0,0.3);color:{vc};border:1px solid {vc}44;font-family:{FONT_BODY};font-size:11px;font-weight:700;padding:2px 8px;border-radius:4px;">{verdict.upper()}</span>
                  <span style="font-family:{FONT_BODY};font-size:12px;font-weight:700;color:{RED};">-{change}</span>
                </div>
              </div>
              <div style="font-family:{FONT_BODY};font-size:13px;color:{MUTED};line-height:1.6;border-left:1px solid {BORDER};padding-left:14px;">{desc}</div>
            </div>""", unsafe_allow_html=True)

    st.markdown("</div>", unsafe_allow_html=True)

gray_divider()

# ══════════════════════════════════════════════════════════════════════════════
# SECTION 4 — ASTR TOKEN
# ══════════════════════════════════════════════════════════════════════════════
section_header(
    "astr-token",
    "04 — ASTR Token",
    "Did ASTR earn its place on Soneium?",
    "Astar's core goal was to make ASTR the economic engine of Soneium, used as collateral, gas, and governance. The bridge flow and asset retention data shows whether that goal was achieved."
)

with st.container():
    st.markdown("<div style='padding:0 64px 60px;'>", unsafe_allow_html=True)
    c_br, c_as = st.columns(2)

    with c_br:
        st.markdown(f"<div style='font-family:{FONT_BODY};font-size:12px;font-weight:700;color:{MUTED};text-transform:uppercase;letter-spacing:0.1em;margin-bottom:16px;'>ASTR Bridge Inflow by Season</div>", unsafe_allow_html=True)
        bc = [RED if v > 50 else (AMBER if v > 1 else BLUE) for v in df_bridge["inflow_m"]]
        fig_br = go.Figure(go.Bar(x=df_bridge["season"], y=df_bridge["inflow_m"],
            marker=dict(color=bc, line=dict(width=0)),
            hovertemplate="<b>%{x}</b><br>Inflow: %{y:.2f}M ASTR<extra></extra>", width=0.6))
        fig_br.add_hline(y=10, line_dash="dot", line_color="rgba(232,25,139,0.5)", line_width=1.5,
            annotation_text="avg reward rate", annotation_font=dict(size=11, color=PINK, family=FONT_BODY), annotation_position="right")
        chart_style(fig_br, height=360)
        fig_br.update_yaxes(ticksuffix="M ASTR")
        fig_br.update_xaxes(tickfont=dict(size=13))
        st.plotly_chart(fig_br, use_container_width=True, config={"displayModeBar": False})
        st.markdown(f"""<div class="caption"><b>Bridge saturation:</b> 99% of ASTR bridged happened in the first two seasons (S1: 133.7M, S2: 128.0M). The remaining 7 seasons combined added only 0.47M ASTR, yet rewards continued at full rate for all 9 seasons.</div>""", unsafe_allow_html=True)

    with c_as:
        st.markdown(f"<div style='font-family:{FONT_BODY};font-size:12px;font-weight:700;color:{MUTED};text-transform:uppercase;letter-spacing:0.1em;margin-bottom:16px;'>Asset Retention: 30 Days After Claim Date</div>", unsafe_allow_html=True)
        df_a = df_assets.sort_values("pct_change")
        a_colors = [RED if v < -30 else (PINK if v < 0 else GREEN) for v in df_a["pct_change"]]
        fig_a = go.Figure(go.Bar(
            x=df_a["pct_change"], y=df_a["asset"], orientation="h",
            marker=dict(color=a_colors, line=dict(width=0)),
            text=[f"{v:+.1f}%" for v in df_a["pct_change"]],
            textposition="outside", textfont=dict(size=13, color=WHITE, family=FONT_BODY),
            hovertemplate="<b>%{y}</b><br>Change: %{x:+.1f}%<extra></extra>", width=0.55,
        ))
        chart_style(fig_a, height=360)
        fig_a.update_xaxes(ticksuffix="%", range=[-85, 40])
        fig_a.update_yaxes(tickfont=dict(size=13))
        fig_a.update_layout(margin=dict(l=8, r=60, t=20, b=16))
        st.plotly_chart(fig_a, use_container_width=True, config={"displayModeBar": False})
        st.markdown(f"""<div class="caption"><b>What stayed:</b> SolvBTC.BBN (-62%) drove the collapse. USDC (+0.9%) and liquid staking (wstASTR +19.8%, vASTR +2.7%) were the stickiest assets, the only genuine ASTR utility signal in this dataset.</div>""", unsafe_allow_html=True)

    st.markdown("<div style='height:40px'></div>", unsafe_allow_html=True)
    fa1, fa2, fa3 = st.columns(3)
    for col, color, title, body in [
        (fa1, RED,   "ASTR as Collateral: Failed",    "Kyo and Untitled Bank saw ASTR collateral collapse post-ACS. Users borrowed against ASTR to farm yield, not for genuine DeFi. No sustainable demand materialized."),
        (fa2, AMBER, "ASTR as Gas: Partial",          "Gas payments in ASTR continued post-ACS but at 87% lower volume. Gas revenue to the network essentially disappeared with the farmers."),
        (fa3, GREEN, "ASTR Liquid Staking: Bright Spot", "wstASTR (+19.8%) and vASTR (+2.7%) are the only assets that grew after the claim date. This is genuine product-market fit Astar should build on."),
    ]:
        with col:
            st.markdown(f"""<div class="card" style="border-left:3px solid {color};">
              <div style="font-family:{FONT_DISPLAY};font-size:15px;font-weight:700;color:{WHITE};margin-bottom:12px;">{title}</div>
              <div style="font-family:{FONT_BODY};font-size:13px;color:{MUTED};line-height:1.7;">{body}</div>
            </div>""", unsafe_allow_html=True)

    st.markdown("</div>", unsafe_allow_html=True)

gray_divider()

# ══════════════════════════════════════════════════════════════════════════════
# SECTION 5 — GAMING VS DEFI
# ══════════════════════════════════════════════════════════════════════════════
section_header(
    "gaming-vs-defi",
    "05 — Gaming vs DeFi",
    "Gaming keeps users. DeFi rents them.",
    "Astar's pitch to Sony was we bring gamers onchain. The retention data supports this, but only partially. Gaming protocols outperform DeFi on retention, but even the best gaming protocol falls well below what successful gaming chains achieve."
)

with st.container():
    st.markdown("<div style='padding:0 64px 60px;'>", unsafe_allow_html=True)
    cg1, cg2 = st.columns([1, 1.1])

    with cg1:
        st.markdown(f"<div style='font-family:{FONT_BODY};font-size:12px;font-weight:700;color:{MUTED};text-transform:uppercase;letter-spacing:0.1em;margin-bottom:16px;'>Retention Rate by Protocol Type</div>", unsafe_allow_html=True)
        df_gd = df_gaming.sort_values("retention_pct", ascending=True)
        gd_colors = [PURPLE if t == "gaming" else BLUE for t in df_gd["type"]]
        fig_gd = go.Figure()
        fig_gd.add_trace(go.Bar(
            x=df_gd["retention_pct"], y=df_gd["protocol"], orientation="h",
            marker=dict(color=gd_colors, line=dict(width=0)),
            text=[f"  {v:.1f}%" for v in df_gd["retention_pct"]],
            textposition="outside", textfont=dict(size=14, color=WHITE, family=FONT_BODY),
            hovertemplate="<b>%{y}</b><br>Retention: %{x:.1f}%<extra></extra>", width=0.6,
        ))
        fig_gd.add_trace(go.Bar(x=[None], y=[None], marker_color=PURPLE, name="Gaming", showlegend=True))
        fig_gd.add_trace(go.Bar(x=[None], y=[None], marker_color=BLUE,   name="DeFi",   showlegend=True))
        chart_style(fig_gd, height=380)
        fig_gd.update_xaxes(ticksuffix="%", range=[0, 18])
        fig_gd.update_yaxes(tickfont=dict(size=13))
        fig_gd.update_layout(margin=dict(l=8, r=70, t=40, b=16))
        st.plotly_chart(fig_gd, use_container_width=True, config={"displayModeBar": False})

    with cg2:
        st.markdown(f"<div style='font-family:{FONT_BODY};font-size:12px;font-weight:700;color:{MUTED};text-transform:uppercase;letter-spacing:0.1em;margin-bottom:16px;'>What Drives the Gap</div>", unsafe_allow_html=True)
        for color, title, body in [
            (PURPLE, "Yoki Legacy: 13% retention",  "Completion-based mechanic (collect-a-set NFTs) creates a goal loop that keeps users returning independently of rewards. Once users start a collection, they have a non-financial reason to come back. Genuine habit formation."),
            (PURPLE, "Evermoon: 6% retention",      "Competitive MOBA format. Higher engagement ceiling but less habit-forming. Users who stopped winning tournaments had no secondary reason to return post-rewards."),
            (BLUE,   "DeFi average: 1.5%",          "Pure yield optimization. When the yield moves, the user moves. No DeFi protocol had product differentiation strong enough to retain users at sub-market rates."),
            (CYAN,   "The key strategic insight",   "Mechanics creating non-financial goals such as collecting, ranking, or owning rare items retain users at 2 to 8 times the rate of financial-only mechanics. Require gaming protocols to demonstrate a non-financial retention hook before receiving ACS 2.0 allocation."),
        ]:
            st.markdown(f"""<div style="background:{CARD};border:1px solid {BORDER};border-left:3px solid {color};border-radius:0 10px 10px 0;padding:16px 18px;margin-bottom:12px;">
              <div style="font-family:{FONT_DISPLAY};font-size:13px;font-weight:700;color:{WHITE};margin-bottom:8px;">{title}</div>
              <div style="font-family:{FONT_BODY};font-size:13px;color:{MUTED};line-height:1.6;">{body}</div>
            </div>""", unsafe_allow_html=True)

    st.markdown("</div>", unsafe_allow_html=True)

gray_divider()

# ══════════════════════════════════════════════════════════════════════════════
# SECTION 6 — INSIGHTS & RECOMMENDATIONS
# ══════════════════════════════════════════════════════════════════════════════
section_header(
    "insights-recs",
    "06 — Insights and Recommendations",
    "What Astar does not know yet, and what to do about it.",
    "Four findings not published by Astar. Three recommendations their growth team can act on immediately."
)

with st.container():
    st.markdown("<div style='padding:0 64px 80px;'>", unsafe_allow_html=True)

    st.markdown(f"<div style='font-family:{FONT_BODY};font-size:12px;font-weight:700;color:{MUTED};text-transform:uppercase;letter-spacing:0.1em;margin-bottom:20px;'>New Insights: Not Published by Astar</div>", unsafe_allow_html=True)

    for num, title, body in [
        ("01", "The S5 Gas Signal: The Campaign Turned Hollow Before Astar Noticed",
         "Gas per transaction dropped from 447K to 207K gas in Season 5, a 2.2x decline indicating activity shifted from genuine DeFi interactions to simple reward-loop farming. This signal predated Astar's own allocation adjustments by two seasons and was never publicly disclosed."),
        ("02", "Bridge Saturation Happened in 20 Days, Rewards Ran for 100",
         "133.7M ASTR bridged in S1, 128.0M in S2, and less than 0.5M combined across S3 through S9. The bridge incentive was exhausted in the first 20% of the campaign. Yet the TVL-weighted formula continued distributing 70% of rewards at full rate based on locked-in capital for the remaining 80 days."),
        ("03", "Liquid Staking is the Only Genuine Utility Signal",
         "wstASTR (+19.8%) and vASTR (+2.7%) were the only assets that increased on Soneium in the 30 days following the reward claim date. These users engaged with ASTR liquid staking independently of ACS rewards and deepened their commitment. This cohort, however small, is Astar's actual product-market fit signal."),
        ("04", "Path of Soneium Received Gaming Rewards Without a Game",
         "The discretionary gaming allocation included Path of Soneium, a quest checklist app with no game loop, no competitive mechanic, and no reason for return visits. It received 2M ASTR per season, equivalent to Evermoon, despite a fraction of the retention. The gaming allocation had no minimum engagement criteria."),
    ]:
        st.markdown(f"""<div class="insight-box">
          <div class="insight-label">Insight {num}</div>
          <div style="font-family:{FONT_DISPLAY};font-size:16px;font-weight:700;color:{WHITE};margin-bottom:8px;">{title}</div>
          <div style="font-family:{FONT_BODY};font-size:13px;color:{MUTED};line-height:1.65;">{body}</div>
        </div>""", unsafe_allow_html=True)

    st.markdown("<div style='height:40px'></div>", unsafe_allow_html=True)
    st.markdown(f"<div style='font-family:{FONT_BODY};font-size:12px;font-weight:700;color:{MUTED};text-transform:uppercase;letter-spacing:0.1em;margin-bottom:20px;'>Three Recommendations for Astar's Growth Team</div>", unsafe_allow_html=True)

    r1, r2, r3 = st.columns(3)
    for col, num, timeline, title, body, metric in [
        (r1, "Recommendation 01", "Protocol + AFC, Q3 2026",
         "Replace TVL-weighted rewards with a 90-day vesting lock tied to retention thresholds",
         "SolvBTC.BBN exited 62% within 30 days, the majority of ACS peak TVL. A 90-day lock requiring 15% or more TVL retention as a prerequisite for full payout would have redirected around $130M in phantom TVL incentives toward protocols with genuine organic floors.",
         "15% or more TVL retention across top-5 protocols at 90 days post-campaign"),
        (r2, "Recommendation 02", "Growth team + Sentio, Q2-Q3 2026",
         "Redirect 30% of gaming allocation to a behavioral tier scored on return rate, not gas consumption",
         "Yoki Legacy's collection mechanic retained users at 2x Evermoon's rate with similar allocation. Path of Soneium received gaming rewards with zero game loop. A 3-metric behavioral dashboard covering 30-day return rate, sessions per retained wallet, and non-financial in-app actions would redirect incentives toward genuinely sticky products.",
         "Average 30-day return rate of 10% or more across gaming tier recipients"),
        (r3, "Recommendation 03", "Business dev + Startale Labs, Q4 2026",
         "Secure one Sony IP integration before launching any follow-on incentive campaign",
         "Soneium's gaming retention of 6 to 13% sits below comparable gaming chains at 15 to 40% because no ACS protocol had Sony IP access. Startale Labs' $63M Series A provides negotiating leverage. Gate ACS 2.0 gaming allocation on at least one signed Sony IP product being live at launch.",
         "50K or more unique wallets within 60 days of Sony IP product launch on Soneium"),
    ]:
        with col:
            st.markdown(f"""<div class="rec-card">
              <div class="rec-num">{num}</div>
              <div style="font-family:{FONT_BODY};font-size:11px;color:{MUTED};margin-bottom:14px;font-weight:500;">{timeline}</div>
              <div style="font-family:{FONT_DISPLAY};font-size:16px;font-weight:700;color:{WHITE};margin-bottom:12px;line-height:1.4;">{title}</div>
              <div style="font-family:{FONT_BODY};font-size:13px;color:{MUTED};line-height:1.7;margin-bottom:16px;">{body}</div>
              <div class="rec-metric">Success metric: {metric}</div>
            </div>""", unsafe_allow_html=True)

    # Footer
    st.markdown(f"""
    <div style="margin-top:56px;padding-top:20px;border-top:1px solid {BORDER};
                font-family:{FONT_BODY};font-size:12px;color:{MUTED};line-height:1.9;text-align:center;">
      <b style="color:{WHITE};">Data sources:</b> ACS Performance Reports (Astar Forum, 2025) &nbsp;|&nbsp;
      DeFiLlama (April 2026) &nbsp;|&nbsp; Blockscout Soneium Explorer &nbsp;|&nbsp; AFC Monthly Report (July 2025)<br>
      Estimated figures carry 15% uncertainty. L2 benchmark retention figures are approximate from public analyst reports.
    </div>
    """, unsafe_allow_html=True)

    st.markdown("</div>", unsafe_allow_html=True)
