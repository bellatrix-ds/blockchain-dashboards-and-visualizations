

import streamlit as st
import pandas as pd
import plotly.graph_objects as go
import plotly.express as px
from plotly.subplots import make_subplots
import requests
from io import StringIO
import os

# ── PAGE CONFIG ──────────────────────────────────────────────────────────────
st.set_page_config(
    page_title="ACS Campaign Post-Mortem",
    page_icon="🔵",
    layout="wide",
    initial_sidebar_state="collapsed",
)

# ── BRAND PALETTE ─────────────────────────────────────────────────────────────
BG_DARK      = "#0d0d12"      # near-black background
BG_CARD      = "#13131e"      # card surface
BG_CARD2     = "#1a1a2a"      # secondary card
PINK         = "#e8198b"      # hot magenta / primary accent
BLUE         = "#00b4ff"      # electric blue / secondary accent
PURPLE       = "#7c3aed"      # mid-purple connector
CYAN         = "#00e5ff"      # highlight cyan
WHITE        = "#f0f0f8"
MUTED        = "#6b6b8a"
GREEN        = "#1db97a"
AMBER        = "#f59e0b"
RED          = "#e84545"
BORDER       = "#252540"

CHART_BG     = BG_DARK
GRID_COLOR   = "#1e1e30"
FONT_FAMILY  = "Inter, Arial, sans-serif"

# ── DATA SOURCE CONFIG ────────────────────────────────────────────────────────
# Priority order:
#   1. Local  → a "data/" folder sitting next to acs_dashboard.py
#   2. GitHub → set GITHUB_RAW_BASE to your repo's raw URL (optional)
#   3. Bundled sample data → always works as a last resort

GITHUB_RAW_BASE = "https://github.com/bellatrix-ds/blockchain-dashboards-and-visualizations/tree/main/05_Astar/data"   # e.g. "https://raw.githubusercontent.com/you/repo/main/data/"
                        # Leave empty ("") to skip GitHub and use local files only.

# Path to local data folder (relative to this script)
DATA_DIR = os.path.join(os.path.dirname(os.path.abspath(__file__)), "data")

# ── HELPERS ───────────────────────────────────────────────────────────────────

@st.cache_data(ttl=3600)
def load_csv(filename: str) -> pd.DataFrame:
    """
    Load a CSV with three fallback levels:
      1. Local  data/ folder next to this script
      2. GitHub raw URL (if GITHUB_RAW_BASE is set)
      3. Bundled sample data
    """
    # --- 1. Try local file first ---
    local_path = os.path.join(DATA_DIR, filename)
    if os.path.exists(local_path):
        return pd.read_csv(local_path)

    # --- 2. Try GitHub if URL is configured ---
    if GITHUB_RAW_BASE and "YOUR_USERNAME" not in GITHUB_RAW_BASE:
        url = GITHUB_RAW_BASE.rstrip("/") + "/" + filename
        try:
            r = requests.get(url, timeout=10)
            r.raise_for_status()
            return pd.read_csv(StringIO(r.text))
        except Exception:
            pass  # fall through to sample data

    # --- 3. Fall back to bundled sample data ---
    st.warning(
        f"**`{filename}` not found.** "
        f"Place your CSV files in a `data/` folder next to `acs_dashboard.py` and rerun. "
        f"Using sample data for now.",
        icon="⚠️",
    )
    return _sample_data(filename)


def _sample_data(filename: str) -> pd.DataFrame:
    """Bundled sample data matching the dashboard's acs_dashboard_data.csv schema."""

    if filename == "tvl_trajectory.csv":
        return pd.DataFrame({
            "period": [
                "Nov'24","Dec","Jan'25","Feb","S1","S2","S3","S4",
                "S5","S6","S7","S8","S9","Jun'25","Jul","Sep","Jan'26","Apr'26"
            ],
            "tvl_usd_m": [2,5,12,60,73,108,119,154,137,125,175,199,220,152,80,30,12,9.5],
            "acs_active": [0,0,0,0,1,1,1,1,1,1,1,1,1,0,0,0,0,0],
        })

    if filename == "season_metrics.csv":
        return pd.DataFrame({
            "season":       ["S1","S2","S3","S4","S5","S6","S7","S8","S9","Post-ACS"],
            "tvs_usd_m":    [73,108,119,154,137,125,175,199,220,10],
            "daily_tx_k":   [1600,1155,1564,1457,991,1042,1115,819,901,175],
            "new_wallets_k":[584,340,292,121,364,389,231,510,529,None],
        })

    if filename == "protocol_tvl.csv":
        return pd.DataFrame({
            "protocol":        ["Kyo Finance","Untitled Bank","SakeFinance","SoneX","QuickSwap","Velodrome"],
            "acs_peak_tvl_m":  [55, 40, 28, 42, 15, 20],
            "current_tvl_m":   [0.99, 0.25, 1.32, 0.086, 1.79, 0.50],
            "retention_pct":   [1.8, 0.6, 4.7, 0.2, 11.9, 2.5],
            "verdict":         ["gone","gone","holds","gone","holds","weak"],
        })

    if filename == "astr_bridge.csv":
        return pd.DataFrame({
            "season":       ["S1","S2","S3","S4","S5","S6","S7","S8","S9"],
            "inflow_m":     [133.7, 128.0, 0.08, 0.11, 0.10, 0.02, 0.02, 0.09, 0.05],
        })

    if filename == "gas_per_tx.csv":
        return pd.DataFrame({
            "season":      ["S1","S2","S3","S4","S5","S6","S7","S8","S9"],
            "gas_per_tx_k":[262, 295, 286, 447, 207, 280, 124, 110, 110],
        })

    if filename == "asset_retention.csv":
        return pd.DataFrame({
            "asset":      ["SolvBTC.BBN","ASTR","vASTR","USDC","wstASTR"],
            "pct_change": [-62, -23, 2.7, 0.9, 19.8],
        })

    if filename == "gaming_defi_retention.csv":
        return pd.DataFrame({
            "protocol":       ["Yoki Legacy","Evermoon","SakeFinance","Kyo Finance","Untitled Bank"],
            "retention_pct":  [13, 6, 4.7, 1.8, 0.6],
            "type":           ["gaming","gaming","defi","defi","defi"],
        })

    if filename == "l2_benchmark.csv":
        return pd.DataFrame({
            "chain":       ["Soneium","Base","Blast","Linea"],
            "peak_tvl_m":  [226, 1800, 2300, 800],
            "tvl_90d_m":   [9.5, 630, 414, 176],
            "retention_pct":[4.2, 35, 18, 22],
        })

    return pd.DataFrame()


