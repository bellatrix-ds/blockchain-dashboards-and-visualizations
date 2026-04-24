import streamlit as st
import pandas as pd
import plotly.graph_objects as go
import requests
from io import StringIO
import os

# ── PAGE CONFIG ───────────────────────────────────────────────────────────────
st.set_page_config(
    page_title="ACS Campaign Performance Report: Soneium Ecosystem",
    page_icon="📊",
    layout="wide",
    initial_sidebar_state="collapsed",
)

# ── PALETTE ───────────────────────────────────────────────────────────────────
BG       = "#0a0a0f"
SURFACE  = "#111118"
CARD     = "#16161f"
BORDER   = "#1f1f2e"
PINK     = "#e8198b"
BLUE     = "#00b4ff"
CYAN     = "#00e5cc"
GREEN    = "#10b981"
AMBER    = "#f59e0b"
RED      = "#ef4444"
WHITE    = "#f4f4f8"
MUTED    = "#64648a"
PURPLE   = "#8b5cf6"
GRID     = "#13131c"
FONT     = "Inter, system-ui, sans-serif"

# ── DATA ──────────────────────────────────────────────────────────────────────
GITHUB = "https://raw.githubusercontent.com/bellatrix-ds/blockchain-dashboards-and-visualizations/refs/heads/main/05_Astar/data"
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
        return pd.DataFrame({
            "period": ["Nov'24","Dec","Jan'25","Feb","S1","S2","S3","S4","S5","S6","S7","S8","S9","Jun'25","Jul","Sep","Jan'26","Apr'26"],
            "tvl_usd_m": [2,5,12,60,73,108,119,154,137,125,175,199,220,152,80,30,12,9.5],
            "acs_active": [0,0,0,0,1,1,1,1,1,1,1,1,1,0,0,0,0,0],
        })
    if f == "season_metrics.csv":
        return pd.DataFrame({
            "season": ["S1","S2","S3","S4","S5","S6","S7","S8","S9","Post-ACS"],
            "tvs_usd_m": [73,108,119,154,137,125,175,199,220,10],
            "daily_tx_k": [1600,1155,1564,1457,991,1042,1115,819,901,175],
            "new_wallets_k": [584,340,292,121,364,389,231,510,529,None],
        })
    if f == "protocol_tvl.csv":
        return pd.DataFrame({
            "protocol": ["Kyo Finance","Untitled Bank","SakeFinance","SoneX","QuickSwap","Velodrome"],
            "acs_peak_tvl_m": [55,40,28,42,15,20],
            "current_tvl_m": [0.99,0.25,1.32,0.086,1.79,0.50],
            "retention_pct": [1.8,0.6,4.7,0.2,11.9,2.5],
            "verdict": ["gone","gone","holds","gone","holds","weak"],
        })
    if f == "astr_bridge.csv":
        return pd.DataFrame({
            "season": ["S1","S2","S3","S4","S5","S6","S7","S8","S9"],
            "inflow_m": [133.7,128.0,0.08,0.11,0.10,0.02,0.02,0.09,0.05],
        })
    if f == "gas_per_tx.csv":
        return pd.DataFrame({
            "season": ["S1","S2","S3","S4","S5","S6","S7","S8","S9"],
            "gas_per_tx_k": [262,295,286,447,207,280,124,110,110],
        })
    if f == "asset_retention.csv":
        return pd.DataFrame({
            "asset": ["SolvBTC.BBN","ASTR","vASTR","USDC","wstASTR"],
            "pct_change": [-62,-23,2.7,0.9,19.8],
        })
    if f == "gaming_defi_retention.csv":
        return pd.DataFrame({
            "protocol": ["Yoki Legacy","Evermoon","SakeFinance","Kyo Finance","Untitled Bank"],
            "retention_pct": [13,6,4.7,1.8,0.6],
            "type": ["gaming","gaming","defi","defi","defi"],
        })
    if f == "l2_benchmark.csv":
        return pd.DataFrame({
            "chain": ["Soneium","Base","Blast","Linea"],
            "peak_tvl_m": [226,1800,2300,800],
            "tvl_90d_m": [9.5,630,414,176],
            "retention_pct": [4.2,35,18,22],
        })
    return pd.DataFrame()

def chart_style(fig, height=380):
    fig.update_layout(
        height=height,
        paper_bgcolor=CARD,
        plot_bgcolor=CARD,
        font=dict(family=FONT, color=WHITE, size=13),
        margin=dict(l=16, r=16, t=20, b=16),
        legend=dict(bgcolor="rgba(0,0,0,0)", font=dict(size=12, color=MUTED),
                    orientation="h", yanchor="bottom", y=1.02, xanchor="left", x=0),
        xaxis=dict(gridcolor=GRID, linecolor=BORDER, tickfont=dict(size=11, color=MUTED), showgrid=True),
        yaxis=dict(gridcolor=GRID, linecolor=BORDER, tickfont=dict(size=11, color=MUTED), showgrid=True),
    )
    return fig

# ── LOAD DATA ─────────────────────────────────────────────────────────────────
df_tvl     = load("tvl_trajectory.csv")
df_seasons = load("season_metrics.csv")
df_proto   = load("protocol_tvl.csv")
df_bridge  = load("astr_bridge.csv")
df_gas     = load("gas_per_tx.csv")
df_assets  = load("asset_retention.csv")
df_gaming  = load("gaming_defi_retention.csv")
df_l2      = load("l2_benchmark.csv")

