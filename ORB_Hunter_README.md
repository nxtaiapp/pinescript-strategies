# ORB Pro - Opening Range Breakout Strategy

A professional-grade TradingView Pine Script (v5) implementation of an Opening Range Breakout strategy with comprehensive filters, partial exits, trailing stops, and risk management.

## Strategy Overview

ORB Pro trades breakouts from the **Opening Range** - the high/low established during the first 15 minutes of the NY session (9:30-9:45 AM ET). The strategy enters when price breaks above/below this range with multiple confirmation filters.

---

## Entry Logic

### Long Entry
- Price breaks **above** OR High
- All confirmation filters pass

### Short Entry
- Price breaks **below** OR Low
- All confirmation filters pass (inverse)

### Confirmation Filters

| Filter | Description | Default |
|--------|-------------|---------|
| **VWAP** | Price must be above/below VWAP | Enabled |
| **Breakout Buffer** | Requires 2 ticks beyond OR level | 2 ticks |
| **EMA (34)** | Price aligned with 34-period EMA | Enabled |
| **HTF Trend** | Price above/below 100 EMA on 30-min | Enabled |
| **2nd Candle** | Waits for confirming close beyond OR | Enabled |
| **ATR Min** | OR width >= 0.5x ATR (filters tight ranges) | Enabled |
| **ATR Max** | OR width <= 1.5x ATR (filters wide ranges) | Enabled |
| **VWAP Slope** | Anti-chop filter based on VWAP momentum | Disabled |
| **Inside Day Skip** | Avoids inside days vs prior day | Disabled |
| **Low Vol Skip** | Skips if today ATR < yesterday ATR | Disabled |

### 2nd Candle Confirmation
Prevents false breakouts by requiring:
1. Current bar is beyond OR level
2. Prior bar **closed** beyond OR level
3. Bar before that was at/within OR level

---

## Exit Conditions

### 1. Take Profit / Stop Loss
| Level | Calculation |
|-------|-------------|
| **Take Profit** | 100% of OR width beyond entry |
| **Stop Loss** | 50% of OR width against entry |

### 2. Partial Exit System
When enabled (default), the position is split:

| Exit | Trigger | Position % |
|------|---------|------------|
| **TP1** | 1R (1x OR width) profit | 50% |
| **Runner** | Trailing stop at 1.5x ATR | 50% |

The trailing stop activates after price moves 0.75R in profit.

### 3. Breakeven Stop
- **Trigger**: Price moves 75% of OR width in profit
- **Action**: Stop moves to entry price (one-time)

### 4. VWAP Invalidation
- Exits immediately if price crosses back through VWAP
- Acts as trend invalidation signal

### 5. End of Day Flat
- All positions closed at 4:00 PM New York time
- No overnight exposure

---

## Trading Sessions

| Session | Time (ET) | Default |
|---------|-----------|---------|
| **Opening Range** | 9:30 - 9:45 AM | Enabled |
| **AM Session** | 9:30 - 11:45 AM | Enabled |
| **PM Session** | 2:30 - 3:45 PM | Disabled |

---

## Input Parameters

### Opening Range & Sessions
- `Opening Range Window` - Time window for OR formation (default: 0930-0945)
- `OR Timezone` - Timezone for OR calculation
- `Enable Trading Window(s)` - Restrict entries to session times
- `AM Session` / `PM Session` - Define allowed trading windows

### Confirmations
- `Require VWAP Confirmation` - Price must be on correct side of VWAP
- `Breakout Buffer (ticks)` - Minimum ticks beyond OR for entry
- `Enable EMA Filter` - Require EMA alignment
- `EMA Length` - Period for EMA calculation (default: 34)
- `Require 2nd-Candle Confirmation` - Wait for confirming close

### HTF Trend Filter
- `Enable HTF Trend Filter` - Use higher timeframe trend
- `HTF Timeframe` - Higher timeframe to check (default: 30m)
- `HTF EMA Length` - EMA period on HTF (default: 100)
- `Only trade when HTF bar is CLOSED` - Avoid repainting

### ATR / Volatility Filters
- `Enable Min OR vs ATR` - Require minimum OR width
- `ATR Length` - Period for ATR calculation (default: 14)
- `Min OR Width = ATR x` - Minimum OR as ATR multiple (default: 0.5)
- `Skip if OR too wide` - Filter excessive volatility
- `Max OR Width = ATR x` - Maximum OR as ATR multiple (default: 1.5)

### Stops / Targets / Partials
- `Base TP % of OR` - Take profit as % of OR width (default: 100%)
- `Base SL % of OR` - Stop loss as % of OR width (default: 50%)
- `Use Partial Take Profit + Runner` - Enable split exits
- `TP1 at R-multiple` - First target in R (default: 1.0)
- `TP1 Qty %` - Position % to exit at TP1 (default: 50%)
- `Runner ATR Trail (x ATR)` - Trail distance for runner (default: 1.5)
- `Activate Runner Trail at R` - R-level to start trailing (default: 0.75)

### Breakeven / Risk Caps
- `Enable Breakeven Stop` - Move stop to entry after profit threshold
- `BE Trigger % of OR` - Profit % to trigger BE (default: 75%)
- `Max Loss per Trade ($)` - Optional dollar-based loss cap

### Backtest
- `Auto backtest last N days` - Use rolling backtest window
- `Backtest Days (N)` - Number of days for auto backtest (default: 30)
- `Backtest Start/End` - Manual date range if auto disabled

---

## Visual Elements

The strategy plots:
- **OR High/Low/Mid** - Gray horizontal lines
- **VWAP** - Yellow line
- **EMA** - Blue line
- **HTF EMA** - Purple line
- **Stop Loss Levels** - Red lines
- **TP/SL Labels** - Green/Red labels on exits
- **Session Background** - Red tint outside trading windows

---

## Alerts

When `Enable Alerts` is on, the strategy sends alerts for:
- Long/Short Entry
- TP1 Filled (partial exit)
- Runner Stop Hit
- Full TP/SL
- VWAP Invalidation Exit
- Breakeven Triggered
- 4 PM Flat (EOD exit)

All alerts include a unique ID for webhook integration.

---

## Usage

1. Open TradingView and go to **Pine Editor**
2. Create a new script and paste contents of `ORB_Pro.pine`
3. Add to chart (recommended: 1-5 minute timeframe)
4. Configure inputs in strategy settings
5. Backtest and optimize for your instrument

### Recommended Instruments
- ES / MES (S&P 500 Futures)
- NQ / MNQ (Nasdaq Futures)
- SPY / QQQ (ETFs)
- High-volume stocks with clean opens

---

## Files

| File | Description |
|------|-------------|
| `ORB_Pro.pine` | Main strategy source code |
| `tools/analyze_backtest.py` | Python backtest analysis tool |
| `LICENSE` | MIT License |

---

## Risk Disclaimer

This strategy is for educational purposes only. Past performance does not guarantee future results. Always backtest thoroughly and use proper risk management. Trade at your own risk.

---

## License

Distributed under the MIT License. See `LICENSE` for details.

---

## Other Strategies in This Repository

| Strategy | Description |
|----------|-------------|
| `EMA Trend Surfer.pine` | EMA pullback strategy with chop/sideways filters |
| `MES_MNQ_DualTF_EMA_Strategy.pine` | Dual timeframe EMA crossover |
| `Mean reversion scalper corrected.pine` | Mean reversion scalping |
| `Trend Surfer.pine` | Trend following strategy |

---

Contributions, issues, and feature requests are welcome.
