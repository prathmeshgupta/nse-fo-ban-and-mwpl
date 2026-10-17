"""CLI Tool for NSE F&O Ban & MWPL.

Usage:
    python runner.py --summary
    python runner.py --symbol AMBUJACEM
"""

import argparse
import sys
from pathlib import Path
import pandas as pd

sys.path.insert(0, str(Path(__file__).resolve().parent / "src"))
from nse_fo_ban_and_mwpl.tracker import FOBanTracker

def main():
    parser = argparse.ArgumentParser(description="NSE F&O Ban & MWPL CLI")
    parser.add_argument("--symbol", help="Target F&O equity ticker")
    parser.add_argument("--summary", action="store_true", help="Show all scrips currently in F&O ban")
    args = parser.parse_args()

    parquet_path = Path(__file__).parent / "output" / "fo_ban_history.parquet"
    if not parquet_path.exists():
        print("Dataset not found. Run python update.py first.")
        return

    df = pd.read_parquet(parquet_path)
    tracker = FOBanTracker(df)

    latest_date = df["trade_date"].max()

    if args.symbol:
        is_banned = tracker.is_symbol_banned(args.symbol)
        sym_history = df[df["symbol"] == args.symbol.upper()]
        if is_banned:
            print(f"\n[ALERT] {args.symbol.upper()} is CURRENTLY IN F&O BAN for trade date {latest_date}!")
            print("  No fresh derivative positions may be initiated (exit only).")
        else:
            print(f"\n[NORMAL] {args.symbol.upper()} is NOT in F&O ban as of {latest_date}.")

        if not sym_history.empty:
            print(f"\n--- Historical Ban Occurrences for {args.symbol.upper()} ---")
            print(sym_history[["trade_date", "symbol", "ban_status", "consecutive_days_in_ban", "reason"]].to_string(index=False))
        print()

    else:
        banned = tracker.get_latest_banned_scrips()
        print(f"\n==========================================================================")
        print(f" NSE F&O BAN STATUS AS OF TRADE DATE {latest_date}")
        print(f"==========================================================================")
        if not banned:
            print("No securities currently in F&O ban.")
        else:
            print(f"Total Securities in Ban: {len(banned)}\n")
            day_df = df[df["trade_date"] == latest_date]
            print(day_df[["symbol", "ban_status", "consecutive_days_in_ban", "reason"]].to_string(index=False))
        print(f"==========================================================================\n")

if __name__ == "__main__":
    main()