# ── GLOBAL CSS ────────────────────────────────────────────────────────────────
st.markdown(f"""
<style>
@import url('https://fonts.googleapis.com/css2?family=Inter:wght@300;400;500;600;700;800&display=swap');
html, body, [class*="css"] {{ font-family:'Inter',sans-serif!important; background:{BG}!important; color:{WHITE}!important; }}
.stApp {{ background:{BG}!important; }}
.block-container {{ padding:0!important; max-width:100%!important; }}
header[data-testid="stHeader"] {{ background:transparent!important; }}
footer {{ display:none!important; }}
#MainMenu {{ visibility:hidden!important; }}
.stTabs [data-baseweb="tab-list"] {{ background:{SURFACE}; border-bottom:2px solid {BORDER}; padding:0 40px; gap:0; }}
.stTabs [data-baseweb="tab"] {{ background:transparent!important; color:{MUTED}!important; border:none!important; border-bottom:3px solid transparent!important; padding:18px 24px!important; font-size:13px!important; font-weight:600!important; letter-spacing:0.03em!important; text-transform:uppercase!important; }}
.stTabs [aria-selected="true"] {{ color:{WHITE}!important; border-bottom:3px solid {BLUE}!important; background:transparent!important; }}
.stTabs [data-baseweb="tab-panel"] {{ padding:0!important; background:{BG}!important; }}
.stPlotlyChart {{ border-radius:10px; overflow:hidden; }}
.kpi-label {{ font-size:11px; font-weight:700; text-transform:uppercase; letter-spacing:0.1em; color:{MUTED}; margin-bottom:10px; }}
.kpi-number {{ font-size:40px; font-weight:800; line-height:1; font-variant-numeric:tabular-nums; margin-bottom:8px; }}
.kpi-sub {{ font-size:13px; color:{MUTED}; line-height:1.5; }}
.card {{ background:{CARD}; border:1px solid {BORDER}; border-radius:12px; padding:28px; height:100%; }}
.card-sm {{ background:{CARD}; border:1px solid {BORDER}; border-radius:10px; padding:20px 24px; }}
.eyebrow {{ font-size:11px; font-weight:700; text-transform:uppercase; letter-spacing:0.12em; color:{BLUE}; margin-bottom:6px; }}
.heading {{ font-size:26px; font-weight:700; color:{WHITE}; line-height:1.3; margin-bottom:8px; }}
.body-text {{ font-size:15px; color:{MUTED}; line-height:1.7; max-width:720px; margin-bottom:32px; }}
.insight-box {{ background:rgba(0,229,204,0.05); border:1px solid rgba(0,229,204,0.2); border-radius:10px; padding:20px 22px; margin-bottom:14px; }}
.insight-label {{ font-size:10px; font-weight:700; text-transform:uppercase; letter-spacing:0.1em; color:{CYAN}; margin-bottom:8px; }}
.caption {{ font-size:13px; color:{MUTED}; line-height:1.6; margin-top:12px; padding:14px 18px; background:rgba(255,255,255,0.02); border-left:3px solid {BORDER}; border-radius:0 6px 6px 0; }}
.rec-card {{ background:{CARD}; border:1px solid {BORDER}; border-top:3px solid {BLUE}; border-radius:0 0 12px 12px; padding:24px; height:100%; }}
.rec-num {{ font-size:11px; font-weight:700; text-transform:uppercase; letter-spacing:0.1em; color:{BLUE}; margin-bottom:8px; }}
.rec-title {{ font-size:16px; font-weight:700; color:{WHITE}; margin-bottom:12px; line-height:1.4; }}
.rec-body {{ font-size:13px; color:{MUTED}; line-height:1.7; margin-bottom:16px; }}
.rec-metric {{ font-size:12px; color:{CYAN}; font-weight:600; border-top:1px solid {BORDER}; padding-top:12px; }}
.page {{ padding:36px 48px; }}
.divider {{ border:none; border-top:1px solid {BORDER}; margin:32px 0; }}
.col-title {{ font-size:13px; font-weight:700; color:{WHITE}; margin-bottom:16px; text-transform:uppercase; letter-spacing:0.08em; }}
</style>
""", unsafe_allow_html=True)

# ── HEADER ────────────────────────────────────────────────────────────────────
st.markdown(f"""
<div style="background:{SURFACE};border-bottom:1px solid {BORDER};padding:24px 48px;">
  <div style="display:flex;justify-content:space-between;align-items:center;flex-wrap:wrap;gap:16px;">
    <div>
      <div style="font-size:11px;font-weight:700;text-transform:uppercase;letter-spacing:0.12em;color:{BLUE};margin-bottom:6px;">Astar Network · Post-Mortem Analysis</div>
      <div style="font-size:24px;font-weight:800;color:{WHITE};margin-bottom:4px;">ACS Campaign Performance Report</div>
      <div style="font-size:13px;color:{MUTED};">Feb 20 – May 30, 2025 &nbsp;·&nbsp; Soneium Ecosystem &nbsp;·&nbsp; Analysis as of April 2026</div>
    </div>
    <div style="display:flex;gap:8px;flex-wrap:wrap;">
      <span style="background:rgba(16,185,129,0.12);color:{GREEN};border:1px solid rgba(16,185,129,0.25);font-size:11px;font-weight:700;padding:5px 12px;border-radius:5px;letter-spacing:0.06em;">PRE-ACS</span>
      <span style="background:rgba(0,180,255,0.12);color:{BLUE};border:1px solid rgba(0,180,255,0.25);font-size:11px;font-weight:700;padding:5px 12px;border-radius:5px;letter-spacing:0.06em;">ACS ACTIVE</span>
      <span style="background:rgba(245,158,11,0.12);color:{AMBER};border:1px solid rgba(245,158,11,0.25);font-size:11px;font-weight:700;padding:5px 12px;border-radius:5px;letter-spacing:0.06em;">POST-ACS</span>
      <span style="background:rgba(239,68,68,0.12);color:{RED};border:1px solid rgba(239,68,68,0.25);font-size:11px;font-weight:700;padding:5px 12px;border-radius:5px;letter-spacing:0.06em;">CURRENT</span>
    </div>
  </div>
</div>
""", unsafe_allow_html=True)

