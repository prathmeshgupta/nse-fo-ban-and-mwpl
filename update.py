"""NSE F&O Ban Weekly/Daily Automated Updater.

Fetches latest official securities in F&O ban from NSE archives,
updates historical ban logs, calculates consecutive days in ban, and exports Parquet/CSV.
"""

import sys
from datetime import datetime
from pathlib import Path
import pandas as pd

# Add local src to path for direct execution
sys.path.insert(0, str(Path(__file__).resolve().parent / "src"))

from nse_fo_ban_and_mwpl.fetcher import FOBanFetcher

def update_fo_ban():
    print(f"[{datetime.now().isoformat()}] Starting F&O Ban update...")
    fetcher = FOBanFetcher()
    output_dir = Path(__file__).resolve().parent / "output"
    output_dir.mkdir(parents=True, exist_ok=True)
    csv_file = output_dir / "fo_ban_history.csv"
    parquet_file = output_dir / "fo_ban_history.parquet"

    existing_df = pd.DataFrame()
    if parquet_file.exists():
        existing_df = pd.read_parquet(parquet_file)
        print(f"Loaded {len(existing_df):,} existing records from {parquet_file.name}")

    print("Fetching latest F&O ban list from NSE archives...")
    new_df = fetcher.fetch_latest_ban()

    if new_df.empty and existing_df.empty:
        raise RuntimeError("No ban data retrieved and no existing database found.")

    combined = []
    if not existing_df.empty:
        combined.append(existing_df)
    if not new_df.empty:
        print(f"Retrieved {len(new_df)} scrips in F&O ban for {new_df['trade_date'].iloc[0]}.")
        combined.append(new_df)

    merged = pd.concat(combined, ignore_index=True)

    # Core key deduplication
    merged = merged.drop_duplicates(subset=["trade_date", "symbol"], keep="last")

    # Sort deterministically
    merged = merged.sort_values(by=["trade_date", "symbol"], ascending=[False, True]).reset_index(drop=True)

    # Calculate consecutive days in ban
    consec_counts = []
    for _, row in merged.iterrows():
        sym = row["symbol"]
        dt = row["trade_date"]
        # Count prior consecutive occurrences
        prior = merged[(merged["symbol"] == sym) & (merged["trade_date"] <= dt)]
        consec_counts.append(len(prior))
    merged["consecutive_days_in_ban"] = consec_counts

    # Save
    merged.to_parquet(parquet_file, index=False, compression="snappy")
    merged.to_csv(csv_file, index=False)
    print(f"Saved {len(merged):,} records to {parquet_file.name} and {csv_file.name}")

    # Run quality gate
    from evaluate_quality import audit_quality
    audit_quality()
    print("F&O Ban update completed successfully.")

if __name__ == "__main__":
    update_fo_ban()