def brand_chart_layout(fig: go.Figure, title: str = "", height: int = 280) -> go.Figure:
    """Apply ACS brand styling to any Plotly figure."""
    fig.update_layout(
        height=height,
        paper_bgcolor=BG_CARD,
        plot_bgcolor=BG_CARD,
        font=dict(family=FONT_FAMILY, color=WHITE, size=11),
        title=dict(
            text=title,
            font=dict(size=11, color=MUTED, family=FONT_FAMILY),
            x=0,
            xanchor="left",
            pad=dict(l=4, b=8),
        ),
        margin=dict(l=10, r=10, t=36 if title else 12, b=10),
        legend=dict(
            bgcolor="rgba(0,0,0,0)",
            font=dict(size=10, color=MUTED),
            orientation="h",
            yanchor="bottom",
            y=1.01,
            xanchor="left",
            x=0,
        ),
        xaxis=dict(
            gridcolor=GRID_COLOR,
            linecolor=BORDER,
            tickfont=dict(size=9, color=MUTED),
            showgrid=True,
        ),
        yaxis=dict(
            gridcolor=GRID_COLOR,
            linecolor=BORDER,
            tickfont=dict(size=9, color=MUTED),
            showgrid=True,
        ),
    )
    return fig


# ── GLOBAL CSS ────────────────────────────────────────────────────────────────
st.markdown(f"""
<style>
  @import url('https://fonts.googleapis.com/css2?family=Inter:wght@300;400;500;600;700&display=swap');

  html, body, [class*="css"] {{
    font-family: 'Inter', sans-serif;
    background-color: {BG_DARK};
    color: {WHITE};
  }}
  .stApp {{ background-color: {BG_DARK}; }}

  /* header */
  .acs-header {{
    background: linear-gradient(135deg, #0d0d1a 0%, #13132a 60%, #0d0d1a 100%);
    border-bottom: 1px solid {BORDER};
    padding: 20px 28px 16px;
    margin-bottom: 0;
  }}
  .acs-title {{
    font-size: 22px; font-weight: 700; letter-spacing: -.3px;
    background: linear-gradient(90deg, {WHITE} 0%, {BLUE} 100%);
    -webkit-background-clip: text; -webkit-text-fill-color: transparent;
    margin: 0; padding: 0;
  }}
  .acs-sub {{
    font-size: 12px; color: {MUTED}; margin-top: 4px;
  }}
  .period-tag {{
    display: inline-block; font-size: 9px; font-weight: 700;
    padding: 2px 8px; border-radius: 3px; margin-right: 5px;
    letter-spacing: .06em; text-transform: uppercase;
  }}

  /* KPI cards */
  .kpi-card {{
    background: {BG_CARD};
    border: 1px solid {BORDER};
    border-radius: 8px;
    padding: 16px 18px;
    height: 100%;
  }}
  .kpi-label {{
    font-size: 9px; font-weight: 600; text-transform: uppercase;
    letter-spacing: .09em; color: {MUTED}; margin-bottom: 6px;
  }}
  .kpi-value {{
    font-size: 28px; font-weight: 700; line-height: 1.1;
    font-variant-numeric: tabular-nums;
  }}
  .kpi-delta {{
    font-size: 11px; margin-top: 4px; font-weight: 500;
  }}
  .kpi-sub {{ font-size: 10px; color: {MUTED}; margin-top: 2px; }}

  .val-pink  {{ color: {PINK}; }}
  .val-blue  {{ color: {BLUE}; }}
  .val-white {{ color: {WHITE}; }}
  .val-green {{ color: {GREEN}; }}
  .val-red   {{ color: {RED}; }}
  .val-amber {{ color: {AMBER}; }}
  .val-muted {{ color: {MUTED}; }}

  /* section chart cards */
  .chart-card {{
    background: {BG_CARD};
    border: 1px solid {BORDER};
    border-radius: 8px;
    padding: 14px;
    margin-bottom: 14px;
  }}
  .chart-card-title {{
    font-size: 10px; font-weight: 600; text-transform: uppercase;
    letter-spacing: .09em; color: {MUTED}; margin-bottom: 10px;
  }}
  .chart-caption {{
    font-size: 10px; color: {MUTED}; margin-top: 6px; line-height: 1.55;
    font-style: italic;
  }}

  /* insight boxes */
  .insight-box {{
    background: {BG_CARD2};
    border-left: 3px solid {CYAN};
    border-radius: 0 6px 6px 0;
    padding: 11px 14px;
    margin-bottom: 10px;
  }}
  .insight-num {{
    font-size: 9px; font-weight: 700; text-transform: uppercase;
    letter-spacing: .08em; color: {CYAN}; margin-bottom: 4px;
  }}
  .insight-text {{
    font-size: 12px; color: {WHITE}; line-height: 1.6;
  }}

  /* rec boxes */
  .rec-box {{
    background: {BG_CARD};
    border: 1px solid {BORDER};
    border-radius: 8px;
    padding: 14px 16px;
    margin-bottom: 10px;
  }}
  .rec-badge {{
    display: inline-block; font-size: 9px; font-weight: 700;
    background: {BLUE}22; color: {BLUE};
    border: 1px solid {BLUE}44;
    padding: 2px 8px; border-radius: 3px;
    letter-spacing: .05em; margin-bottom: 7px;
  }}
  .rec-title {{
    font-size: 13px; font-weight: 600; color: {WHITE};
    margin-bottom: 6px; line-height: 1.3;
  }}
  .rec-body {{
    font-size: 11px; color: {MUTED}; line-height: 1.7;
  }}
  .rec-meta {{
    font-size: 10px; color: {MUTED}; margin-top: 10px;
    padding-top: 8px; border-top: 1px solid {BORDER};
  }}
  .rec-meta b {{ color: {WHITE}; font-weight: 500; }}

  /* verdict pills */
  .pill-holds {{ background: #1db97a22; color: {GREEN}; border: 1px solid {GREEN}44; font-size: 9px; font-weight: 700; padding: 1px 7px; border-radius: 3px; }}
  .pill-weak  {{ background: #f59e0b22; color: {AMBER};  border: 1px solid {AMBER}44; font-size: 9px; font-weight: 700; padding: 1px 7px; border-radius: 3px; }}
  .pill-gone  {{ background: #e8454522; color: {RED};    border: 1px solid {RED}44;   font-size: 9px; font-weight: 700; padding: 1px 7px; border-radius: 3px; }}
  .pill-gaming{{ background: #7c3aed22; color: #a78bfa;  border: 1px solid #7c3aed44; font-size: 9px; font-weight: 700; padding: 1px 7px; border-radius: 3px; }}
  .pill-defi  {{ background: #00b4ff22; color: {BLUE};   border: 1px solid {BLUE}44;  font-size: 9px; font-weight: 700; padding: 1px 7px; border-radius: 3px; }}

  /* divider */
  .acs-divider {{
    border: none; border-top: 1px solid {BORDER}; margin: 28px 0;
  }}

  /* section heading */
  .section-label {{
    font-size: 9px; font-weight: 700; text-transform: uppercase;
    letter-spacing: .12em; color: {MUTED}; margin-bottom: 4px;
  }}
  .section-title {{
    font-size: 18px; font-weight: 600; color: {WHITE};
    margin-bottom: 16px; line-height: 1.3;
  }}

  /* Streamlit overrides */
  .stPlotlyChart {{ border-radius: 8px; overflow: hidden; }}
  div[data-testid="metric-container"] {{ display: none; }}
  footer {{ display: none; }}
  #MainMenu {{ visibility: hidden; }}
  header[data-testid="stHeader"] {{ background: transparent; }}
  .block-container {{ padding: 0 !important; max-width: 100% !important; }}
</style>
""", unsafe_allow_html=True)


