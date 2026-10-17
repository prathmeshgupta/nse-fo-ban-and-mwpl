"""Quality and Integrity Audit for NSE F&O Ban Dataset."""

import pandas as pd
from pathlib import Path

def audit_quality():
    print("=" * 65)
    print(" NSE F&O BAN & MWPL - DATA QUALITY AUDIT")
    print("=" * 65)

    parquet_path = Path(__file__).parent / "output" / "fo_ban_history.parquet"
    assert parquet_path.exists(), f"Missing {parquet_path.name}"

    df = pd.read_parquet(parquet_path)
    print(f"Total Ban Observations Indexed: {len(df):,}")

    null_syms = df["symbol"].isnull().sum()
    null_dates = df["trade_date"].isnull().sum()
    null_status = df["ban_status"].isnull().sum()

    print(f"Null Symbols: {null_syms} {'[PASS]' if null_syms == 0 else '[FAIL]'}")
    print(f"Null Trade Dates: {null_dates} {'[PASS]' if null_dates == 0 else '[FAIL]'}")
    print(f"Null Ban Status: {null_status} {'[PASS]' if null_status == 0 else '[FAIL]'}")

    distinct_dates = df["trade_date"].nunique()
    print(f"Distinct Trading Dates Covered: {distinct_dates}")

    assert null_syms == 0, "Symbols contain nulls!"
    assert null_dates == 0, "Trade dates contain nulls!"
    assert null_status == 0, "Ban status contains nulls!"

    print("=" * 65)
    print("ALL AUDIT CHECKS PASSED.")
    print("=" * 65)

if __name__ == "__main__":
    audit_quality()