# ── TABS ──────────────────────────────────────────────────────────────────────
tabs = st.tabs([
    "📋  Executive Summary",
    "📈  TVL & Activity",
    "🏦  Protocol Autopsy",
    "🔗  ASTR Token",
    "🎮  Gaming vs DeFi",
    "🌐  L2 Benchmark",
    "💡  Insights & Recs",
])

# ─────────────────────────────────────────────────────────────────────────────
# TAB 1 — EXECUTIVE SUMMARY
# ─────────────────────────────────────────────────────────────────────────────
with tabs[0]:
    st.markdown("<div class='page'>", unsafe_allow_html=True)

    st.markdown(f"""
    <div class="eyebrow">The Core Finding</div>
    <div class="heading">Astar spent $20M+ to rent an audience.<br>The audience left on June 10, 2025.</div>
    <div class="body-text">The ACS campaign delivered impressive headline numbers — $226M TVL, 3.57M wallets, 147M transactions. But 95.8% of that TVL vanished within 90 days of the reward claim date. This report quantifies what stuck, what left, and what Astar should do differently next time.</div>
    """, unsafe_allow_html=True)

    k1, k2, k3, k4 = st.columns(4)
    for col, label, val, sub, color in [
        (k1, "Peak TVL Reached", "$226M", "Season 9 · May 2025", WHITE),
        (k2, "TVL Today", "$9.5M", "↓ 95.8% collapse in 90 days", RED),
        (k3, "Wallets Retained", "~3–5%", "Of 3.57M unique campaign wallets", AMBER),
        (k4, "Daily Tx Drop", "–87%", "Post-ACS vs. campaign average", RED),
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
        (k5, "ASTR Bridged In", "674.9M", "–23% within 30 days of claim"),
        (k6, "ASTR Distributed", "80.3M", "Of 100M budget · 19.7M unspent"),
        (k7, "ASTR vs All-Time High", "–65%", "$0.0084 · $71.9M market cap"),
        (k8, "Pre-ACS Baseline TVL", "$60M", "ACS added +267% at its peak"),
    ]:
        with col:
            st.markdown(f"""<div class="card-sm">
              <div class="kpi-label">{label}</div>
              <div style="font-size:26px;font-weight:700;color:{WHITE};margin-bottom:6px;">{val}</div>
              <div class="kpi-sub">{sub}</div>
            </div>""", unsafe_allow_html=True)

    st.markdown("<hr class='divider'>", unsafe_allow_html=True)
    st.markdown(f"<div class='eyebrow'>Three Verdicts</div><div class='heading' style='font-size:20px;margin-bottom:24px;'>What the data tells us</div>", unsafe_allow_html=True)

    v1, v2, v3 = st.columns(3)
    for col, color, icon, title, body in [
        (v1, RED, "❌", "ACS did NOT establish ASTR utility",
         "ASTR usage collapsed post-rewards. Bridge outflows of 23% within 30 days of the claim date confirm wallets treated ASTR purely as a reward vehicle, not a utility asset."),
        (v2, AMBER, "⚠️", "Gaming showed promise — DeFi did not",
         "Yoki Legacy retained 13% of users — 7× Kyo Finance's 1.8%. Gaming mechanics create habit; DeFi farming creates mercenaries. The next campaign should weight gaming 3× over DeFi."),
        (v3, BLUE, "→", "The real opportunity is the organic floor",
         "19 wallets were actively using Kyo Finance in April 2026 with no incentives. Understanding who they are and why they stayed is worth more than any campaign headline."),
    ]:
        with col:
            st.markdown(f"""<div class="card" style="border-top:3px solid {color};">
              <div style="font-size:28px;margin-bottom:12px;">{icon}</div>
              <div style="font-size:16px;font-weight:700;color:{WHITE};margin-bottom:12px;line-height:1.4;">{title}</div>
              <div style="font-size:13px;color:{MUTED};line-height:1.7;">{body}</div>
            </div>""", unsafe_allow_html=True)

    st.markdown("</div>", unsafe_allow_html=True)

