# ORB Pro

ORB Pro is a TradingView Pine Script (v5) implementation of an Opening Range Breakout (ORB) strategy with built-in filters, partial exits, runner trailing, breakeven logic, and a backtest-range input. The strategy in this repository is `ORB_Pro_Refactored_FIXED.pine`.

## Features
- Opening Range breakout entries with configurable OR window and timezone
- VWAP, EMA, and HTF (higher timeframe) trend confirmation filters
- ATR-based OR width filtering and low-volatility skip
- Optional 2nd-candle confirmation and VWAP slope anti-chop filter
- Configurable TP/SL as percentages of OR, partial TP (TP1) + runner trails
- One-time breakeven move and optional max-dollar-loss cap per trade
- Backtest range: auto last-N-days (default 30) or manual start/end timestamps
- Alerts support (toggleable via `Enable Alerts` input)

## Usage
1. Open TradingView and go to the Pine Editor.
2. Create a new script and paste the contents of `ORB_Pro_Refactored_FIXED.pine`.
3. Add the script to a chart (choose your symbol and timeframe).
4. Configure inputs in the strategy settings:
   - `Auto backtest last N days` (default enabled) and `Backtest Days` (default 30) — toggles the default backtest window.
   - `Enable Alerts` — when enabled, alerts are sent for entry, TP1, runner SL, VWAP invalidations, breakeven, and daily flat.
   - Other inputs: OR window, VWAP/EMA/HTF filters, TP/SL percentages, partials, ATR trail settings, etc.

## Notes
- The script is written for Pine Script v5.
- When `backtestAuto` is true, the script sets the backtest window to the last `backtestDays` days automatically.
- If you choose manual backtest mode, set `Backtest Start` and `Backtest End` to the desired timestamps.

## Files
- `ORB_Pro_Refactored_FIXED.pine` — main strategy source.

## License
This repository is distributed under the MIT License (see `LICENSE`).

---
Contributions, issues, and feature requests are welcome.