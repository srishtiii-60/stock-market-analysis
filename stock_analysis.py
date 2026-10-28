"""
Stock Market Trend Analysis - Starter Script
Step 1: data download -> Step 2: cleaning -> Step 3: moving averages,
returns, volatility -> Step 4: chart

Run:  python stock_analysis.py
"""

import os
import yfinance as yf
import pandas as pd
import matplotlib.pyplot as plt

# ---------- Settings (yahan se change kar sakti ho) ----------
TICKER = "TCS.NS"          # try: RELIANCE.NS, INFY.NS, HDFCBANK.NS, ^NSEI, BTC-USD
START_DATE = "2021-01-01"
END_DATE = None            # None = aaj tak

os.makedirs("data", exist_ok=True)
os.makedirs("outputs", exist_ok=True)


# ---------- Step 1: Data download ----------
def load_data(ticker: str) -> pd.DataFrame:
    df = yf.download(ticker, start=START_DATE, end=END_DATE, progress=False)
    if df.empty:
        raise ValueError(f"{ticker} ka data nahi mila. Ticker check karo.")
    # Naye yfinance version mein columns MultiIndex aate hain, usko flat karo
    if isinstance(df.columns, pd.MultiIndex):
        df.columns = df.columns.droplevel(1)
    df.to_csv(f"data/{ticker}.csv")
    return df


# ---------- Step 2: Cleaning ----------
def clean_data(df: pd.DataFrame) -> pd.DataFrame:
    df = df.copy()
    df.index = pd.to_datetime(df.index)
    df = df.sort_index()
    df = df[~df.index.duplicated(keep="first")]
    df = df.dropna(subset=["Close"])
    return df


# ---------- Step 3: Analysis ----------
def add_indicators(df: pd.DataFrame) -> pd.DataFrame:
    df = df.copy()
    df["MA50"] = df["Close"].rolling(50).mean()
    df["MA200"] = df["Close"].rolling(200).mean()
    df["Daily_Return"] = df["Close"].pct_change()
    df["Cumulative_Return"] = (1 + df["Daily_Return"]).cumprod() - 1
    # 30-day rolling volatility (daily returns ka standard deviation)
    df["Volatility_30d"] = df["Daily_Return"].rolling(30).std()
    return df


def print_summary(df: pd.DataFrame, ticker: str) -> None:
    total_return = df["Cumulative_Return"].iloc[-1] * 100
    avg_daily = df["Daily_Return"].mean() * 100
    volatility = df["Daily_Return"].std() * 100
    print(f"\n===== {ticker} Summary =====")
    print(f"Period            : {df.index[0].date()} to {df.index[-1].date()}")
    print(f"Total return      : {total_return:.2f}%")
    print(f"Avg daily return  : {avg_daily:.3f}%")
    print(f"Daily volatility  : {volatility:.3f}%")
    print(f"Highest close     : {df['Close'].max():.2f}")
    print(f"Lowest close      : {df['Close'].min():.2f}")


# ---------- Step 4: Chart ----------
def plot_trend(df: pd.DataFrame, ticker: str) -> None:
    fig, (ax1, ax2) = plt.subplots(
        2, 1, figsize=(12, 8), sharex=True, gridspec_kw={"height_ratios": [3, 1]}
    )

    ax1.plot(df.index, df["Close"], label="Close", linewidth=1.2)
    ax1.plot(df.index, df["MA50"], label="50-day MA", linewidth=1)
    ax1.plot(df.index, df["MA200"], label="200-day MA", linewidth=1)
    ax1.set_title(f"{ticker} - Price & Moving Averages")
    ax1.set_ylabel("Price")
    ax1.legend()
    ax1.grid(alpha=0.3)

    ax2.plot(df.index, df["Volatility_30d"] * 100, color="tab:red", linewidth=1)
    ax2.set_title("30-day Rolling Volatility (%)")
    ax2.set_ylabel("Volatility %")
    ax2.grid(alpha=0.3)

    plt.tight_layout()
    plt.savefig(f"outputs/{ticker}_trend.png", dpi=150)
    plt.show()


if __name__ == "__main__":
    raw = load_data(TICKER)
    data = clean_data(raw)
    data = add_indicators(data)
    print(data.tail())
    print_summary(data, TICKER)
    plot_trend(data, TICKER)