# ─────────────────────────────────────────────────────────────────────────────
# TAB 2 — TVL & ACTIVITY
# ─────────────────────────────────────────────────────────────────────────────
with tabs[1]:
    st.markdown("<div class='page'>", unsafe_allow_html=True)
    st.markdown(f"""<div class="eyebrow">TVL & Transaction Activity</div>
    <div class="heading">The campaign created a mountain, not a foundation.</div>
    <div class="body-text">TVL grew 267% during ACS. It collapsed 96% after. The charts below show exactly when activity became artificial — and what the organic baseline actually looks like.</div>""", unsafe_allow_html=True)

    fig_tvl = go.Figure()
    acs_mask = df_tvl["acs_active"] == 1
    fig_tvl.add_trace(go.Scatter(
        x=df_tvl.loc[acs_mask,"period"].tolist(),
        y=df_tvl.loc[acs_mask,"tvl_usd_m"].tolist(),
        fill="tozeroy", fillcolor="rgba(0,180,255,0.07)",
        line=dict(color="rgba(0,180,255,0.25)", width=1, dash="dot"),
        name="ACS active period", hoverinfo="skip",
    ))
    fig_tvl.add_trace(go.Scatter(
        x=df_tvl["period"].tolist(), y=df_tvl["tvl_usd_m"].tolist(),
        fill="tozeroy", fillcolor="rgba(232,25,139,0.07)",
        line=dict(color=PINK, width=3), name="Total TVL",
        hovertemplate="<b>%{x}</b><br>TVL: $%{y:.0f}M<extra></extra>", mode="lines",
    ))
    fig_tvl.add_annotation(x="S9", y=220, text="<b>Peak $226M</b>", showarrow=True,
        arrowhead=2, arrowcolor=PINK, font=dict(color=PINK, size=13), ax=40, ay=-36)
    fig_tvl.add_annotation(x="Apr'26", y=9.5, text="<b>$9.5M today</b>", showarrow=False,
        font=dict(color=RED, size=13), xanchor="right", yshift=16)
    chart_style(fig_tvl, height=420)
    fig_tvl.update_xaxes(tickangle=-35, tickfont=dict(size=11))
    fig_tvl.update_yaxes(tickprefix="$", ticksuffix="M")
    st.plotly_chart(fig_tvl, use_container_width=True, config={"displayModeBar": False})
    st.markdown(f"""<div class="caption"><b>What happened:</b> TVL grew from $60M (pre-ACS) to $226M peak — driven primarily by SolvBTC.BBN deposits.
    When rewards ended May 30, SolvBTC.BBN exited –62% within 30 days of the June 10 claim date,
    accounting for the majority of the $216M collapse. The organic floor was always ~$9–12M.</div>""", unsafe_allow_html=True)

    st.markdown("<div style='height:32px'></div>", unsafe_allow_html=True)
    col_l, col_r = st.columns([1.1, 1])

    with col_l:
        st.markdown("<div class='col-title'>Season-by-Season Breakdown</div>", unsafe_allow_html=True)
        rows = ""
        for _, row in df_seasons.iterrows():
            s = str(row["season"])
            tvs = f"${row['tvs_usd_m']:.0f}M"
            dtx = f"{row['daily_tx_k']:.0f}K" if pd.notna(row.get("daily_tx_k")) else "—"
            nw = f"{row['new_wallets_k']:.0f}K" if pd.notna(row.get("new_wallets_k")) else "—"
            is_post = s == "Post-ACS"
            sc = RED if is_post else BLUE
            rows += f"""<tr style="border-bottom:1px solid {BORDER};{'background:rgba(239,68,68,0.04);' if is_post else ''}">
              <td style="padding:13px 16px;font-size:13px;font-weight:700;color:{sc};">{s}</td>
              <td style="padding:13px 16px;font-size:15px;font-weight:700;color:{WHITE};">{tvs}</td>
              <td style="padding:13px 16px;font-size:13px;color:{MUTED};">{dtx}</td>
              <td style="padding:13px 16px;font-size:13px;color:{MUTED};">{nw}</td>
            </tr>"""
        st.markdown(f"""<div style="background:{CARD};border:1px solid {BORDER};border-radius:12px;overflow:hidden;">
          <table style="width:100%;border-collapse:collapse;">
            <thead><tr style="background:{SURFACE};border-bottom:2px solid {BORDER};">
              <th style="padding:13px 16px;font-size:11px;color:{MUTED};text-align:left;font-weight:700;text-transform:uppercase;letter-spacing:0.08em;">Season</th>
              <th style="padding:13px 16px;font-size:11px;color:{MUTED};text-align:left;font-weight:700;text-transform:uppercase;letter-spacing:0.08em;">TVS</th>
              <th style="padding:13px 16px;font-size:11px;color:{MUTED};text-align:left;font-weight:700;text-transform:uppercase;letter-spacing:0.08em;">Daily Txns</th>
              <th style="padding:13px 16px;font-size:11px;color:{MUTED};text-align:left;font-weight:700;text-transform:uppercase;letter-spacing:0.08em;">New Wallets</th>
            </tr></thead><tbody>{rows}</tbody>
          </table></div>""", unsafe_allow_html=True)

    with col_r:
        st.markdown("<div class='col-title'>Gas Per Transaction — Economic Depth Signal</div>", unsafe_allow_html=True)
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
            showarrow=True, arrowhead=2, arrowcolor=RED, font=dict(color=RED, size=12), ax=44, ay=-28)
        fig_gas.add_annotation(x="S5", y=207, text="↓ Hollow farming begins",
            showarrow=False, font=dict(color=MUTED, size=11), yshift=16)
        chart_style(fig_gas, height=340)
        fig_gas.update_yaxes(ticksuffix="K gas", range=[0, 540])
        st.plotly_chart(fig_gas, use_container_width=True, config={"displayModeBar": False})
        st.markdown(f"""<div class="caption"><b>Key insight:</b> Gas/tx dropped 2.2× in Season 5 (447K → 207K). This is the exact moment activity shifted from genuine DeFi to low-complexity farming loops. Astar never published this signal.</div>""", unsafe_allow_html=True)

    st.markdown("</div>", unsafe_allow_html=True)

