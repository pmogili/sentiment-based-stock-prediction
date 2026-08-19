import argparse
from dataclasses import dataclass
from typing import List, Optional

import matplotlib.pyplot as plt
import numpy as np
import pandas as pd
import yfinance as yf
from sklearn.linear_model import LinearRegression
from vaderSentiment.vaderSentiment import SentimentIntensityAnalyzer


@dataclass
class AnalysisResult:
    ticker: str
    trend_slope: float
    annualized_volatility: float
    max_drawdown: float
    sentiment_score: float
    headlines_used: int


def _flatten_yfinance_columns(df: pd.DataFrame) -> pd.DataFrame:
    """yfinance often returns MultiIndex columns; flatten to Open/High/Low/Close/Volume."""
    if not isinstance(df.columns, pd.MultiIndex):
        return df
    df = df.copy()
    ohlcv = {"Open", "High", "Low", "Close", "Adj Close", "Volume"}
    lvl0 = set(df.columns.get_level_values(0).astype(str))
    lvl1 = set(df.columns.get_level_values(1).astype(str))
    # Drop the level that is the ticker/symbol, keep OHLCV names
    if ohlcv & lvl0 and not (ohlcv & lvl1):
        df.columns = df.columns.droplevel(1)
    elif ohlcv & lvl1 and not (ohlcv & lvl0):
        df.columns = df.columns.droplevel(0)
    else:
        df.columns = df.columns.droplevel(-1)
    return df


# Yahoo Finance `period` values (see yfinance docs). Also: custom "Nd" = last N calendar days.
VALID_YF_PERIODS = frozenset(
    {"1d", "5d", "1mo", "3mo", "6mo", "1y", "2y", "5y", "10y", "ytd", "max"}
)


def parse_period(period: str) -> tuple[Optional[str], Optional[pd.Timestamp], Optional[pd.Timestamp]]:
    """
    Returns either (yfinance_period, None, None) or (None, start, end) for a custom day window.

    Built-in codes (days / months / years):
      - Days: 1d, 5d
      - Months: 1mo, 3mo, 6mo
      - Years: 1y, 2y, 5y, 10y
      - Other: ytd, max
    Custom: "30d", "90d" = last N calendar days (uses start/end instead of period).
    """
    p = period.strip().lower()
    if not p:
        raise ValueError("period must not be empty.")
    if p in VALID_YF_PERIODS:
        return p, None, None
    if p.endswith("d") and p[:-1].isdigit():
        n = int(p[:-1])
        if n <= 0:
            raise ValueError(f"Invalid day window '{period}': N must be positive.")
        end = pd.Timestamp.now().normalize() + pd.Timedelta(days=1)
        start = end - pd.Timedelta(days=n)
        return None, start, end
    raise ValueError(
        f"Unknown period '{period}'. "
        f"Use one of: {', '.join(sorted(VALID_YF_PERIODS))} or e.g. 30d, 90d for last N days."
    )


def _scalar_float(val) -> float:
    """Coerce pandas Series/ndarray of size 1 or numpy scalar to Python float."""
    if isinstance(val, pd.Series):
        return float(val.iloc[0]) if len(val) == 1 else float(val.mean())
    arr = np.asarray(val).squeeze()
    if arr.ndim == 0:
        return float(arr)
    if arr.size == 1:
        return float(arr.flat[0])
    raise TypeError(f"Expected a scalar, got shape {getattr(arr, 'shape', None)}")


def download_prices(ticker: str, period: str = "1y", interval: str = "1d") -> pd.DataFrame:
    per, start, end = parse_period(period)
    if per is not None:
        data = yf.download(ticker, period=per, interval=interval, auto_adjust=True, progress=False)
    else:
        data = yf.download(
            ticker, start=start, end=end, interval=interval, auto_adjust=True, progress=False
        )
    if data.empty:
        raise ValueError(f"No price data found for ticker '{ticker}'.")
    data = _flatten_yfinance_columns(data)
    cols = ["Open", "High", "Low", "Close", "Volume"]
    missing = [c for c in cols if c not in data.columns]
    if missing:
        raise ValueError(f"Unexpected columns from yfinance: missing {missing}. Got: {list(data.columns)}")
    data = data[cols].dropna()
    return data


def compute_time_series_metrics(df: pd.DataFrame) -> tuple[float, float, float]:
    close = df["Close"].copy()
    # If Close is still 2D (duplicate columns), take first column as Series
    if isinstance(close, pd.DataFrame):
        close = close.iloc[:, 0]
    returns = close.pct_change().dropna()
    if isinstance(returns, pd.DataFrame):
        returns = returns.iloc[:, 0]

    x = np.arange(len(close)).reshape(-1, 1)
    y = np.asarray(close, dtype=float).reshape(-1, 1)
    model = LinearRegression()
    model.fit(x, y)
    trend_slope = float(model.coef_[0][0])

    vol_raw = returns.std() * np.sqrt(252)
    annualized_volatility = _scalar_float(vol_raw)

    rolling_max = close.cummax()
    drawdown = (close - rolling_max) / rolling_max
    max_drawdown = _scalar_float(drawdown.min())

    return trend_slope, annualized_volatility, max_drawdown


