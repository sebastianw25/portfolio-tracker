"""
Portfolio Tracker
Pulls live prices, calculates value/gain/allocation, prints a summary,
saves a pie chart, and logs a timestamped snapshot to history.csv.
Author: Sebastian Williams
"""

import os
from datetime import date

import yfinance as yf
import pandas as pd
import matplotlib.pyplot as plt


# YOUR HOLDINGS -- edit when you buy/sell. cost_basis = total $ you paid.
HOLDINGS = [
    {"account": "Roth IRA", "ticker": "VOO",  "shares": 5.192, "cost_basis": 3581.51},
    {"account": "Roth IRA", "ticker": "NVDA", "shares": 1.0,   "cost_basis": 208.88},
    {"account": "Roth IRA", "ticker": "QQQM", "shares": 0.688, "cost_basis": 200.52},
    {"account": "Roth IRA", "ticker": "AAPL", "shares": 0.156, "cost_basis": 49.94},
]

HISTORY_FILE = "history.csv"
CHART_FILE = "allocation.png"


def get_price(ticker):
    try:
        t = yf.Ticker(ticker)
        price = t.fast_info.get("lastPrice")
        if price is None:
            price = t.history(period="1d")["Close"].iloc[-1]
        return float(price)
    except Exception as e:
        print(f"  ! Could not fetch {ticker}: {e}")
        return None


def build_portfolio():
    rows = []
    print("Fetching live prices...")
    for h in HOLDINGS:
        price = get_price(h["ticker"])
        if price is None:
            continue
        market_value = h["shares"] * price
        gain_loss = market_value - h["cost_basis"]
        rows.append({
            "Ticker": h["ticker"],
            "Shares": h["shares"],
            "Cost Basis": h["cost_basis"],
            "Price": price,
            "Market Value": market_value,
            "Gain/Loss": gain_loss,
        })
    df = pd.DataFrame(rows)
    total_value = df["Market Value"].sum()
    df["% Allocation"] = df["Market Value"] / total_value * 100
    return df


def print_summary(df):
    total_value = df["Market Value"].sum()
    total_cost = df["Cost Basis"].sum()
    total_gain = df["Gain/Loss"].sum()
    total_gain_pct = total_gain / total_cost * 100 if total_cost else 0

    print("\n" + "=" * 70)
    print(f"{'PORTFOLIO SUMMARY':^70}")
    print(f"{date.today().strftime('%B %d, %Y'):^70}")
    print("=" * 70)
    print(f"{'Ticker':<8}{'Shares':>10}{'Price':>12}{'Value':>14}{'Gain/Loss':>14}{'Alloc':>10}")
    print("-" * 70)
    for _, r in df.iterrows():
        print(f"{r['Ticker']:<8}{r['Shares']:>10.3f}{r['Price']:>12,.2f}{r['Market Value']:>14,.2f}{r['Gain/Loss']:>+14,.2f}{r['% Allocation']:>9.1f}%")
    print("-" * 70)
    print(f"{'TOTAL':<8}{'':<10}{'':<12}{total_value:>14,.2f}{total_gain:>+14,.2f}{100:>9.1f}%")
    print("=" * 70)
    print(f"Total invested: ${total_cost:,.2f}")
    print(f"Total return: {total_gain_pct:+.2f}%")
    print("=" * 70)
    return total_value, total_gain


def save_pie_chart(df):
    plt.figure(figsize=(8, 8))
    plt.pie(df["Market Value"], labels=df["Ticker"], autopct="%1.1f%%",
            startangle=90, counterclock=False)
    plt.title("Portfolio Allocation by Market Value")
    plt.tight_layout()
    plt.savefig(CHART_FILE, dpi=120)
    plt.close()
    print(f"\nSaved chart -> {CHART_FILE}")


def log_history(total_value, total_gain):
    today = date.today().isoformat()
    new_row = pd.DataFrame([{
        "Date": today,
        "Total Value": round(total_value, 2),
        "Total Gain/Loss": round(total_gain, 2),
    }])
    if os.path.exists(HISTORY_FILE):
        hist = pd.read_csv(HISTORY_FILE)
        hist = hist[hist["Date"] != today]
        hist = pd.concat([hist, new_row], ignore_index=True)
    else:
        hist = new_row
    hist.to_csv(HISTORY_FILE, index=False)
    print(f"Logged snapshot -> {HISTORY_FILE} ({len(hist)} entries)")


def main():
    df = build_portfolio()
    if df.empty:
        print("No data fetched -- check your internet connection.")
        return
    total_value, total_gain = print_summary(df)
    save_pie_chart(df)
    log_history(total_value, total_gain)


if __name__ == "__main__":
    main()