# ─────────────────────────────────────────────────────────────────────────────
# TAB 3 — PROTOCOL AUTOPSY
# ─────────────────────────────────────────────────────────────────────────────
with tabs[2]:
    st.markdown("<div class='page'>", unsafe_allow_html=True)
    st.markdown(f"""<div class="eyebrow">Protocol Autopsy</div>
    <div class="heading">Which protocols built something real?</div>
    <div class="body-text">Six protocols received significant ACS allocation. Below is what each looked like at peak vs. today — and an honest verdict on whether ACS helped them build a lasting user base or just rented temporary attention.</div>""", unsafe_allow_html=True)

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
    st.markdown(f"""<div class="caption"><b>The collapse:</b> Kyo Finance $55M → $987K (–98.2%). Untitled Bank $40M → $248K (–99.4%). SoneX $42M → $86K (–99.8%). QuickSwap and SakeFinance show the only meaningful retention — but both are multi-chain protocols whose TVL reflects their broader ecosystem, not Soneium-native demand.</div>""", unsafe_allow_html=True)

    st.markdown("<div style='height:32px'></div>", unsafe_allow_html=True)
    c_bar, c_cards = st.columns([1, 1.2])

    with c_bar:
        st.markdown("<div class='col-title'>90-Day Post-ACS TVL Retention Rate</div>", unsafe_allow_html=True)
        df_ret = df_proto.sort_values("retention_pct", ascending=True)
        bar_colors = [{"gone":RED,"weak":AMBER,"holds":GREEN}.get(v, MUTED) for v in df_ret["verdict"]]
        fig_ret = go.Figure(go.Bar(
            x=df_ret["retention_pct"], y=df_ret["protocol"], orientation="h",
            marker=dict(color=bar_colors, line=dict(width=0)),
            text=[f"  {v:.1f}%" for v in df_ret["retention_pct"]],
            textposition="outside", textfont=dict(size=13, color=WHITE),
            hovertemplate="<b>%{y}</b><br>Retention: %{x:.1f}%<extra></extra>", width=0.6,
        ))
        chart_style(fig_ret, height=360)
        fig_ret.update_xaxes(ticksuffix="%", range=[0, 16])
        fig_ret.update_yaxes(tickfont=dict(size=13))
        fig_ret.update_layout(margin=dict(l=8, r=60, t=20, b=16))
        st.plotly_chart(fig_ret, use_container_width=True, config={"displayModeBar": False})

    with c_cards:
        st.markdown("<div class='col-title'>Protocol Verdicts</div>", unsafe_allow_html=True)
        for name, verdict, change, desc in [
            ("Kyo Finance","gone","–98.2%","DEX with $55M ACS peak. Only 19 active wallets in April 2026. ACS bought temporary liquidity, not users."),
            ("Untitled Bank","gone","–99.4%","Lending platform with 1,377% TVL growth during ACS. Growth was entirely incentive-driven — no organic borrowing demand emerged post-rewards."),
            ("SakeFinance","holds","–95.3%","Best DeFi retention at 4.7%. Existing LP base from other chains provided a non-zero organic floor."),
            ("QuickSwap","holds","–88.1%","11.9% retention is misleading — reflects global QuickSwap liquidity, not Soneium-native demand."),
            ("Velodrome","weak","–97.5%","Protocol-owned liquidity showed some resilience but couldn't survive removal of ASTR yield incentives."),
            ("SoneX","gone","–99.8%","Effectively zero TVL remaining. Worst retention of all ACS participants."),
        ]:
            vc = RED if verdict == "gone" else (GREEN if verdict == "holds" else AMBER)
            cc = RED if "–" in change else GREEN
            st.markdown(f"""<div style="background:{CARD};border:1px solid {BORDER};border-radius:10px;padding:14px 18px;margin-bottom:10px;display:flex;align-items:flex-start;gap:14px;">
              <div style="min-width:110px;">
                <div style="font-size:13px;font-weight:700;color:{WHITE};margin-bottom:6px;">{name}</div>
                <div style="display:flex;gap:6px;align-items:center;flex-wrap:wrap;">
                  <span style="background:rgba(0,0,0,0.3);color:{vc};border:1px solid {vc}44;font-size:11px;font-weight:700;padding:2px 8px;border-radius:4px;">{verdict.upper()}</span>
                  <span style="font-size:12px;font-weight:700;color:{cc};">{change}</span>
                </div>
              </div>
              <div style="font-size:12px;color:{MUTED};line-height:1.6;border-left:1px solid {BORDER};padding-left:14px;">{desc}</div>
            </div>""", unsafe_allow_html=True)

    st.markdown("</div>", unsafe_allow_html=True)

