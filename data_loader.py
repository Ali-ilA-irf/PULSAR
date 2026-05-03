# ============================================================
#  File    : data_loader.py
#
#  All other members import fetch_stock_data() from here.
#
#  Column names (exact, do not change):
#    Date, Open, High, Low, Close, Volume,
#    Daily Return (%), Volatility (Rolling Std)
# ============================================================

import pandas as pd
import numpy as np
import yfinance as yf
import streamlit as st

# ─────────────────────────────────────────────────────────────
#  CONSTANTS
# ─────────────────────────────────────────────────────────────

TICKERS = ['AAPL', 'TSLA', 'JNJ']
START   = '2021-01-01'
END     = '2024-12-31'

# ─────────────────────────────────────────────────────────────
#  HELPER : compute_derived()
#  Adds Daily Return (%) and Volatility (Rolling Std) columns.
#  Called by both fetch_stock_data() and process_uploaded_data().
# ─────────────────────────────────────────────────────────────

def compute_derived(df: pd.DataFrame) -> pd.DataFrame:
    df = df.copy()
    df['Date'] = pd.to_datetime(df['Date'])
    df.sort_values('Date', inplace=True)
    df.reset_index(drop=True, inplace=True)

    if 'Daily Return (%)' not in df.columns:
        df['Daily Return (%)'] = df['Close'].pct_change() * 100

    if 'Volatility (Rolling Std)' not in df.columns:
        df['Volatility (Rolling Std)'] = (
            df['Daily Return (%)'].rolling(30).std()
        )

    return df

# ─────────────────────────────────────────────────────────────
#  FUNCTION 1 : fetch_stock_data()
#  Downloads AAPL, TSLA, JNJ from Yahoo Finance.
#  Returns dict: { 'AAPL': df, 'TSLA': df, 'JNJ': df }
#  Cached so the app doesn't re-download on every rerun.
# ─────────────────────────────────────────────────────────────

@st.cache_data
def fetch_stock_data() -> dict:
    data_dict = {}

    for ticker in TICKERS:
        try:
            # Download from Yahoo Finance
            df = yf.download(
                ticker,
                start=START,
                end=END,
                auto_adjust=True,
                progress=False
            )

            # yf.download() returns MultiIndex like ('Close', 'AAPL')
            # This flattens it to just 'Close'
            if isinstance(df.columns, pd.MultiIndex):
                df.columns = df.columns.get_level_values(0)

            # Drop Adj Close if still present
            df.drop(columns=['Adj Close'], inplace=True, errors='ignore')

            # Make Date a regular column (it starts as the index)
            df.reset_index(inplace=True)

            # Add derived columns
            df = compute_derived(df)

            data_dict[ticker] = df

        except Exception as e:
            # Fallback: warn and try loading local CSV
            st.warning(f"Could not fetch {ticker}: {e}. Loading local fallback.")
            try:
                df = pd.read_csv(f"{ticker}.csv")
                df = compute_derived(df)
                data_dict[ticker] = df
            except Exception:
                st.error(f"No local fallback found for {ticker}.")

    return data_dict

# ─────────────────────────────────────────────────────────────
#  FUNCTION 2 : process_uploaded_data()
#  Handles user-uploaded CSV files from the sidebar.
#  Returns dict: { 'TICKER': df } ready to merge into data_dict
# ─────────────────────────────────────────────────────────────

def process_uploaded_data(uploaded_file) -> dict:
    try:
        df = pd.read_csv(uploaded_file)
    except Exception as e:
        st.error(f"Could not read file: {e}")
        return {}

    # Strip whitespace from column names
    df.columns = [c.strip() for c in df.columns]

    # Check required columns exist
    required = ['Date', 'Open', 'High', 'Low', 'Close', 'Volume']
    missing = [c for c in required if c not in df.columns]
    if missing:
        st.error(f"Uploaded file missing columns: {missing}")
        return {}

    # Add derived columns if not present
    if 'Daily Return (%)' not in df.columns:
        df['Daily Return (%)'] = df['Close'].pct_change() * 100

    if 'Volatility (Rolling Std)' not in df.columns:
        df['Volatility (Rolling Std)'] = (
            df['Daily Return (%)'].rolling(30).std()
        )

    ticker = uploaded_file.name.replace('.csv', '').upper()

    return {ticker: df}


if __name__ == "__main__":

    all_pass = True

    for ticker in TICKERS:
        print(f"Downloading {ticker}...")
        df = yf.download(ticker, start=START, end=END,
                         auto_adjust=True, progress=False)

        if isinstance(df.columns, pd.MultiIndex):
            df.columns = df.columns.get_level_values(0)

        df.drop(columns=['Adj Close'], inplace=True, errors='ignore')
        df.reset_index(inplace=True)
        df = compute_derived(df)

        checks = {
            "Has Date"                     : "Date" in df.columns,
            "Has Close"                    : "Close" in df.columns,
            "Has Daily Return (%)"         : "Daily Return (%)" in df.columns,
            "Has Volatility (Rolling Std)" : "Volatility (Rolling Std)" in df.columns,
            "No MultiIndex"                : not isinstance(df.columns, pd.MultiIndex),
            "No Adj Close"                 : "Adj Close" not in df.columns,
            "Over 500 rows"                : len(df) > 500,
        }

        print(f"\n-- {ticker} ({len(df)} rows) --")
        for check, result in checks.items():
            icon = "PASS" if result else "FAIL"
            print(f"  [{icon}] {check}")
            if not result:
                all_pass = False

        print(f"  Date range: {df['Date'].min().date()} -> {df['Date'].max().date()}")
        print(f"  Columns: {list(df.columns)}")

    