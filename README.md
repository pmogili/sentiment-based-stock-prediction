# 📈 Sentiment-Based Stock Prediction

A machine learning project that combines **stock market time-series data** with **sentiment analysis** to study stock price movements and market sentiment. The project includes a Python-based analysis pipeline, Jupyter Notebook, and a Flask-based web interface for interacting with the analysis.

## 🚀 Project Overview

Traditional stock market analysis primarily relies on historical price and volume data. However, stock prices can also be influenced by public opinion, news, and overall market sentiment.

This project combines:

* 📊 Historical stock market data
* 📰 News headline sentiment analysis
* 🤖 Machine learning and data analysis techniques
* 📈 Time-series analysis
* 📉 Trend, volatility, and maximum drawdown analysis
* 🌐 Flask backend
* 💻 HTML, CSS, and JavaScript frontend

The goal is to analyze the relationship between historical stock-market behaviour and news sentiment and provide an interactive interface for exploring the results.

## 🛠️ Technologies Used

### Machine Learning & Data Analysis

* Python
* Pandas
* NumPy
* Scikit-learn
* Matplotlib
* Seaborn
* Jupyter Notebook

### Sentiment Analysis

* Natural Language Processing (NLP)
* VADER Sentiment Analysis
* Yahoo Finance news data

### Web Application

* Flask
* HTML
* CSS
* JavaScript

## 📂 Project Structure

```text
sentiment-based-stock-prediction/
│
├── backend/
│   └── app.py
│
├── frontend/
│   ├── index.html
│   ├── main.js
│   └── styles.css
│
├── stock_time_series_sentiment.ipynb
├── stock_time_series_sentiment.py
├── requirements.txt
├── .gitignore
└── README.md
```

## 🔄 Workflow

The overall workflow of the project is:

```text
Historical Stock Data
        │
        ▼
Data Collection
        │
        ▼
Data Preprocessing
        │
        ▼
Time-Series Analysis
        │
        ├───────────────┐
        │               │
        ▼               ▼
Stock Features     News Headlines
        │               │
        │               ▼
        │        Sentiment Analysis
        │               │
        └───────┬───────┘
                ▼
       Feature Analysis
                │
                ▼
       Market & Sentiment
             Insights
                │
                ▼
          Web Interface
```

## 📊 Features

* Historical stock price analysis
* Stock trend analysis
* Volatility calculation
* Maximum drawdown calculation
* Time-series data processing
* News headline collection
* Sentiment score calculation
* VADER-based sentiment analysis
* Integration of market and sentiment information
* Interactive web interface
* Flask REST API
* Jupyter Notebook-based analysis

## 💻 Installation

### 1. Clone the repository

```bash
git clone https://github.com/YOUR-USERNAME/sentiment-based-stock-prediction.git
cd sentiment-based-stock-prediction
```

### 2. Create a virtual environment

```bash
python -m venv venv
```

Activate it:

**Windows**

```bash
venv\Scripts\activate
```

**Linux / macOS**

```bash
source venv/bin/activate
```

### 3. Install dependencies

```bash
pip install -r requirements.txt
```

## ▶️ Running the Project

### Run the Python analysis

```bash
python stock_time_series_sentiment.py --ticker AAPL --period 1y --interval 1d
```

For example:

```bash
python stock_time_series_sentiment.py --ticker TSLA --no-plot
```

### Run the Jupyter Notebook

```bash
jupyter notebook stock_time_series_sentiment.ipynb
```

The notebook can be used for interactive data exploration, visualization, and sentiment analysis.

### Run the Flask application

From the project root:

```bash
python backend/app.py
```

The Flask application runs at:

```text
http://localhost:5000
```

Open the following URL in your browser:

```text
http://localhost:5000
```

## 🌐 Frontend

The frontend is located inside:

```text
frontend/
```

It contains:

* `index.html` — Web page structure
* `styles.css` — User interface styling
* `main.js` — Frontend functionality and backend communication

The frontend communicates with the Flask backend through the analysis API.

### API Endpoint

```text
GET /api/analyze?ticker=AAPL&period=1y&interval=1d
```

Example:

```text
http://localhost:5000/api/analyze?ticker=AAPL&period=1y&interval=1d
```

## 📅 Supported Periods

The project retrieves historical stock data through `yfinance`.

| Kind       | Values                         |
| ---------- | ------------------------------ |
| **Days**   | `1d`, `5d`, `30d`, `90d`, etc. |
| **Months** | `1mo`, `3mo`, `6mo`            |
| **Years**  | `1y`, `2y`, `5y`, `10y`        |
| **Other**  | `ytd`, `max`                   |

Examples:

```bash
python stock_time_series_sentiment.py --ticker AAPL --period 6mo
```

```bash
python stock_time_series_sentiment.py --ticker MSFT --period 30d
```

## 📓 Jupyter Notebook

The project includes:

```text
stock_time_series_sentiment.ipynb
```

The notebook provides an interactive environment for:

* Data preprocessing
* Exploratory data analysis
* Time-series analysis
* Trend analysis
* Volatility analysis
* Maximum drawdown calculation
* News headline analysis
* Sentiment analysis
* Data visualization

## 📈 Analysis & Results

The project analyzes historical stock-market behaviour together with recent news sentiment.

Key analysis areas include:

* Historical price movements
* Market trends
* Volatility
* Returns
* Maximum drawdown
* News sentiment
* Average sentiment scores
* Relationship between market behaviour and sentiment

Sentiment scores are calculated using the **VADER sentiment analyzer**.

The VADER compound score ranges approximately from:

```text
-1 → Negative
 0 → Neutral
+1 → Positive
```

## 🔮 Future Improvements

Possible improvements include:

* Integration of real-time stock market APIs
* Real-time news collection
* More advanced NLP models such as BERT
* LSTM/GRU-based time-series prediction
* Transformer-based stock prediction
* Financial-domain sentiment models
* Social-media sentiment analysis
* Technical indicator integration
* Improved feature engineering
* Backtesting
* Real-time prediction dashboard
* Deployment using cloud platforms

## ⚠️ Disclaimer

This project is intended for **educational and research purposes only**.

Stock market analysis and predictions are inherently uncertain. The results generated by this project should **not** be considered financial advice or recommendations to buy or sell securities.

