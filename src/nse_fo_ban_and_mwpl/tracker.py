"""F&O Ban History & Consecutive Days Tracker."""

import pandas as pd
from typing import Dict, Any, List

class FOBanTracker:
    """Tracks consecutive days in ban and ban entry/exit events."""

    def __init__(self, df: pd.DataFrame):
        self.df = df.copy()

    def get_latest_banned_scrips(self, as_of_date: str = None) -> List[str]:
        """Returns list of scrips currently in F&O ban."""
        if self.df.empty:
            return []
        target_date = as_of_date or self.df["trade_date"].max()
        day_df = self.df[self.df["trade_date"] == target_date]
        return day_df[day_df["ban_status"] == "IN_BAN"]["symbol"].tolist()

    def is_symbol_banned(self, symbol: str, as_of_date: str = None) -> bool:
        """Returns True if the target ticker is currently in ban."""
        banned = self.get_latest_banned_scrips(as_of_date)
        return symbol.upper() in banned
