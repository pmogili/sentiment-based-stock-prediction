from pathlib import Path
import sys

import numpy as np
import pandas as pd
from flask import Flask, jsonify, request, send_from_directory
from flask_cors import CORS

ROOT = Path(__file__).resolve().parents[1]
FRONTEND_DIR = ROOT / "frontend"
FRONTEND_DIR_STR = str(FRONTEND_DIR)
if str(ROOT) not in sys.path:
    sys.path.insert(0, str(ROOT))

from stock_time_series_sentiment import analyze_stock, sentiment_label


app = Flask(__name__)
CORS(app)


@app.get("/health")
def health() -> tuple[dict, int]:
    return {"status": "ok"}, 200


@app.get("/")
def serve_index():
    """Serve dashboard so http://localhost:5000/ is not 404."""
    return send_from_directory(FRONTEND_DIR_STR, "index.html")


@app.get("/main.js")
def serve_main_js():
    return send_from_directory(
        FRONTEND_DIR_STR, "main.js", mimetype="application/javascript"
    )


@app.get("/styles.css")
def serve_styles():
    return send_from_directory(FRONTEND_DIR_STR, "styles.css", mimetype="text/css")


@app.get("/api/analyze")
def analyze() -> tuple[dict, int]:
    ticker = request.args.get("ticker", "AAPL").strip().upper()
    period = request.args.get("period", "1y").strip()
    interval = request.args.get("interval", "1d").strip()

    try:
        result, df, headlines = analyze_stock(ticker, period, interval)
    except Exception as exc:
        return {"error": str(exc)}, 400

    close = df["Close"]
    if isinstance(close, pd.DataFrame):
        close = close.iloc[:, 0]
    close_vals = np.asarray(close, dtype=float).ravel()
    payload = {
        "ticker": result.ticker,
        "trend_slope": result.trend_slope,
        "annualized_volatility": result.annualized_volatility,
        "max_drawdown": result.max_drawdown,
        "sentiment_score": result.sentiment_score,
        "sentiment_label": sentiment_label(result.sentiment_score, result.headlines_used),
        "headlines_used": result.headlines_used,
        "headlines": headlines[:10],
        "series": {
            "dates": [d.strftime("%Y-%m-%d") for d in close.index],
            "close": close_vals.tolist(),
        },
    }
    return jsonify(payload), 200


if __name__ == "__main__":
    app.run(host="0.0.0.0", port=5000, debug=True)
