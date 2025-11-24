<!-- .github/copilot-instructions.md for pinescript-strategies -->
# Copilot / AI Agent Instructions — pinescript-strategies

Purpose: help an AI editing agent be productive working with Pine Script strategy files and small local tooling in this repository.

What this repo is: a collection of TradingView Pine Script v5 strategies and a tiny analysis tool.
- Primary scripts: top-level `*.pine` files (e.g. `ORB_Pro_Refactored_FIXED.pine`, `MES_MNQ_DualTF_EMA_Strategy.pine`).
- Backtest helper: `tools/analyze_backtest.py` — simple CSV analyzer using `pandas`/`numpy`.

Big picture (how things are expected to flow)
- Author edits Pine scripts locally and copies/pastes them into TradingView Pine Editor for testing and backtesting.
- TradingView strategy tester produces CSV (or strategy export) that can be post-processed by `tools/analyze_backtest.py`.
- There is no CI/build for Pine scripts — TradingView is the runtime.

Key files to reference
- `README.md` — describes `ORB_Pro_Refactored_FIXED.pine` usage and backtest inputs.
- `tools/analyze_backtest.py` — run examples and dependency notes are embedded in the script's header.
- Top-level `*.pine` files — treat them as the canonical sources. Look for inputs like `backtestAuto`, `Backtest Days`, `Backtest Start/End`, `Enable Alerts`.

Repository-specific conventions and patterns
- Pine version: all scripts target Pine Script v5. Keep generated code compatible with v5 syntax (e.g. `strategy.*`, `input.*`, `ta.*`).
- Backtest window: scripts implement both auto (`backtestAuto`/`backtestDays`) and manual (`Backtest Start`, `Backtest End`) backtest ranges — preserve and prefer existing input names when modifying logic.
- Alerts: scripts expose an `Enable Alerts` toggle. When adding or changing alert text, keep messages concise and consistent with existing alert names (entry, TP1, runner SL, breakeven, daily flat).
- File editing workflow: do not attempt to run Pine scripts locally — they must be pasted into TradingView for execution and visual verification.

Developer workflows and useful commands (explicit)
- Running the backtest analyzer (macOS / zsh):
  - Create a Python venv and install dependencies:
    ```bash
    python3 -m venv .venv
    source .venv/bin/activate
    pip install pandas numpy
    ```
  - Analyze an exported TradingView CSV:
    ```bash
    python3 tools/analyze_backtest.py /path/to/export.csv
    # If analyzer fails to auto-detect profit, pass explicit column name
    python3 tools/analyze_backtest.py /path/to/export.csv --profit-col "Profit"
    ```

-- Pine script workflow (manual):
  - Open TradingView -> Pine Editor
  - Create new script -> paste contents of `<file>.pine`
  - Add to chart, configure inputs (notably backtest window & timeframe)
  - Use Strategy Tester -> Export trades to CSV -> analyze with `tools/analyze_backtest.py`

Patterns for safe edits
- Preserve input names and default behavior: many users rely on input names like `backtestAuto`, `Backtest Days`, `Enable Alerts`.
- Keep default backtest behavior intact (auto last-N-days) unless the user explicitly asks to change it.
- When refactoring a strategy, limit scope to a single file unless the change is obviously cross-cutting.
- When changing alert text or input defaults, update `README.md` if usage changes.

Integration points and external dependencies
- TradingView (manual) — the runtime for Pine scripts and source of CSV exports.
- Python libs for analyzer: `pandas`, `numpy` (installed via `pip`). No lockfile present — keep dependencies minimal.

Examples to copy/paste for quick checks
- Detect profit column hint from analyzer header: it tries columns like `Profit`, `PnL`, `net profit`, `profit_usd`, `pl`, `realized`.
- Analyzer usage example:
  `python3 tools/analyze_backtest.py exports/ORB_export.csv --profit-col "Profit"`

When to ask the repo owner
- If a Pine script appears to target a different Pine version than v5.
- If changes require automated exports or CI (this repo is currently manual; adding CI should be coordinated).
- If you plan to add dependency-managed tooling (e.g., requirements.txt) — ask whether to commit it.

Editing etiquette for AI agents
- Make minimal, focused edits. For Pine scripts, prefer small PRs that change one behavioral aspect at a time.
- Add short descriptions in PR titles referencing the strategy filename (e.g., `ORB: adjust ATR filter default`) and update `README.md` only for user-visible changes.
- Do not attempt to run or validate Pine logic locally. Instead, provide clear instructions and tests the human can run in TradingView.

Next steps after edits
- Tell the user to paste the updated `.pine` into TradingView and provide a sample exported CSV if they want a full verification run.

Feedback
- If anything above is incorrect or missing (tooling, files, conventions), tell me what to change and I will update this file.