# ─────────────────────────────────────────────────────────────────────────────
# TAB 4 — ASTR TOKEN
# ─────────────────────────────────────────────────────────────────────────────
with tabs[3]:
    st.markdown("<div class='page'>", unsafe_allow_html=True)
    st.markdown(f"""<div class="eyebrow">ASTR Token Analysis</div>
    <div class="heading">Did ASTR earn its place on Soneium?</div>
    <div class="body-text">Astar's core goal was to make ASTR the economic engine of Soneium — used as collateral, gas, and governance. The bridge flow and asset retention data shows whether that goal was achieved.</div>""", unsafe_allow_html=True)

    c_br, c_as = st.columns(2)
    with c_br:
        st.markdown("<div class='col-title'>ASTR Bridge Inflow by Season</div>", unsafe_allow_html=True)
        bc = [RED if v > 50 else (AMBER if v > 1 else BLUE) for v in df_bridge["inflow_m"]]
        fig_br = go.Figure(go.Bar(x=df_bridge["season"], y=df_bridge["inflow_m"],
            marker=dict(color=bc, line=dict(width=0)),
            hovertemplate="<b>%{x}</b><br>Inflow: %{y:.2f}M ASTR<extra></extra>", width=0.6))
        fig_br.add_hline(y=10, line_dash="dot", line_color="rgba(232,25,139,0.5)", line_width=1.5,
            annotation_text="avg reward rate", annotation_font=dict(size=11, color=PINK), annotation_position="right")
        chart_style(fig_br, height=360)
        fig_br.update_yaxes(ticksuffix="M ASTR")
        fig_br.update_xaxes(tickfont=dict(size=13))
        st.plotly_chart(fig_br, use_container_width=True, config={"displayModeBar": False})
        st.markdown(f"""<div class="caption"><b>Bridge saturation:</b> 99% of all ASTR bridged happened in the first two seasons (S1: 133.7M, S2: 128.0M). The remaining 7 seasons combined added only 0.47M ASTR — yet rewards continued at full rate for all 9 seasons.</div>""", unsafe_allow_html=True)

    with c_as:
        st.markdown("<div class='col-title'>Asset Retention — 30 Days After Claim Date (Jun 10 → Jul 10)</div>", unsafe_allow_html=True)
        df_a = df_assets.sort_values("pct_change")
        a_colors = [RED if v < -30 else (PINK if v < 0 else GREEN) for v in df_a["pct_change"]]
        fig_a = go.Figure(go.Bar(
            x=df_a["pct_change"], y=df_a["asset"], orientation="h",
            marker=dict(color=a_colors, line=dict(width=0)),
            text=[f"{v:+.1f}%" for v in df_a["pct_change"]],
            textposition="outside", textfont=dict(size=13, color=WHITE),
            hovertemplate="<b>%{y}</b><br>Change: %{x:+.1f}%<extra></extra>", width=0.55,
        ))
        chart_style(fig_a, height=360)
        fig_a.update_xaxes(ticksuffix="%", range=[-85, 40])
        fig_a.update_yaxes(tickfont=dict(size=13))
        fig_a.update_layout(margin=dict(l=8, r=60, t=20, b=16))
        st.plotly_chart(fig_a, use_container_width=True, config={"displayModeBar": False})
        st.markdown(f"""<div class="caption"><b>What stayed:</b> SolvBTC.BBN (–62%) drove the collapse — purely yield-seeking capital. USDC (+0.9%) and liquid staking (wstASTR +19.8%, vASTR +2.7%) were the stickiest assets. Staking derivatives are the only genuine ASTR utility signal in this dataset.</div>""", unsafe_allow_html=True)

    st.markdown("<div style='height:28px'></div>", unsafe_allow_html=True)
    st.markdown(f"<div class='col-title'>The ASTR Utility Verdict</div>", unsafe_allow_html=True)
    fa1, fa2, fa3 = st.columns(3)
    for col, color, title, body in [
        (fa1, RED, "ASTR as Collateral — Failed", "Kyo and Untitled Bank saw ASTR collateral collapse post-ACS. Users borrowed against ASTR to farm yield, not for genuine DeFi. No sustainable borrowing demand materialized."),
        (fa2, AMBER, "ASTR as Gas — Partial", "Gas payments in ASTR continued post-ACS but at –87% volume. Gas revenue to the network essentially disappeared with the farmers."),
        (fa3, GREEN, "ASTR Liquid Staking — Bright Spot", "wstASTR (+19.8%) and vASTR (+2.7%) are the only assets that grew after the claim date. This is genuine product-market fit. Astar should build the next campaign around expanding this cohort."),
    ]:
        with col:
            st.markdown(f"""<div class="card" style="border-left:3px solid {color};">
              <div style="font-size:15px;font-weight:700;color:{WHITE};margin-bottom:12px;">{title}</div>
              <div style="font-size:13px;color:{MUTED};line-height:1.7;">{body}</div>
            </div>""", unsafe_allow_html=True)

    st.markdown("</div>", unsafe_allow_html=True)

# ─────────────────────────────────────────────────────────────────────────────
# TAB 5 — GAMING VS DEFI
# ─────────────────────────────────────────────────────────────────────────────
with tabs[4]:
    st.markdown("<div class='page'>", unsafe_allow_html=True)
    st.markdown(f"""<div class="eyebrow">Gaming vs DeFi Retention</div>
    <div class="heading">Gaming keeps users. DeFi rents them.</div>
    <div class="body-text">Astar's pitch to Sony was "we bring gamers onchain." The retention data supports this — but only partially. Gaming protocols outperform DeFi on retention, but even the best gaming protocol falls well below what successful gaming chains achieve.</div>""", unsafe_allow_html=True)

    cg1, cg2 = st.columns([1, 1.1])
    with cg1:
        st.markdown("<div class='col-title'>Retention Rate by Protocol Type</div>", unsafe_allow_html=True)
        df_gd = df_gaming.sort_values("retention_pct", ascending=True)
        gd_colors = [PURPLE if t == "gaming" else BLUE for t in df_gd["type"]]
        fig_gd = go.Figure()
        fig_gd.add_trace(go.Bar(
            x=df_gd["retention_pct"], y=df_gd["protocol"], orientation="h",
            marker=dict(color=gd_colors, line=dict(width=0)),
            text=[f"  {v:.1f}%" for v in df_gd["retention_pct"]],
            textposition="outside", textfont=dict(size=14, color=WHITE),
            hovertemplate="<b>%{y}</b><br>Retention: %{x:.1f}%<extra></extra>", width=0.6,
        ))
        fig_gd.add_trace(go.Bar(x=[None], y=[None], marker_color=PURPLE, name="Gaming", showlegend=True))
        fig_gd.add_trace(go.Bar(x=[None], y=[None], marker_color=BLUE, name="DeFi", showlegend=True))
        chart_style(fig_gd, height=380)
        fig_gd.update_xaxes(ticksuffix="%", range=[0, 18])
        fig_gd.update_yaxes(tickfont=dict(size=13))
        fig_gd.update_layout(margin=dict(l=8, r=70, t=40, b=16))
        st.plotly_chart(fig_gd, use_container_width=True, config={"displayModeBar": False})

    with cg2:
        st.markdown("<div class='col-title'>What Drives the Gap</div>", unsafe_allow_html=True)
        for color, title, body in [
            (PURPLE, "Yoki Legacy — 13% retention", "Completion-based mechanic (collect-a-set NFTs) creates a goal loop that keeps users returning independently of rewards. Once users start a collection, they have a non-financial reason to come back. This is genuine habit formation."),
            (PURPLE, "Evermoon — 6% retention", "Competitive MOBA format. Higher engagement ceiling but less habit-forming than collection mechanics. Users who stopped winning tournaments had no secondary reason to return after rewards ended."),
            (BLUE, "DeFi average — 1.5% retention", "Pure yield optimization. When the yield moves, the user moves. No DeFi protocol on Soneium had product differentiation strong enough to retain users at sub-market rates."),
            (CYAN, "The key strategic insight", "Game mechanics that create non-financial goals (completing a collection, ranking, owning a rare item) retain users at 2–8× the rate of financial-only mechanics. Require gaming protocols to demonstrate a non-financial retention hook before receiving ACS 2.0 allocation."),
        ]:
            st.markdown(f"""<div style="background:{CARD};border:1px solid {BORDER};border-left:3px solid {color};border-radius:0 10px 10px 0;padding:16px 18px;margin-bottom:12px;">
              <div style="font-size:13px;font-weight:700;color:{WHITE};margin-bottom:8px;">{title}</div>
              <div style="font-size:13px;color:{MUTED};line-height:1.6;">{body}</div>
            </div>""", unsafe_allow_html=True)

    st.markdown("</div>", unsafe_allow_html=True)

