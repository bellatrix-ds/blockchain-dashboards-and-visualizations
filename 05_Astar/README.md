# ACS Campaign Post-Mortem — Streamlit Dashboard

Dark-themed analytics dashboard for the Astar Contribution Score post-mortem,
styled with the ACS brand kit (dark background, hot-pink + electric-blue palette).

---

## Quick Start

```bash
pip install -r requirements.txt
streamlit run acs_dashboard.py
```

---

## GitHub CSV Setup

1. Open `acs_dashboard.py` and update line ~40:
   ```python
   GITHUB_RAW_BASE = "https://raw.githubusercontent.com/YOUR_USERNAME/YOUR_REPO/main/data/"
   ```

2. Create a `/data/` folder in your repo and push the following CSV files.

---

## Required CSV Files & Schema

All files live in your GitHub repo under `/data/`.

### `tvl_trajectory.csv`
| column | type | description |
|--------|------|-------------|
| period | str | Label for x-axis (e.g. "Nov'24", "S1", "Apr'26") |
| tvl_usd_m | float | TVL in USD millions |
| acs_active | int | 1 = inside ACS window, 0 = outside |

### `season_metrics.csv`
| column | type | description |
|--------|------|-------------|
| season | str | Season label ("S1" … "S9", "Post-ACS") |
| tvs_usd_m | float | Total value secured in $M |
| daily_tx_k | float | Average daily transactions in thousands |
| new_wallets_k | float | New wallets added that season (K) |

### `protocol_tvl.csv`
| column | type | description |
|--------|------|-------------|
| protocol | str | Protocol name |
| acs_peak_tvl_m | float | Peak TVL during ACS in $M |
| current_tvl_m | float | TVL as of April 2026 in $M |
| retention_pct | float | (current / peak) × 100 |
| verdict | str | "holds", "weak", or "gone" |

### `astr_bridge.csv`
| column | type | description |
|--------|------|-------------|
| season | str | "S1" … "S9" |
| inflow_m | float | Net ASTR inflow that season in millions |

### `gas_per_tx.csv`
| column | type | description |
|--------|------|-------------|
| season | str | "S1" … "S9" |
| gas_per_tx_k | float | Average gas consumed per transaction (thousands) |

### `asset_retention.csv`
| column | type | description |
|--------|------|-------------|
| asset | str | Asset name (e.g. "SolvBTC.BBN", "ASTR") |
| pct_change | float | % change Jun 10 → Jul 10 2025 (negative = exit) |

### `gaming_defi_retention.csv`
| column | type | description |
|--------|------|-------------|
| protocol | str | Protocol name |
| retention_pct | float | Estimated post-ACS user/wallet retention % |
| type | str | "gaming" or "defi" |

### `l2_benchmark.csv`
| column | type | description |
|--------|------|-------------|
| chain | str | Chain name ("Soneium", "Base", "Blast", "Linea") |
| peak_tvl_m | float | Incentive-period peak TVL in $M |
| tvl_90d_m | float | TVL 90 days post-incentive in $M |
| retention_pct | float | (tvl_90d / peak) × 100 |

---

## Fallback Behaviour

If the GitHub fetch fails (wrong URL, private repo, or no internet),
the app automatically loads **bundled sample data** matching the exact
schemas above and displays a yellow warning banner. The dashboard remains
fully functional — just replace GITHUB_RAW_BASE and upload real CSVs when ready.

---

## Deployment

### Streamlit Community Cloud (free)
1. Push `acs_dashboard.py` and `requirements.txt` to your GitHub repo root.
2. Go to [share.streamlit.io](https://share.streamlit.io) → New app → select your repo.
3. Main file path: `acs_dashboard.py`
4. Deploy.

### Local only
```bash
streamlit run acs_dashboard.py --server.port 8501
```

---

## Brand Kit Reference (from ACS Season 4 banner)
| Token | Hex |
|-------|-----|
| Background | `#0d0d12` |
| Card surface | `#13131e` |
| Hot pink / primary | `#e8198b` |
| Electric blue / secondary | `#00b4ff` |
| Cyan highlight | `#00e5ff` |
| Mid purple | `#7c3aed` |
| Muted text | `#6b6b8a` |
| Border | `#252540` |
