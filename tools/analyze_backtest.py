#!/usr/bin/env python3
"""Simple backtest CSV analyzer for TradingView-style strategy exports.

Usage:
  python3 tools/analyze_backtest.py /path/to/backtest.csv

The script attempts to detect a numeric profit column and computes:
- total trades, wins, losses, win rate
- net profit, gross profit, gross loss, profit factor
- average win/loss, expectancy
- max drawdown (trade-by-trade) and max drawdown percent
- average P&L per trade

If column names differ, pass --profit-col NAME to specify the profit column.
"""
import sys
import math
from pathlib import Path
import argparse

try:
    import pandas as pd
    import numpy as np
except Exception as e:
    print("Missing dependencies. Install with: pip install pandas numpy")
    raise


def detect_profit_col(df):
    # look for likely profit columns
    lowercols = [c.lower() for c in df.columns]
    for candidate in ["profit", "pnl", "net profit", "net_pnl", "profit_usd", "pl", "realized"]:
        for i, c in enumerate(lowercols):
            if candidate in c:
                return df.columns[i]
    # fallback: any numeric column named like 'profit' or containing 'profit'
    for i, c in enumerate(lowercols):
        if "profit" in c or "pnl" in c or "pl" in c:
            return df.columns[i]
    # last resort: numeric column other than time/index
    numeric = [c for c in df.columns if pd.api.types.is_numeric_dtype(df[c])]
    if len(numeric) == 1:
        return numeric[0]
    return None


def max_drawdown(cum):
    peak = -1e18
    mdd = 0.0
    peak_index = 0
    trough_index = 0
    for i, v in enumerate(cum):
        if v > peak:
            peak = v
            peak_i = i
        dd = peak - v
        if dd > mdd:
            mdd = dd
            peak_index = peak_i
            trough_index = i
    return mdd, peak_index, trough_index


def analyze(path, profit_col=None):
    df = pd.read_csv(path)
    if profit_col is None:
        profit_col = detect_profit_col(df)
    if profit_col is None:
        print("Could not detect profit column. Columns found:", list(df.columns))
        return 1
    print(f"Using profit column: {profit_col}")
    # coerce to numeric
    df[profit_col] = pd.to_numeric(df[profit_col], errors='coerce')
    trades = df[~df[profit_col].isna()].copy()
    trades = trades.reset_index(drop=True)
    n = len(trades)
    wins = trades[trades[profit_col] > 0]
    losses = trades[trades[profit_col] <= 0]
    gross_profit = wins[profit_col].sum()
    gross_loss = losses[profit_col].sum()
    net = trades[profit_col].sum()
    win_rate = len(wins) / n * 100 if n>0 else 0
    avg_win = wins[profit_col].mean() if len(wins)>0 else 0
    avg_loss = losses[profit_col].mean() if len(losses)>0 else 0
    pf = (gross_profit / -gross_loss) if gross_loss < 0 else float('inf')
    expectancy = (win_rate/100.0) * (avg_win) + (1 - win_rate/100.0) * (avg_loss)
    avg_trade = net / n if n>0 else 0
    # cumulative equity curve
    cum = trades[profit_col].fillna(0).cumsum().to_numpy()
    mdd, peak_i, trough_i = max_drawdown(cum)
    mdd_pct = (mdd / (cum[peak_i] if cum[peak_i]!=0 else 1)) * 100 if n>0 else 0

    print("\n=== Summary ===")
    print(f"Total trades: {n}")
    print(f"Wins: {len(wins)}, Losses: {len(losses)}, Win rate: {win_rate:.2f}%")
    print(f"Net profit: {net:.2f}")
    print(f"Gross profit: {gross_profit:.2f}")
    print(f"Gross loss: {gross_loss:.2f}")
    print(f"Profit factor: {pf:.2f}")
    print(f"Average win: {avg_win:.2f}")
    print(f"Average loss: {avg_loss:.2f}")
    print(f"Expectancy per trade: {expectancy:.4f}")
    print(f"Avg P&L per trade: {avg_trade:.4f}")
    print(f"Max drawdown: {mdd:.2f} (peak idx {peak_i} -> trough idx {trough_i}), {mdd_pct:.2f}%")

    # Add simple daily summary if timestamp column exists
    time_cols = [c for c in df.columns if 'time' in c.lower() or 'date' in c.lower()]
    if time_cols:
        tcol = time_cols[0]
        try:
            trades['_t'] = pd.to_datetime(trades[tcol])
            daily = trades.groupby(trades['_t'].dt.date)[profit_col].sum()
            print('\n=== Daily Summary (last 10) ===')
            print(daily.tail(10))
            print('\nAvg daily P&L:', daily.mean(), 'Std daily P&L:', daily.std())
        except Exception:
            pass

    return 0


def main():
    p=argparse.ArgumentParser()
    p.add_argument('csv', help='CSV file path')
    p.add_argument('--profit-col', help='Explicit profit column name', default=None)
    args = p.parse_args()
    return analyze(args.csv, args.profit_col)

if __name__=='__main__':
    sys.exit(main())
