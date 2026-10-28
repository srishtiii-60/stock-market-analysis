"""
Stock Comparison - TCS vs Infosys vs HDFC Bank vs Reliance vs Nifty 50
Outputs (saved in outputs/):
  1. cumulative_returns.png   - kaun aage raha
  2. volatility.png           - kaun zyada risky (annualised volatility)
  3. correlation_heatmap.png  - kaunse stocks saath chalte hain
  4. summary.csv              - saare numbers ek table mein

Run:  python compare_stocks.py
"""

import os
import yfinance as yf
import pandas as pd
import numpy as np
import matplotlib.pyplot as plt

# ---------- Settings ----------
TICKERS = {
    "TCS.NS": "TCS",
    "INFY.NS": "Infosys",
    "HDFCBANK.NS": "HDFC Bank",
    "RELIANCE.NS": "Reliance",
    "^NSEI": "Nifty 50",
}
START_DATE = "2021-01-01"
TRADING_DAYS = 252

os.makedirs("data", exist_ok=True)
os.makedirs("outputs", exist_ok=True)


# ---------- Data ----------
def load_prices() -> pd.DataFrame:
    raw = yf.download(list(TICKERS.keys()), start=START_DATE, progress=False)
    prices = raw["Close"].rename(columns=TICKERS)
    prices = prices.sort_index().dropna()  # sirf wo dates jab sabka data ho
    prices.to_csv("data/comparison_prices.csv")
    return prices


# ---------- Analysis ----------
def build_summary(prices: pd.DataFrame, returns: pd.DataFrame) -> pd.DataFrame:
    years = (prices.index[-1] - prices.index[0]).days / 365.25
    total_return = prices.iloc[-1] / prices.iloc[0] - 1
    cagr = (1 + total_return) ** (1 / years) - 1
    ann_vol = returns.std() * np.sqrt(TRADING_DAYS)
    running_max = prices.cummax()
    max_drawdown = (prices / running_max - 1).min()

    summary = pd.DataFrame(
        {
            "Total Return %": total_return * 100,
            "CAGR %": cagr * 100,
            "Annualised Volatility %": ann_vol * 100,
            "Max Drawdown %": max_drawdown * 100,
        }
    ).round(2)
    return summary.sort_values("Total Return %", ascending=False)


# ---------- Charts ----------
def plot_cumulative(returns: pd.DataFrame) -> None:
    cumulative = (1 + returns).cumprod() - 1
    plt.figure(figsize=(12, 6))
    for col in cumulative.columns:
        lw = 2.5 if col == "Nifty 50" else 1.3
        ls = "--" if col == "Nifty 50" else "-"
        plt.plot(cumulative.index, cumulative[col] * 100, label=col, linewidth=lw, linestyle=ls)
    plt.axhline(0, color="black", linewidth=0.8)
    plt.title("Cumulative Returns since " + START_DATE)
    plt.ylabel("Return %")
    plt.legend()
    plt.grid(alpha=0.3)
    plt.tight_layout()
    plt.savefig("outputs/cumulative_returns.png", dpi=150)
    plt.close()


def plot_volatility(summary: pd.DataFrame) -> None:
    vol = summary["Annualised Volatility %"].sort_values()
    plt.figure(figsize=(9, 5))
    bars = plt.barh(vol.index, vol.values, color="tab:red", alpha=0.75)
    plt.bar_label(bars, fmt="%.1f%%", padding=3)
    plt.title("Annualised Volatility (higher = riskier)")
    plt.xlabel("Volatility %")
    plt.grid(axis="x", alpha=0.3)
    plt.tight_layout()
    plt.savefig("outputs/volatility.png", dpi=150)
    plt.close()


def plot_correlation(returns: pd.DataFrame) -> None:
    corr = returns.corr()
    fig, ax = plt.subplots(figsize=(7, 6))
    im = ax.imshow(corr, cmap="RdYlGn", vmin=-1, vmax=1)
    ax.set_xticks(range(len(corr)))
    ax.set_yticks(range(len(corr)))
    ax.set_xticklabels(corr.columns, rotation=45, ha="right")
    ax.set_yticklabels(corr.columns)
    for i in range(len(corr)):
        for j in range(len(corr)):
            ax.text(j, i, f"{corr.iloc[i, j]:.2f}", ha="center", va="center", fontsize=9)
    ax.set_title("Correlation of Daily Returns")
    fig.colorbar(im)
    plt.tight_layout()
    plt.savefig("outputs/correlation_heatmap.png", dpi=150)
    plt.close()


if __name__ == "__main__":
    prices = load_prices()
    returns = prices.pct_change().dropna()

    summary = build_summary(prices, returns)
    summary.to_csv("outputs/summary.csv")

    print(f"\nPeriod: {prices.index[0].date()} to {prices.index[-1].date()}")
    print("\n===== Summary =====")
    print(summary.to_string())

    plot_cumulative(returns)
    plot_volatility(summary)
    plot_correlation(returns)
    print("\nCharts saved in outputs/ folder.")