# ── LOAD DATA ─────────────────────────────────────────────────────────────────
df_tvl       = pd.read_csv("https://raw.githubusercontent.com/bellatrix-ds/blockchain-dashboards-and-visualizations/refs/heads/main/05_Astar/data/tvl_trajectory.csv")
df_seasons   = pd.read_csv("https://raw.githubusercontent.com/bellatrix-ds/blockchain-dashboards-and-visualizations/refs/heads/main/05_Astar/data/season_metrics.csv")
df_protocols = pd.read_csv("https://raw.githubusercontent.com/bellatrix-ds/blockchain-dashboards-and-visualizations/refs/heads/main/05_Astar/data/protocol_tvl.csv")
df_bridge    = pd.read_csv("https://raw.githubusercontent.com/bellatrix-ds/blockchain-dashboards-and-visualizations/refs/heads/main/05_Astar/data/astr_bridge.csv")
df_gas       = pd.read_csv("https://raw.githubusercontent.com/bellatrix-ds/blockchain-dashboards-and-visualizations/refs/heads/main/05_Astar/data/gas_per_tx.csv")
df_assets    = pd.read_csv("https://raw.githubusercontent.com/bellatrix-ds/blockchain-dashboards-and-visualizations/refs/heads/main/05_Astar/data/asset_retention.csv")
df_gaming    = pd.read_csv("https://raw.githubusercontent.com/bellatrix-ds/blockchain-dashboards-and-visualizations/refs/heads/main/05_Astar/data/gaming_defi_retention.csv")
df_l2        = pd.read_csv("https://raw.githubusercontent.com/bellatrix-ds/blockchain-dashboards-and-visualizations/refs/heads/main/05_Astar/data/l2_benchmark.csv")