# ─────────────────────────────────────────────────────────────────────────────
# TAB 6 — L2 BENCHMARK
# ─────────────────────────────────────────────────────────────────────────────
with tabs[5]:
    st.markdown("<div class='page'>", unsafe_allow_html=True)
    st.markdown(f"""<div class="eyebrow">L2 Competitive Benchmark</div>
    <div class="heading">Soneium's retention is 4× below the L2 average.</div>
    <div class="body-text">Incentive campaigns are common across L2s. But Soneium's 4.2% post-incentive TVL retention is significantly below Base (35%), Linea (22%), and Blast (18%). Here's why — and what those chains did differently.</div>""", unsafe_allow_html=True)

    chain_colors = {"Soneium": RED, "Base": GREEN, "Blast": AMBER, "Linea": BLUE}
    bench_html = ""
    for _, row in df_l2.iterrows():
        chain = row["chain"]
        c = chain_colors.get(chain, MUTED)
        peak_bar = min(row["peak_tvl_m"] / 23, 100)
        ret_bar = min(row["tvl_90d_m"] / 23, 100)
        bench_html += f"""
        <div style="background:{CARD};border:1px solid {BORDER};border-left:4px solid {c};border-radius:0 12px 12px 0;padding:24px 28px;margin-bottom:16px;">
          <div style="display:flex;justify-content:space-between;align-items:center;margin-bottom:20px;">
            <div style="font-size:20px;font-weight:800;color:{WHITE};">{chain}</div>
            <div style="text-align:right;">
              <div style="font-size:28px;font-weight:800;color:{c};">{row['retention_pct']:.0f}%</div>
              <div style="font-size:11px;color:{MUTED};font-weight:600;text-transform:uppercase;letter-spacing:0.08em;">90-day retention</div>
            </div>
          </div>
          <div style="display:flex;align-items:center;gap:12px;margin-bottom:10px;">
            <span style="font-size:11px;color:{MUTED};min-width:70px;font-weight:600;text-transform:uppercase;letter-spacing:0.06em;">Peak TVL</span>
            <div style="flex:1;height:6px;background:{BORDER};border-radius:3px;overflow:hidden;">
              <div style="width:{peak_bar}%;height:100%;background:{c};opacity:0.4;border-radius:3px;"></div>
            </div>
            <span style="font-size:13px;font-weight:700;color:{MUTED};min-width:64px;text-align:right;">${row['peak_tvl_m']:,.0f}M</span>
          </div>
          <div style="display:flex;align-items:center;gap:12px;">
            <span style="font-size:11px;color:{MUTED};min-width:70px;font-weight:600;text-transform:uppercase;letter-spacing:0.06em;">90-day TVL</span>
            <div style="flex:1;height:6px;background:{BORDER};border-radius:3px;overflow:hidden;">
              <div style="width:{ret_bar}%;height:100%;background:{c};border-radius:3px;"></div>
            </div>
            <span style="font-size:13px;font-weight:700;color:{c};min-width:64px;text-align:right;">${row['tvl_90d_m']:,.0f}M</span>
          </div>
        </div>"""
    st.markdown(bench_html, unsafe_allow_html=True)

    st.markdown("<div style='height:24px'></div>", unsafe_allow_html=True)
    st.markdown(f"<div class='col-title'>Why Other L2s Retained Better</div>", unsafe_allow_html=True)
    b1, b2, b3 = st.columns(3)
    for col, color, title, body in [
        (b1, GREEN, "Base — 35% Retention", "Coinbase's 100M+ user base gave Base structural distribution. Incentivized users were already Coinbase customers with existing crypto behavior — not first-time participants attracted purely by yield."),
        (b2, AMBER, "Blast — 18% Retention", "Blast's native yield model (ETH and stablecoin auto-yield) means the chain itself generates returns independent of protocol incentives — a baseline reason to keep assets even after campaigns end."),
        (b3, BLUE, "Linea — 22% Retention", "MetaMask integration (1B+ installs) provided organic user access. Campaign participants already had Web3 infrastructure — not mercenary capital attracted by temporary ASTR yields."),
    ]:
        with col:
            st.markdown(f"""<div class="card">
              <div style="font-size:15px;font-weight:700;color:{color};margin-bottom:12px;">{title}</div>
              <div style="font-size:13px;color:{MUTED};line-height:1.7;">{body}</div>
            </div>""", unsafe_allow_html=True)

    st.markdown(f"""<div style="margin-top:28px;padding:24px 28px;background:rgba(239,68,68,0.07);border:1px solid rgba(239,68,68,0.2);border-radius:12px;">
      <div style="font-size:15px;font-weight:700;color:{RED};margin-bottom:10px;">The structural disadvantage Astar needs to solve</div>
      <div style="font-size:14px;color:{MUTED};line-height:1.7;">Base, Blast, and Linea all had a structural retention mechanism that existed independently of their incentive campaigns. Astar's only retention mechanism was the ASTR reward itself. Until Astar has a structural retention driver — Sony IP, native yield, or an existing user distribution channel — any follow-on campaign will produce similar results.</div>
    </div>""", unsafe_allow_html=True)

    st.markdown("</div>", unsafe_allow_html=True)

