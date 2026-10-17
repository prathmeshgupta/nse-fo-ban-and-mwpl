# NSE F&O Ban & MWPL Registry

[![Daily/Weekly FO Ban Dataset Update](https://github.com/prathmeshgupta/nse-fo-ban-and-mwpl/actions/workflows/weekly_update.yml/badge.svg)](https://github.com/prathmeshgupta/nse-fo-ban-and-mwpl/actions/workflows/weekly_update.yml)
[![License: MIT](https://img.shields.io/badge/License-MIT-yellow.svg)](https://opensource.org/licenses/MIT)
[![Python 3.10+](https://img.shields.io/badge/python-3.10+-blue.svg)](https://www.python.org/downloads/)

Audited, daily time-series dataset of National Stock Exchange of India (NSE) **Futures & Options (F&O) Ban Period Securities** and **Market-Wide Position Limit (MWPL) breaches**.

Essential for algorithmic derivative strategies, preventing exchange ban penalty violations, and tracking short-squeeze volatility shocks.

---

### Regulatory Background & The 95% MWPL Rule

In the Indian equity derivatives market, the exchange enforces a Market Wide Position Limit (MWPL) on every single-stock derivative:
1. **Entering Ban Period:** When aggregate open interest across all futures and option contracts of an underlying stock crosses **95% of its MWPL**, the exchange places the scrip under the **F&O Ban Period**.
2. **Trading Restrictions:** While in ban, **no market participant is permitted to initiate a fresh position** (neither long nor short). Only unwinding or squaring off existing positions is permitted.
3. **Severe Penalties:** Any trader attempting to increase open interest in a banned scrip faces exchange penalties starting at ₹100,000+ per contract.
4. **Exiting Ban Period:** A security exits the ban period only when its aggregate open interest falls below **80% of MWPL**.

---

### Dataset Schema

Outputs are distributed in both **Apache Parquet (`snappy` compressed)** and standard **CSV**:
* `output/fo_ban_history.parquet`
* `output/fo_ban_history.csv`

| Field | Type | Description |
| :--- | :--- | :--- |
| `trade_date` | `string` | Trade session date in `YYYY-MM-DD` |
| `symbol` | `string` | NSE F&O Symbol (e.g. `AMBUJACEM`, `SAIL`, `KAYNES`) |
| `ban_status` | `string` | `IN_BAN` |
| `reason` | `string` | Regulatory trigger (`Exceeded 95% Market Wide Position Limit (MWPL)`) |
| `consecutive_days_in_ban` | `int64` | Running count of consecutive sessions in ban |
| `source` | `string` | Data source origin (`NSE_FO_SECBAN`) |

---

### Automated Weekly & Daily Updates

* **Schedule**: Automated GitHub Actions workflow executes at **14:15 UTC (19:45 IST) Monday to Friday**, with a Sunday reconciliation at **02:00 UTC**.
* **Zero Secrets**: Uses public NSE clearing archives (`nsearchives.nseindia.com/content/fo/fo_secban.csv`).

---

### Quickstart & CLI Usage

```bash
# 1. Clone the repository
git clone https://github.com/prathmeshgupta/nse-fo-ban-and-mwpl.git
cd nse-fo-ban-and-mwpl

# 2. Install dependencies
pip install -r requirements.txt

# 3. Run the automated updater locally
python update.py

# 4. View all scrips currently in F&O ban
python runner.py --summary

# 5. Check if a specific ticker is in ban
python runner.py --symbol AMBUJACEM
```
