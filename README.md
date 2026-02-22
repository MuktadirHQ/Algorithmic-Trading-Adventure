# Algorithmic Trading Adventure

Run the moving-average crossover backtest end to end.

## Quickstart (Windows)

1. Open a terminal in this folder.
2. (Optional) Create and activate a virtual environment:
	- `python -m venv venv`
	- `venv\\Scripts\\activate`
3. Install dependencies: `pip install -r requirements.txt`
4. Run the script: `python main.py`
5. When prompted, enter:
	- Stock symbol (e.g., `AAPL`, `MSFT`)
	- Start date `YYYY-MM-DD`
	- End date `YYYY-MM-DD`

## What it does
- Downloads historical prices via `yfinance`.
- Computes 50/200 simple moving averages and trades on golden/death crosses.
- Writes trade results and PnL to a timestamped `trade_results_*.txt` file.

## Troubleshooting
- If you see SSL or network errors, retry later or switch networks.
- To rerun cleanly, delete old `trade_results_*.txt` files if you want fresh outputs only.