# ─────────────────────────────────────────────────────────────────────────────
# TAB 7 — INSIGHTS & RECOMMENDATIONS
# ─────────────────────────────────────────────────────────────────────────────
with tabs[6]:
    st.markdown("<div class='page'>", unsafe_allow_html=True)
    st.markdown(f"""<div class="eyebrow">Insights & Recommendations</div>
    <div class="heading">What Astar doesn't know yet — and what to do about it.</div>
    <div class="body-text">Four findings not published by Astar. Three recommendations their growth team can act on immediately.</div>""", unsafe_allow_html=True)

    st.markdown(f"<div class='col-title'>New Insights — Not Published by Astar</div>", unsafe_allow_html=True)
    for num, title, body in [
        ("01", "The S5 Gas Signal — The Campaign Turned Hollow Before Astar Noticed",
         "Gas per transaction dropped from 447K to 207K gas in Season 5 — a 2.2× decline indicating activity shifted from genuine DeFi interactions to simple reward-loop farming. This signal predated Astar's own allocation adjustments by two seasons and was never publicly disclosed."),
        ("02", "Bridge Saturation Happened in 20 Days — Rewards Ran for 100",
         "133.7M ASTR bridged in S1, 128.0M in S2, and less than 0.5M combined across S3–S9. The bridge incentive was exhausted in the first 20% of the campaign. Yet the TVL-weighted formula continued distributing 70% of rewards at full rate based on locked-in capital for the remaining 80 days."),
        ("03", "Liquid Staking is the Only Genuine Utility Signal",
         "wstASTR (+19.8%) and vASTR (+2.7%) were the only assets that increased on Soneium in the 30 days following the reward claim date. These users engaged with ASTR liquid staking independently of ACS rewards and deepened their commitment. This cohort — however small — is Astar's actual product-market fit signal."),
        ("04", "Path of Soneium Received Gaming Rewards Without a Game",
         "The discretionary gaming allocation included Path of Soneium — a quest checklist app (bridge, deposit, complete tasks) with no game loop, no competitive mechanic, and no reason for return visits. It received 2M ASTR/season — equivalent to Evermoon — despite a fraction of the retention. The gaming allocation had no minimum engagement criteria."),
    ]:
        st.markdown(f"""<div class="insight-box">
          <div class="insight-label">Insight {num}</div>
          <div style="font-size:15px;font-weight:700;color:{WHITE};margin-bottom:8px;">{title}</div>
          <div style="font-size:13px;color:{MUTED};line-height:1.6;">{body}</div>
        </div>""", unsafe_allow_html=True)

    st.markdown("<div style='height:32px'></div>", unsafe_allow_html=True)
    st.markdown(f"<div class='col-title'>Three Recommendations for Astar's Growth Team</div>", unsafe_allow_html=True)

    r1, r2, r3 = st.columns(3)
    for col, num, timeline, title, body, metric in [
        (r1, "Recommendation 01", "Protocol + AFC · Q3 2026",
         "Replace TVL-weighted rewards with a 90-day vesting lock tied to retention thresholds",
         "SolvBTC.BBN exited –62% within 30 days — the majority of ACS peak TVL. A 90-day lock requiring ≥15% TVL retention as a prerequisite for full payout would have redirected ~$130M in phantom TVL incentives toward protocols with genuine organic floors. Formula change: 50% TVL weight → 30% TVL + 20% 30-day wallet return rate.",
         "≥15% TVL retention across top-5 protocols at 90 days post-campaign"),
        (r2, "Recommendation 02", "Growth team + Sentio · Q2–Q3 2026",
         "Redirect 30% of gaming allocation to a behavioral tier scored on return rate, not gas consumption",
         "Yoki Legacy's collection mechanic retained users at 2× Evermoon's rate with similar allocation. Path of Soneium received gaming rewards with zero game loop. A 3-metric behavioral dashboard (30-day return rate, sessions per retained wallet, non-financial in-app actions) built on Sentio would redirect incentives toward genuinely sticky products before the next campaign.",
         "Average 30-day return rate ≥10% across gaming tier recipients"),
        (r3, "Recommendation 03", "Business dev + Startale Labs · Q4 2026",
         "Secure one Sony IP integration before launching any follow-on incentive campaign",
         "Soneium's gaming retention (6–13%) sits below comparable gaming chains (15–40%) because no ACS protocol had Sony IP access. Sony controls PlayStation franchises, anime, and music. Startale Labs' $63M Series A provides negotiating leverage. Gate ACS 2.0 gaming allocation on at least one signed Sony IP product being live at launch — not in development.",
         "≥50K unique wallets within 60 days of Sony IP product launch on Soneium"),
    ]:
        with col:
            st.markdown(f"""<div class="rec-card">
              <div class="rec-num">{num}</div>
              <div style="font-size:11px;color:{MUTED};margin-bottom:14px;font-weight:500;">{timeline}</div>
              <div class="rec-title">{title}</div>
              <div class="rec-body">{body}</div>
              <div class="rec-metric">📊 Success metric: {metric}</div>
            </div>""", unsafe_allow_html=True)

    st.markdown(f"""<div style="margin-top:48px;padding-top:20px;border-top:1px solid {BORDER};font-size:12px;color:{MUTED};line-height:1.9;">
      <b style="color:{WHITE};">Data sources:</b> ACS Performance Reports (Astar Forum, 2025) &nbsp;·&nbsp; DeFiLlama (April 2026) &nbsp;·&nbsp; Blockscout Soneium Explorer &nbsp;·&nbsp; AFC Monthly Report (July 2025)<br>
      Estimated figures carry ±15% uncertainty. L2 benchmark retention figures are approximate from public analyst reports.
    </div>""", unsafe_allow_html=True)

    st.markdown("</div>", unsafe_allow_html=True)