# ══════════════════════════════════════════════════════════════════════════════
# HEADER
# ══════════════════════════════════════════════════════════════════════════════
st.markdown(f"""
<div class="acs-header">
  <div style="display:flex; align-items:flex-start; justify-content:space-between; flex-wrap:wrap; gap:12px;">
    <div>
      <div class="acs-title">ACS Campaign Post-Mortem &mdash; Soneium Ecosystem</div>
      <div class="acs-sub">Feb 20 &ndash; May 30 2025 campaign &nbsp;&middot;&nbsp; Analysis as of April 2026 &nbsp;&middot;&nbsp; 80.3M ASTR distributed</div>
    </div>
    <div style="display:flex; gap:6px; align-items:center; flex-wrap:wrap; padding-top:4px;">
      <span class="period-tag" style="background:#eaf3de22; color:#1db97a; border:1px solid #1db97a44;">pre_acs</span>
      <span class="period-tag" style="background:#00b4ff22; color:{BLUE};  border:1px solid {BLUE}44;">acs_active</span>
      <span class="period-tag" style="background:#f59e0b22; color:{AMBER}; border:1px solid {AMBER}44;">post_acs</span>
      <span class="period-tag" style="background:#e8454522; color:{RED};   border:1px solid {RED}44;">current</span>
    </div>
  </div>
</div>
""", unsafe_allow_html=True)

st.markdown("<div style='height:20px'></div>", unsafe_allow_html=True)

