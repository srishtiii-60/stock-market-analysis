# Stock Market Trend Analysis

Python project to analyse stock and crypto price trends using `yfinance` and Pandas.

> Educational analysis only. This is not investment advice.

## Features
- Downloads historical price data (NSE stocks, Nifty 50, crypto)
- Data cleaning (duplicates, missing values, sorting)
- 50-day and 200-day moving averages
- Daily and cumulative returns
- 30-day rolling volatility
- Trend chart saved to `outputs/`

## Tech Stack
Python, Pandas, yfinance, Matplotlib

## How to Run
```bash
pip install -r requirements.txt
python stock_analysis.py
```
Change `TICKER` in `stock_analysis.py` (e.g. `RELIANCE.NS`, `INFY.NS`, `^NSEI`, `BTC-USD`).

## Project Structure
```
stock-market-analysis/
├── data/            # downloaded CSVs
├── notebooks/       # exploration notebooks
├── outputs/         # saved charts
├── stock_analysis.py
├── requirements.txt
└── README.md
```

## Key Insights
_Add 4-5 insights from your own analysis here (e.g. which sector was less volatile, stock vs Nifty returns)._

## Next Steps
- [ ] Compare multiple stocks
- [ ] Correlation heatmap
- [ ] Streamlit dashboard
- [ ] Moving average crossover backtest
