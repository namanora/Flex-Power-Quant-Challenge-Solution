# FlexPower Quant Challenge Solutions

This repository contains my solutions to the FlexPower Quant Challenge, organized into two main parts:

- **Task 1**: Minimal reporting tool and API for trade PnL using a SQLite database.  
- **Task 2**: Data analysis of German power market forecasts and prices, and development of a trading strategy.

---

## File Structure

├── AA_Solution_1.ipynb # Task 1: exploratory notebook (compute volumes, PnL functions) 

├── AA_Solution_1.py # Task 1: Python module (with compute_pnl) used by Flask API 

├── AA_Solution_2.ipynb # Task 2: analysis notebook (visualizations, strategy backtests) 

├── app.py # Flask application exposing /v1/pnl/<strategy_id> 

├── trades.sqlite # Sample trades database for Task 1 

├── analysis_task_data.xlsx # Time‑series data for Task 2 

├── requirements.txt # Python dependencies 

└── README.md # This file

## Requirements

Create and activate a Python 3 virtual environment, then install:

```bash
pip install -r requirements.txt
```
## Task 1: Minimal Reporting Tool & API

### 1.1. Total Buy/Sell Volume

#### Functions in AA_Solution_1.py:

compute_total_buy_volume()

compute_total_sell_volume()

Connect to trades.sqlite, query the epex_12_20_12_13 table, return total buy/sell volumes.

### 1.2. Strategy PnL Calculation

Function compute_pnl(strategy_id: str) -> float in AA_Solution_1.py

Sums quantity * price for side='sell' and -quantity * price for side='buy'.

Returns 0.0 if no trades for the given strategy.

### 1.3 Flask API

The Flask app in app.py serves PnL routes on localhost:5000.

#### 1. Start the Server

```bash
python app.py
```
It listens on http://127.0.0.1:5000/.

#### 2. Query the endpoint

```bash
GET http://localhost:5000/v1/pnl/<strategy_id>
```
Repsonse:
```bash
{
  "strategy": "my_strategy",
  "value": 12345.67,
  "unit": "euro",
  "capture_time": "2025-04-22T12:34:00Z"
}
```

## Task 2: Data Analysis & Trading Strategy

### Overview

We analyze German day‑ahead vs intraday forecasts and prices for wind and PV, then build:

Battery Arbitrage Benchmarks

Greedy “best‑pair” forward-scan.

Fixed‑hour seasonal strategy (winter vs summer hours).

24‑Hour Spread Regression Strategy

Use 24 separate Random Forest regressors (one per hour).

Rolling‑window backtest: train on past months, test on the next.

### Setup

1. Load analysis_task_data.xlsx into pandas.

2. Filter to “top‑of‑hour” rows (minute == 0).

3. Extract calendar flags, compute deltas, spreads, lagged and rolling features.

4. Assemble feature matrix X and target y (intraday – day‑ahead spread).

### Key Features

Day‑Ahead Forecasts
– Wind Day Ahead Forecast, PV Day Ahead Forecast.

Lagged DA Forecasts
– 24 h lag + rolling mean/std.

Lagged Forecast Errors (“Deltas”)
– intraday – day‑ahead differences for past 1–4 days.

Lagged Price Spreads
– past 1–4 day intraday – day‑ahead gaps.

Rolling Spread Stats
– mean/std over past 24 h & 168 h.

Rolling Delta Stats
– mean/std of forecast errors over past 24 h.

Calendar Flags
– is_holiday, weekday, is_weekend, month.

All features are known at d – 1 12:00.

### Model Selection

Use January subset for speed.

Sweep n_estimators ∈ [10,25,…,1000] with OOB R² → choose 400 trees at the elbow.

Plot OOB error vs. n_estimators to confirm diminishing returns.

### Backtest Results

Fixed‑Hour Benchmark (always trade at hour 23) → ≈ €120 000 (uses hindsight).

Spread Regression Strategy → ≈ €97 234 total PnL in 2021.

Cumulative PnL rose steadily after initial months (rolling-window).

October saw a large single-day drawdown (~ –€15 000), highlighting tail risk.

Production‐grade would require drawdown limits or ensemble filters.

## How to Reproduce

### 1. Install dependencies:

```bash
pip install -r requirements.txt
```

### 2. Run

app.py for Task 1 API (see above).

### 3. Open 

and execute AA_Solution_1.ipynb & AA_Solution_2.ipynb in Jupyter to explore data, plots, and backtests.

## Thank you for reviewing! I look forward to your feedback.