def _title_from_news_item(item: object) -> Optional[str]:
    """Yahoo news JSON varies: top-level 'title' or nested content.title / content.summary."""
    if not isinstance(item, dict):
        return None
    t = item.get("title")
    if isinstance(t, str) and t.strip():
        return t.strip()
    content = item.get("content")
    if isinstance(content, dict):
        for key in ("title", "summary", "description"):
            val = content.get(key)
            if isinstance(val, str) and val.strip():
                return val.strip()
    return None


def extract_headlines_from_yfinance_news(news_items: List[dict], max_items: int = 20) -> List[str]:
    headlines: List[str] = []
    for item in news_items[:max_items]:
        title = _title_from_news_item(item)
        if title:
            headlines.append(title)
    return headlines


def score_sentiment(headlines: List[str]) -> float:
    if not headlines:
        return 0.0
    analyzer = SentimentIntensityAnalyzer()
    scores = [analyzer.polarity_scores(h)["compound"] for h in headlines]
    return float(np.mean(scores))


def sentiment_label(score: float, headlines_used: Optional[int] = None) -> str:
    if headlines_used is not None and headlines_used == 0:
        return "No news data"
    if score >= 0.1:
        return "Positive"
    if score <= -0.1:
        return "Negative"
    return "Neutral"


def analyze_stock(ticker: str, period: str, interval: str) -> tuple[AnalysisResult, pd.DataFrame, List[str]]:
    ticker = ticker.upper().strip()
    df = download_prices(ticker, period=period, interval=interval)
    trend_slope, annualized_volatility, max_drawdown = compute_time_series_metrics(df)

    tk = yf.Ticker(ticker)
    raw_news: Optional[List[dict]] = getattr(tk, "news", None)
    headlines = extract_headlines_from_yfinance_news(raw_news or [])
    sentiment = score_sentiment(headlines)

    result = AnalysisResult(
        ticker=ticker,
        trend_slope=trend_slope,
        annualized_volatility=annualized_volatility,
        max_drawdown=max_drawdown,
        sentiment_score=sentiment,
        headlines_used=len(headlines),
    )
    return result, df, headlines


def plot_prices(df: pd.DataFrame, ticker: str) -> None:
    close = df["Close"]
    ma20 = close.rolling(20).mean()
    ma50 = close.rolling(50).mean()

    plt.figure(figsize=(11, 6))
    plt.plot(close.index, close.values, label="Close", linewidth=1.8)
    plt.plot(ma20.index, ma20.values, label="MA20", linewidth=1.2)
    plt.plot(ma50.index, ma50.values, label="MA50", linewidth=1.2)
    plt.title(f"{ticker} Price Time Series")
    plt.xlabel("Date")
    plt.ylabel("Price")
    plt.legend()
    plt.tight_layout()
    plt.show()


def print_report(result: AnalysisResult, headlines: List[str]) -> None:
    print("\n=== Stock Price Time Series + Sentiment Analysis ===")
    print(f"Ticker: {result.ticker}")
    print(f"Trend slope (price units/day): {result.trend_slope:.4f}")
    print(f"Annualized volatility: {result.annualized_volatility:.2%}")
    print(f"Max drawdown: {result.max_drawdown:.2%}")
    print(
        f"Sentiment score: {result.sentiment_score:.3f} "
        f"({sentiment_label(result.sentiment_score, result.headlines_used)})"
    )
    print(f"Headlines used: {result.headlines_used}")
    if headlines:
        print("\nSample headlines:")
        for idx, headline in enumerate(headlines[:5], start=1):
            print(f"{idx}. {headline}")


def parse_args() -> argparse.Namespace:
    parser = argparse.ArgumentParser(
        description="Stock Price Time Series Analysis with Sentiment Analysis"
    )
    parser.add_argument("--ticker", type=str, default="AAPL", help="Stock ticker (e.g., AAPL)")
    parser.add_argument(
        "--period",
        type=str,
        default="1y",
        help=(
            "Lookback: Yahoo codes 1d,5d,1mo,3mo,6mo,1y,2y,5y,10y,ytd,max — or custom Nd e.g. 30d,90d"
        ),
    )
    parser.add_argument("--interval", type=str, default="1d", help="Data interval (e.g., 1d, 1wk)")
    parser.add_argument(
        "--no-plot",
        action="store_true",
        help="Disable plotting and print metrics only.",
    )
    return parser.parse_args()


def main() -> None:
    args = parse_args()
    result, df, headlines = analyze_stock(args.ticker, args.period, args.interval)
    print_report(result, headlines)
    if not args.no_plot:
        plot_prices(df, result.ticker)


if __name__ == "__main__":
    main()
