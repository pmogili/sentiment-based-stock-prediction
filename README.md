# Stock Price Time Series + Sentiment Analysis

This project performs:

- Historical stock price time-series analysis
- Trend and volatility metrics
- Maximum drawdown calculation
- News headline sentiment scoring

## Setup

1. Create and activate a virtual environment (optional but recommended).
2. Install dependencies:

```bash
pip install -r requirements.txt
```

## Full Stack App (Frontend + Backend)

### 1) Start backend API

```bash
python backend/app.py
```

Backend runs at `http://localhost:5000`.

### 2) Open the website

With the backend running, open **`http://localhost:5000`** — the API and the dashboard are served together (no 404 on `/`).

**Optional:** serve only the static UI on another port (the page will still call the API on port 5000):

```bash
python -m http.server 5500 -d frontend
```

Then open `http://localhost:5500`.

## Run

```bash
python stock_time_series_sentiment.py --ticker AAPL --period 1y --interval 1d
```

Without chart:

```bash
python stock_time_series_sentiment.py --ticker TSLA --no-plot
```

## Period (days, months, years)

Data comes from Yahoo Finance. The `period` string must be one of their codes, or a custom **last N days** value.

| Kind | Values |
|------|--------|
| **Days** | `1d`, `5d`, or custom `30d`, `90d`, … (any positive integer + `d`) |
| **Months** | `1mo`, `3mo`, `6mo` |
| **Years** | `1y`, `2y`, `5y`, `10y` |
| **Other** | `ytd` (year to date), `max` (all history Yahoo has) |

Examples:

```bash
python stock_time_series_sentiment.py --ticker AAPL --period 6mo
python stock_time_series_sentiment.py --ticker MSFT --period 30d
```

## Arguments

- `--ticker`: stock symbol (default: `AAPL`)
- `--period`: lookback (default: `1y`) — see table above
- `--interval`: bar size, e.g. `1d`, `1wk`, `1h` (default: `1d`)
- `--no-plot`: print-only mode, no chart popup

## Notebook

Open and run:

- `stock_time_series_sentiment.ipynb`

You can change ticker/period/interval in the parameter cell and run all cells.

## Notes

- Data and news are fetched from Yahoo Finance via `yfinance`.
- Sentiment uses VADER compound scores averaged across recent headlines.
- Frontend calls backend endpoint: `GET /api/analyze?ticker=AAPL&period=1y&interval=1d`
