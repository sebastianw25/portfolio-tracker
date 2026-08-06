# Portfolio Tracker

A Python script that pulls live stock/ETF prices, calculates market value,
gain/loss, and allocation for a personal investment portfolio, prints a clean
summary, generates an allocation pie chart, and logs a timestamped snapshot to
`history.csv` so growth can be tracked over time.

## Features
- Live price fetching via the `yfinance` API
- Market value, gain/loss, and percentage-return calculations with `pandas`
- Allocation pie chart output with `matplotlib`
- Historical snapshot logging to CSV (one entry per day, growth tracking over time)
- Graceful error handling if a ticker or the network fails

## Tech Stack
Python · yfinance · pandas · matplotlib

## Setup
```bash
pip install yfinance pandas matplotlib
```

## Usage
Edit the `HOLDINGS` list at the top of `portfolio_tracker.py` with your own
positions (ticker, shares, and total cost basis), then run:

```bash
python portfolio_tracker.py
```

## Output
- A formatted summary table in the terminal
- `allocation.png` — a pie chart of holdings by market value
- `history.csv` — a running log of total value and gain/loss over time

## Notes
Prices are delayed and provided for personal tracking, not real-time trading.
