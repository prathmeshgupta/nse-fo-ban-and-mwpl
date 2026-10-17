"""NSE F&O Ban & MWPL Fetcher.

Downloads official securities in ban period from NSE archives (fo_secban.csv),
parses the target trade session date, and extracts banned scrips.
"""

import re
import requests
import pandas as pd
from datetime import datetime, date
from typing import Optional, List, Dict, Any

NSE_SECBAN_URL = "https://nsearchives.nseindia.com/content/fo/fo_secban.csv"

HEADERS = {
    "User-Agent": "Mozilla/5.0 (Windows NT 10.0; Win64; x64) AppleWebKit/537.36 (KHTML, like Gecko) Chrome/124.0.0.0 Safari/537.36",
    "Accept": "text/html,application/xhtml+xml,application/xml;q=0.9,*/*;q=0.8",
}

class FOBanFetcher:
    """Fetches official F&O ban period securities from NSE archives."""

    def __init__(self):
        self.session = requests.Session()
        self.session.headers.update(HEADERS)

    def fetch_latest_ban(self) -> pd.DataFrame:
        """Fetch current F&O ban list from NSE archives."""
        try:
            resp = self.session.get(NSE_SECBAN_URL, timeout=15)
            if resp.status_code != 200 or not resp.text.strip():
                return pd.DataFrame()

            lines = [line.strip() for line in resp.text.strip().split("\n") if line.strip()]
            if not lines:
                return pd.DataFrame()

            # First line contains date, e.g. "Securities in Ban For Trade Date 19-OCT-2026:"
            header_line = lines[0]
            date_match = re.search(r"(\d{1,2}-[A-Za-z]{3}-\d{4})", header_line)
            if date_match:
                date_str = date_match.group(1)
                trade_date = pd.to_datetime(date_str).strftime("%Y-%m-%d")
            else:
                trade_date = date.today().strftime("%Y-%m-%d")

            banned_symbols = []
            for line in lines[1:]:
                # Lines are like "1,AMBUJACEM" or "2,KAYNES"
                parts = line.split(",")
                if len(parts) >= 2:
                    sym = parts[1].strip().upper()
                else:
                    sym = parts[0].strip().upper()

                # Clean any number prefixes
                sym = re.sub(r"^\d+\.?\s*", "", sym).strip()
                if sym and not sym.startswith("NO RECORDS"):
                    banned_symbols.append(sym)

            records = []
            for sym in banned_symbols:
                records.append({
                    "trade_date": trade_date,
                    "symbol": sym,
                    "ban_status": "IN_BAN",
                    "reason": "Exceeded 95% Market Wide Position Limit (MWPL)",
                    "source": "NSE_FO_SECBAN"
                })

            return pd.DataFrame(records)

        except Exception as e:
            print(f"Error fetching F&O ban list: {e}")
            return pd.DataFrame()