# ── Wrap content in padded container ─────────────────────────────────────────
with st.container():
    pad_l, main_col, pad_r = st.columns([0.03, 0.94, 0.03])
    with main_col:

        # ══════════════════════════════════════════════════════════════════
        # ROW 1 — KPI CARDS (8 cards, 4 per row)
        # ══════════════════════════════════════════════════════════════════
        c1, c2, c3, c4 = st.columns(4)
        kpi_cards = [
            (c1, "Peak TVL",          "$226M",  "Season 9 · May 2025",         "white",  ""),
            (c2, "Current TVL",       "$9.5M",  "–95.8% from peak",            "red",    "val-red"),
            (c3, "Unique wallets",    "3.57M",  "~3–5% retained post-ACS",     "white",  "val-red"),
            (c4, "Total transactions","147M",   "–87% daily vol post-ACS",     "white",  "val-red"),
        ]
        for col, label, val, delta, _val_cls, delta_cls in kpi_cards:
            with col:
                vc = f"val-{_val_cls}" if _val_cls != "white" else "val-white"
                st.markdown(f"""
                <div class="kpi-card">
                  <div class="kpi-label">{label}</div>
                  <div class="kpi-value {vc}">{val}</div>
                  <div class="kpi-delta {delta_cls if delta_cls else 'val-muted'}">{delta}</div>
                </div>""", unsafe_allow_html=True)

        st.markdown("<div style='height:10px'></div>", unsafe_allow_html=True)

        c5, c6, c7, c8 = st.columns(4)
        kpi_cards2 = [
            (c5, "ASTR bridged",       "674.9M", "–23% within 30d of claim",    "white",  "val-red"),
            (c6, "ASTR distributed",   "80.3M",  "of 100M budget · 19.7M unspent","white","val-muted"),
            (c7, "ASTR price vs ATH",  "–65%",   "$0.0084 · $71.9M mcap",       "red",    "val-muted"),
            (c8, "Pre-ACS TVL",        "$60M",   "+267% during campaign",        "white",  "val-green"),
        ]
        for col, label, val, delta, _val_cls, delta_cls in kpi_cards2:
            with col:
                vc = f"val-{_val_cls}" if _val_cls != "white" else "val-white"
                st.markdown(f"""
                <div class="kpi-card">
                  <div class="kpi-label">{label}</div>
                  <div class="kpi-value {vc}">{val}</div>
                  <div class="kpi-delta {delta_cls}">{delta}</div>
                </div>""", unsafe_allow_html=True)

        st.markdown("<hr class='acs-divider'>", unsafe_allow_html=True)

        # ══════════════════════════════════════════════════════════════════
        # ROW 2 — TVL Trajectory  |  Season Table
        # ══════════════════════════════════════════════════════════════════
        col_tvl, col_table = st.columns([1.6, 1])

        with col_tvl:
            st.markdown("<div class='chart-card-title'>TVL TRAJECTORY — SONEIUM (NOV 2024 → APR 2026)</div>", unsafe_allow_html=True)

            fig_tvl = go.Figure()
            acs_mask = df_tvl["acs_active"] == 1
            x_all = df_tvl["period"].tolist()
            y_all = df_tvl["tvl_usd_m"].tolist()
            # ACS shaded region
                x_acs = df_tvl.loc[acs_mask, "period"].tolist()
                y_acs = df_tvl.loc[acs_mask, "tvl_usd_m"].tolist()
                fig_tvl.add_trace(go.Scatter(
                    x=x_acs, y=y_acs, fill="tozeroy",
                    fillcolor="rgba(0, 180, 255, 0.09)",
                    line=dict(color="rgba(0, 180, 255, 0.33)", width=1, dash="dot"),
                    name="ACS period", hoverinfo="skip",
                ))
                # Main TVL line
                fig_tvl.add_trace(go.Scatter(
                    x=x_all, y=y_all, fill="tozeroy",
                    fillcolor="rgba(232, 25, 139, 0.08)",
                    line=dict(color=PINK, width=2.5),
                    name="Total TVL ($M)",
                    hovertemplate="<b>%{x}</b><br>TVL: $%{y:.0f}M<extra></extra>",
                    mode="lines",
                ))
                # Annotation
                fig_tvl.add_annotation(
                    x="S9", y=220, text="Peak $226M", showarrow=True,
                    arrowhead=2, arrowcolor=PINK, font=dict(color=PINK, size=10),
                    ax=30, ay=-30,
                )
                fig_tvl.add_annotation(
                    x="Apr'26", y=9.5, text="$9.5M", showarrow=False,
                    font=dict(color=RED, size=10), xanchor="right",
                )
    
            brand_chart_layout(fig_tvl, height=270)
            fig_tvl.update_xaxes(tickangle=-40, tickfont=dict(size=8))
            fig_tvl.update_yaxes(tickprefix="$", ticksuffix="M", tickfont=dict(size=9))
            st.plotly_chart(fig_tvl, use_container_width=True, config={"displayModeBar": False})
            st.markdown(
                "<div class='chart-caption'>ACS window (shaded): $60M → $226M (+267%). "
                "Post-campaign: 96% collapse driven by SolvBTC.BBN exit (–62% within 30d of Jun 10 reward claim).</div>",
                unsafe_allow_html=True
            )

        with col_table:
            st.markdown("<div class='chart-card-title'>SEASON-BY-SEASON TVS SNAPSHOT ($M)</div>", unsafe_allow_html=True)

            # Build the table as HTML for brand styling
            rows_html = ""
            color_map = {
                "S1":"#185fa5","S2":"#185fa5","S3":"#185fa5","S4":"#185fa5",
                "S5":"#ba7517","S6":"#ba7517","S7":"#ba7517",
                "S8":"#993c1d","S9":"#993c1d","Post-ACS":"#993c1d",
            }
            for _, row in df_seasons.iterrows():
                s = str(row["season"])
                tvs = f"${row['tvs_usd_m']:.0f}M"
                dtx = f"{row['daily_tx_k']:.0f}K" if pd.notna(row.get("daily_tx_k")) else "—"
                nw  = f"{row['new_wallets_k']:.0f}K" if pd.notna(row.get("new_wallets_k")) else "est. low"
                bar_w = min(int(row.get("daily_tx_k", 0) / 18), 40)
                bar_c = color_map.get(s, MUTED)
                rows_html += f"""
                <tr style="border-bottom:1px solid {BORDER};">
                  <td style="padding:5px 6px;font-size:11px;color:{MUTED};font-weight:600;">{s}</td>
                  <td style="padding:5px 6px;font-size:11px;color:{WHITE};font-weight:500;">{tvs}</td>
                  <td style="padding:5px 6px;font-size:11px;color:{MUTED};">{dtx}
                    <span style="display:inline-block;height:4px;width:{bar_w}px;background:{bar_c};border-radius:2px;vertical-align:middle;margin-left:4px;"></span>
                  </td>
                  <td style="padding:5px 6px;font-size:11px;color:{MUTED};">{nw}</td>
                </tr>"""

            st.markdown(f"""
            <div style="background:{BG_CARD};border:1px solid {BORDER};border-radius:8px;padding:12px;overflow:auto;max-height:290px;">
              <table style="width:100%;border-collapse:collapse;">
                <thead>
                  <tr style="border-bottom:1px solid {BORDER};">
                    <th style="padding:4px 6px;font-size:9px;color:{MUTED};text-align:left;font-weight:600;letter-spacing:.08em;text-transform:uppercase;">Season</th>
                    <th style="padding:4px 6px;font-size:9px;color:{MUTED};text-align:left;font-weight:600;letter-spacing:.08em;text-transform:uppercase;">TVS</th>
                    <th style="padding:4px 6px;font-size:9px;color:{MUTED};text-align:left;font-weight:600;letter-spacing:.08em;text-transform:uppercase;">Daily tx avg</th>
                    <th style="padding:4px 6px;font-size:9px;color:{MUTED};text-align:left;font-weight:600;letter-spacing:.08em;text-transform:uppercase;">New wallets</th>
                  </tr>
                </thead>
                <tbody>{rows_html}</tbody>
              </table>
            </div>
            """, unsafe_allow_html=True)

        st.markdown("<div style='height:6px'></div>", unsafe_allow_html=True)

        # ══════════════════════════════════════════════════════════════════
        # ROW 3 — Protocol Retention  |  ASTR Bridge  |  Gas per Tx
        # ══════════════════════════════════════════════════════════════════
        c_ret, c_bridge, c_gas = st.columns(3)

        with c_ret:
            st.markdown("<div class='chart-card-title'>PROTOCOL TVL RETENTION (90D POST-ACS)</div>", unsafe_allow_html=True)
            df_p = df_protocols.copy().sort_values("retention_pct", ascending=True)
            color_fn = lambda v: GREEN if v >= 5 else (AMBER if v >= 1.5 else RED)
            bar_colors = [color_fn(v) for v in df_p["retention_pct"]]
            fig_ret = go.Figure(go.Bar(
                x=df_p["retention_pct"], y=df_p["protocol"],
                orientation="h",
                marker=dict(color=bar_colors, line=dict(width=0)),
                text=[f"{v:.1f}%" for v in df_p["retention_pct"]],
                textposition="outside",
                textfont=dict(size=10, color=WHITE),
                hovertemplate="<b>%{y}</b><br>Retention: %{x:.1f}%<extra></extra>",
                width=0.55,
            ))
            brand_chart_layout(fig_ret, height=240)
            fig_ret.update_xaxes(ticksuffix="%", range=[0, 16], showgrid=True)
            fig_ret.update_yaxes(tickfont=dict(size=10))
            fig_ret.update_layout(margin=dict(l=6, r=40, t=12, b=10))
            st.plotly_chart(fig_ret, use_container_width=True, config={"displayModeBar": False})
            st.markdown(
                "<div class='chart-caption'>No protocol exceeded 12% TVL retention. "
                "QuickSwap's resilience reflects its multi-chain liquidity base, not Soneium-native demand.</div>",
                unsafe_allow_html=True
            )

        with c_bridge:
            st.markdown("<div class='chart-card-title'>ASTR BRIDGE FLOW — NET INFLOW BY SEASON (M)</div>", unsafe_allow_html=True)
            bar_c_bridge = [RED if v > 50 else (AMBER if v > 1 else BLUE) for v in df_bridge["inflow_m"]]
            fig_br = go.Figure(go.Bar(
                x=df_bridge["season"], y=df_bridge["inflow_m"],
                marker=dict(color=bar_c_bridge, line=dict(width=0)),
                hovertemplate="<b>%{x}</b><br>Inflow: %{y:.2f}M ASTR<extra></extra>",
                width=0.6,
            ))
            # Reward-rate reference line
            fig_br.add_hline(y=10, line_dash="dot", line_color=f"{PINK}66", line_width=1,
                             annotation_text="reward rate", annotation_font=dict(size=8, color=PINK),
                             annotation_position="right")
            brand_chart_layout(fig_br, height=240)
            fig_br.update_yaxes(ticksuffix="M")
            st.plotly_chart(fig_br, use_container_width=True, config={"displayModeBar": False})
            st.markdown(
                "<div class='chart-caption'>Bridge saturation by S3. 99% of total ASTR inflow happened "
                "in first 20 days — the remaining 80 days added virtually nothing, yet continued to be rewarded at full rate.</div>",
                unsafe_allow_html=True
            )

        with c_gas:
            st.markdown("<div class='chart-card-title'>GAS PER TRANSACTION — ECONOMIC DEPTH PROXY (K GAS/TX)</div>", unsafe_allow_html=True)
            pt_colors = [RED if i == 3 else AMBER for i in range(len(df_gas))]
            fig_gas = go.Figure()
            fig_gas.add_trace(go.Scatter(
                x=df_gas["season"], y=df_gas["gas_per_tx_k"],
                mode="lines+markers",
                line=dict(color=AMBER, width=2.5),
                marker=dict(color=pt_colors, size=[12 if i == 3 else 7 for i in range(len(df_gas))],
                            line=dict(color=BG_DARK, width=1.5)),
                fill="tozeroy", fillcolor=f"{AMBER}12",
                hovertemplate="<b>%{x}</b><br>Gas/tx: %{y:.0f}K<extra></extra>",
            ))
            fig_gas.add_annotation(
                x="S4", y=447, text="Peak 447K<br>(genuine DeFi)",
                showarrow=True, arrowhead=2, arrowcolor=RED,
                font=dict(color=RED, size=9), ax=40, ay=-25,
            )
            fig_gas.add_annotation(
                x="S5", y=207, text="↓ 207K hollow",
                showarrow=False, font=dict(color=MUTED, size=9), yshift=12,
            )
            brand_chart_layout(fig_gas, height=240)
            fig_gas.update_yaxes(ticksuffix="K", range=[0, 520])
            st.plotly_chart(fig_gas, use_container_width=True, config={"displayModeBar": False})
            st.markdown(
                "<div class='chart-caption'>S5 drop from 447K → 207K gas/tx marks the exact inflection "
                "where genuine DeFi interactions gave way to low-complexity reward farming. "
                "This signal was not published by Astar.</div>",
                unsafe_allow_html=True
            )

        st.markdown("<hr class='acs-divider'>", unsafe_allow_html=True)

        # ══════════════════════════════════════════════════════════════════
        # ROW 4 — Protocol Autopsy Grouped Bar  |  L2 Benchmark
        # ══════════════════════════════════════════════════════════════════
        c_autopsy, c_l2 = st.columns([1.2, 1])

        with c_autopsy:
            st.markdown("<div class='chart-card-title'>PROTOCOL AUTOPSY — ACS PEAK VS. CURRENT TVL ($M)</div>", unsafe_allow_html=True)
            fig_proto = go.Figure()
            fig_proto.add_trace(go.Bar(
                name="ACS peak", x=df_protocols["protocol"], y=df_protocols["acs_peak_tvl_m"],
                marker=dict(color=BLUE, opacity=0.75, line=dict(width=0)),
                hovertemplate="<b>%{x}</b><br>Peak: $%{y:.0f}M<extra></extra>",
                width=0.35,
            ))
            fig_proto.add_trace(go.Bar(
                name="Current (Apr 2026)", x=df_protocols["protocol"], y=df_protocols["current_tvl_m"],
                marker=dict(color=PINK, opacity=0.85, line=dict(width=0)),
                hovertemplate="<b>%{x}</b><br>Current: $%{y:.2f}M<extra></extra>",
                width=0.35,
            ))
            fig_proto.update_layout(barmode="group", bargap=0.3)
            brand_chart_layout(fig_proto, height=280)
            fig_proto.update_yaxes(tickprefix="$", ticksuffix="M")
            fig_proto.update_xaxes(tickangle=-20, tickfont=dict(size=9))
            st.plotly_chart(fig_proto, use_container_width=True, config={"displayModeBar": False})
            st.markdown(
                "<div class='chart-caption'>Kyo Finance: $55M → $987K (–98.2%). Untitled Bank: $40M → $248K (–99.4%). "
                "The two largest ACS DeFi beneficiaries have essentially no organic TVL floor.</div>",
                unsafe_allow_html=True
            )

        with c_l2:
            st.markdown("<div class='chart-card-title'>L2 POST-INCENTIVE RETENTION BENCHMARK</div>", unsafe_allow_html=True)

            bench_html = ""
            chain_colors = {"Soneium": RED, "Base": GREEN, "Blast": AMBER, "Linea": BLUE}
            for _, r in df_l2.iterrows():
                chain = r["chain"]
                c = chain_colors.get(chain, MUTED)
                peak_w = min(int(r["peak_tvl_m"] / 25), 100)
                ret_w  = min(int(r["tvl_90d_m"] / 25), 100)
                ret_pct = f"{r['retention_pct']:.0f}%"
                bench_html += f"""
                <div style="margin-bottom:14px;">
                  <div style="font-size:12px;font-weight:600;color:{WHITE};margin-bottom:5px;">{chain}</div>
                  <div style="display:flex;align-items:center;gap:8px;margin-bottom:4px;">
                    <span style="font-size:9px;color:{MUTED};min-width:28px;text-align:right;">peak</span>
                    <div style="flex:1;height:5px;background:{BORDER};border-radius:3px;overflow:hidden;">
                      <div style="width:{peak_w}%;height:100%;background:{c};opacity:.5;border-radius:3px;"></div>
                    </div>
                    <span style="font-size:9px;color:{MUTED};min-width:42px;">${r['peak_tvl_m']:,.0f}M</span>
                  </div>
                  <div style="display:flex;align-items:center;gap:8px;">
                    <span style="font-size:9px;color:{MUTED};min-width:28px;text-align:right;">90d</span>
                    <div style="flex:1;height:5px;background:{BORDER};border-radius:3px;overflow:hidden;">
                      <div style="width:{ret_w}%;height:100%;background:{c};border-radius:3px;"></div>
                    </div>
                    <span style="font-size:9px;color:{c};min-width:42px;font-weight:700;">${r['tvl_90d_m']:,.0f}M ({ret_pct})</span>
                  </div>
                </div>"""

            st.markdown(f"""
            <div style="background:{BG_CARD};border:1px solid {BORDER};border-radius:8px;padding:14px;height:280px;overflow:auto;">
              {bench_html}
            </div>""", unsafe_allow_html=True)
            st.markdown(
                "<div class='chart-caption'>Soneium's 4% 90-day retention is significantly below the 18–35% range "
                "seen on comparable L2 launches. Base's structural distribution advantage (Coinbase users) "
                "and Blast's passive yield model explain the gap. Benchmarks are estimated from public reports.</div>",
                unsafe_allow_html=True
            )

        st.markdown("<hr class='acs-divider'>", unsafe_allow_html=True)

        # ══════════════════════════════════════════════════════════════════
        # ROW 5 — Asset Retention Waterfall  |  Gaming vs DeFi  |  Insights
        # ══════════════════════════════════════════════════════════════════
        c_assets, c_gd, c_insights = st.columns([1, 1, 1])

        with c_assets:
            st.markdown("<div class='chart-card-title'>ASTR ASSET RETENTION ON SONEIUM — JUN 10 → JUL 10 2025</div>", unsafe_allow_html=True)
            df_a = df_assets.sort_values("pct_change")
            colors_a = [RED if v < -30 else (PINK if v < 0 else GREEN) for v in df_a["pct_change"]]
            fig_a = go.Figure(go.Bar(
                x=df_a["pct_change"], y=df_a["asset"],
                orientation="h",
                marker=dict(color=colors_a, line=dict(width=0)),
                text=[f"{v:+.1f}%" for v in df_a["pct_change"]],
                textposition="outside",
                textfont=dict(size=10, color=WHITE),
                hovertemplate="<b>%{y}</b><br>Change: %{x:+.1f}%<extra></extra>",
                width=0.55,
            ))
            brand_chart_layout(fig_a, height=250)
            fig_a.update_xaxes(ticksuffix="%", range=[-80, 35])
            fig_a.update_layout(margin=dict(l=6, r=42, t=12, b=10))
            st.plotly_chart(fig_a, use_container_width=True, config={"displayModeBar": False})
            st.markdown(
                "<div class='chart-caption'>SolvBTC.BBN's –62% exit within 30 days of claim was the primary driver "
                "of post-ACS TVL collapse. USDC (+1%) and liquid staking derivatives "
                "(wstASTR +20%, vASTR +3%) were the stickiest assets — reflecting genuine utility beyond reward farming.</div>",
                unsafe_allow_html=True
            )

        with c_gd:
            st.markdown("<div class='chart-card-title'>GAMING VS DEFI RETENTION COMPARISON</div>", unsafe_allow_html=True)
            df_gd = df_gaming.sort_values("retention_pct", ascending=True)
            gd_colors = [PURPLE if t == "gaming" else BLUE for t in df_gd["type"]]
            fig_gd = go.Figure(go.Bar(
                x=df_gd["retention_pct"], y=df_gd["protocol"],
                orientation="h",
                marker=dict(color=gd_colors, line=dict(width=0)),
                text=[f"{v:.1f}%" for v in df_gd["retention_pct"]],
                textposition="outside",
                textfont=dict(size=10, color=WHITE),
                hovertemplate="<b>%{y}</b><br>Retention: %{x:.1f}%<extra></extra>",
                width=0.55,
            ))
            brand_chart_layout(fig_gd, height=250)
            fig_gd.update_xaxes(ticksuffix="%", range=[0, 18])
            fig_gd.update_layout(margin=dict(l=6, r=42, t=12, b=10))

            # Legend
            fig_gd.add_trace(go.Bar(x=[None], y=[None], marker_color=PURPLE, name="gaming", showlegend=True))
            fig_gd.add_trace(go.Bar(x=[None], y=[None], marker_color=BLUE,   name="defi",   showlegend=True))
            fig_gd.update_layout(legend=dict(orientation="h", y=1.08, x=0, font=dict(size=9)))

            st.plotly_chart(fig_gd, use_container_width=True, config={"displayModeBar": False})
            st.markdown(
                "<div class='chart-caption'>Gaming protocols outperform DeFi on retention. Yoki Legacy's completion "
                "mechanic (collect-a-set) yields 2× the retention of competitive MOBA format (Evermoon).</div>",
                unsafe_allow_html=True
            )

        with c_insights:
            st.markdown("<div class='chart-card-title'>KEY NEW INSIGHTS (NOT PUBLISHED BY ASTAR)</div>", unsafe_allow_html=True)
            insights = [
                ("01", "Gas/tx ratio dropped 2.2× in S5 (447K → 207K), revealing the exact season activity turned hollow — before Astar's own allocation cuts confirmed it."),
                ("02", "ASTR bridge saturation occurred by S3. The final 70 days of ACS added ~0.09M ASTR net inflow per season — yet continued to reward 80% of the TVL budget."),
                ("03", "AFC deployed 15M ASTR to Soneium Velodrome LPs in June 2025 as retail TVL collapsed — functioning as an emergency institutional backstop to prevent near-zero ASTR market depth."),
                ("04", "Gaming allocation optimized for gameable gas metrics — Path of Soneium (checklist app, no game loop) received 2M ASTR/season, equal to the most complex games. Farming infrastructure was systematically rewarded over genuine engagement."),
            ]
            for num, text in insights:
                st.markdown(f"""
                <div class="insight-box">
                  <div class="insight-num">Insight {num}</div>
                  <div class="insight-text">{text}</div>
                </div>""", unsafe_allow_html=True)

        st.markdown("<hr class='acs-divider'>", unsafe_allow_html=True)

        # ══════════════════════════════════════════════════════════════════
        # ROW 6 — RECOMMENDATIONS
        # ══════════════════════════════════════════════════════════════════
        st.markdown("""
        <div class='section-label'>Three Recommendations for Astar's Growth Team</div>
        """, unsafe_allow_html=True)

        r1, r2, r3 = st.columns(3)
        recs = [
            (r1,
             "REC 1 · Protocol + AFC · Q3 2026",
             "Introduce 90-day TVL vesting locks tied to post-campaign retention thresholds",
             "SolvBTC.BBN exited –62% within 30d, representing the majority of ACS peak TVL. "
             "A 90-day lock condition requiring ≥15% TVL retention as a prerequisite for full reward "
             "payout would have redirected ~$130M in phantom TVL incentives toward protocols with genuine "
             "organic floors.",
             "Success metric: ≥15% TVL retention across top-5 protocols at 90d post-campaign."),
            (r2,
             "REC 2 · Growth team + Sentio · Q2–Q3 2026",
             "Redirect 30% of discretionary budget to a 'sticky protocol tier' scored on 30-day return rate, not gas consumption",
             "Yoki Legacy's completion mechanic retained users at 2× the rate of Evermoon despite similar "
             "allocation levels. A 3-metric behavioral dashboard (30d return rate, sessions per retained "
             "wallet, in-app spending) built with Sentio by Q2 2026 would redirect incentives away from "
             "reward-loop infrastructure toward products with genuine stickiness.",
             "Target: average 3rd protocol return rate ≥10% across tier recipients."),
            (r3,
             "REC 3 · Business dev + Startale Labs · Q4 2026",
             "Secure one Sony IP integration before launching any follow-on incentive campaign",
             "Soneium's gaming retention (5–8%) sits below comparable gaming chains (15–40%) because no "
             "ACS gaming protocol had access to IP that drives brand affinity. Sony controls PlayStation "
             "franchises, anime, and music. Startale Labs' $63M Series A provides negotiating leverage. "
             "Gate ACS 2.0 gaming allocation on one signed Sony IP product being live.",
             "Success metric: ≥50K unique wallets within 60 days of Sony IP product launch."),
        ]
        for col, badge, title, body, metric in recs:
            with col:
                st.markdown(f"""
                <div class="rec-box">
                  <div class="rec-badge">{badge}</div>
                  <div class="rec-title">{title}</div>
                  <div class="rec-body">{body}</div>
                  <div class="rec-meta"><b>Success metric:</b> {metric}</div>
                </div>""", unsafe_allow_html=True)

        # ── Footer ────────────────────────────────────────────────────────
        st.markdown(f"""
        <div style="margin-top:32px;padding-top:16px;border-top:1px solid {BORDER};
                    font-size:10px;color:{MUTED};line-height:1.8;">
          Data sources: ACS Performance Reports (Astar Forum, 2025) &middot; DeFiLlama (April 2026) &middot;
          Blockscout Soneium dashboard &middot; AFC Monthly Report (July 2025)<br>
          Estimated figures carry ±15% uncertainty. L2 benchmark retention figures are approximate from public analyst reports.
        </div>
        """, unsafe_allow_html=True)
