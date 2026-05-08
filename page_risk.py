# page_risk.py — Risk Comparator
# Author: Maryam Zahid (24F-0658)
# Module Contract: render(data_dict: dict)
# data_dict keys: 'AAPL', 'TSLA', 'JNJ'
# DataFrame cols: Date, Open, High, Low, Close, Volume,
#                 Daily Return (%), Volatility (Rolling Std)
#
# NOTE: data_loader.py stores 'Daily Return (%)' already in % units
#       e.g.  1.5 means +1.5%,  -2.0 means -2.0%
#       All ratio calculations below work in % space; final display is also %.

import streamlit as st
import pandas as pd
import numpy as np
import plotly.express as px
import plotly.graph_objects as go
from scipy import stats
from data_loader import fetch_stock_data


# Risk-free rate assumption (annualized, e.g., 3-month US T-Bill ~5% in 2023–24)
# Expressed in % to match data_loader units: 5% p.a. → 0.0198% per day
RISK_FREE_RATE_ANNUAL_PCT = 5.0          # 5 %
RISK_FREE_DAILY_PCT = RISK_FREE_RATE_ANNUAL_PCT / 252   # ~0.0198 %


def _compute_risk_metrics(ticker: str, df: pd.DataFrame) -> dict:
    """Compute all risk metrics for one ticker.

    data_loader guarantees 'Daily Return (%)' is already in % units
    (e.g. 1.5 means +1.5%).  All arithmetic stays in % space;
    annualisation factors are applied without any unit conversion.
    """
    r = df["Daily Return (%)"].dropna()   # already in %, e.g. 1.5 = 1.5%

    mean_r = r.mean()     # mean daily return (%)
    std_r  = r.std()      # daily std dev (%)

    # Annualized figures (still in % since we stay in % space)
    ann_vol = std_r * np.sqrt(252)
    sharpe  = (mean_r - RISK_FREE_DAILY_PCT) / std_r * np.sqrt(252) if std_r != 0 else 0

    # Sortino Ratio — penalises only returns below the risk-free daily rate
    downside     = r[r < RISK_FREE_DAILY_PCT]
    downside_std = downside.std() if len(downside) > 0 else 0
    sortino      = (mean_r - RISK_FREE_DAILY_PCT) / downside_std * np.sqrt(252) if downside_std != 0 else 0

    # Value-at-Risk — parametric normal, result already in % units
    var_95 = stats.norm.ppf(0.05, mean_r, std_r)   # e.g. -1.8 means -1.8%
    var_99 = stats.norm.ppf(0.01, mean_r, std_r)

    # Maximum Drawdown from Close prices
    close        = df["Close"].dropna()
    roll_max     = close.cummax()
    drawdown     = (close - roll_max) / roll_max
    max_drawdown = drawdown.min() * 100   # convert fraction → %

    return {
        "Ticker":                   ticker,
        "Avg Daily Return (%)": round(mean_r,      4),
        "Annualized Volatility (%)": round(ann_vol, 4),
        "Sharpe Ratio":             round(sharpe,   4),
        "Sortino Ratio":            round(sortino,  4),
        "VaR 95% (daily %)": round(var_95,   4),
        "VaR 99% (daily %)": round(var_99,   4),
        "Max Drawdown (%)": round(max_drawdown, 4),
        "Max Gain (%)": round(r.max(), 4),
        "Max Loss (%)": round(r.min(), 4),
    }


def render(data_dict: dict):
    st.title("Risk Comparator")
    st.caption(
        "Side-by-side risk and volatility comparison across AAPL, TSLA, and JNJ — "
        "including Sharpe Ratio, Sortino Ratio, Value-at-Risk, and Maximum Drawdown."
    )

    # ── Build metrics table ──────────────────────
    rows = [_compute_risk_metrics(ticker, df) for ticker, df in data_dict.items()]
    comp_df = pd.DataFrame(rows)

    max_vol = comp_df["Annualized Volatility (%)"].max()
    min_vol = comp_df["Annualized Volatility (%)"].min()
    max_sharpe = comp_df["Sharpe Ratio"].max()
    min_sharpe = comp_df["Sharpe Ratio"].min()

    # ──────────────────────────────────────────────
    # Section 1 — Risk Summary Table
    # ──────────────────────────────────────────────
    st.subheader("Risk Summary Table")
    st.caption(
        "Highest volatility  |  Lowest volatility  |  "
        f"Risk-free rate assumed: {RISK_FREE_RATE_ANNUAL_PCT:.1f}% p.a."
    )

    def highlight_vol(val):
        if val == max_vol:
            return "background-color: #3d1a1a; color: #f85149; font-weight: bold"
        if val == min_vol:
            return "background-color: #0f2d18; color: #3fb950; font-weight: bold"
        return ""

    def highlight_sharpe(val):
        if val == max_sharpe:
            return "background-color: #0f2d18; color: #3fb950; font-weight: bold"
        if val == min_sharpe:
            return "background-color: #3d1a1a; color: #f85149; font-weight: bold"
        return ""

    display_cols = [
        "Ticker", "Avg Daily Return (%)", "Annualized Volatility (%)",
        "Sharpe Ratio", "Sortino Ratio", "Max Drawdown (%)",
    ]
    styled = (
        comp_df[display_cols]
        .style.map(highlight_vol, subset=["Annualized Volatility (%)"])
        .map(highlight_sharpe, subset=["Sharpe Ratio"])
        .format(
            {
                "Avg Daily Return (%)": "{:.4f}",
                "Annualized Volatility (%)": "{:.4f}",
                "Sharpe Ratio": "{:.4f}",
                "Sortino Ratio": "{:.4f}",
                "Max Drawdown (%)": "{:.4f}",
            }
        )
    )
    st.dataframe(styled, width="stretch", hide_index=True)

    # ──────────────────────────────────────────────
    # Section 2 — Annualized Volatility Bar Chart
    # ──────────────────────────────────────────────
    st.subheader("Annualized Volatility Comparison")
    fig1 = px.bar(
        comp_df,
        x="Ticker",
        y="Annualized Volatility (%)",
        color="Ticker",
        template="plotly_dark",
        color_discrete_sequence=["#58a6ff", "#f0883e", "#3fb950"],
        text_auto=".2f",
    )
    fig1.update_traces(textposition="outside")
    fig1.update_layout(showlegend=False, yaxis_title="Annualized Volatility (%)")
    st.plotly_chart(fig1, width="stretch")

    # ──────────────────────────────────────────────
    # Section 3 — Risk vs Return Scatter
    # ──────────────────────────────────────────────
    st.subheader("Risk vs Return Scatter")
    fig2 = px.scatter(
        comp_df,
        x="Annualized Volatility (%)",
        y="Avg Daily Return (%)",
        text="Ticker",
        color="Ticker",
        template="plotly_dark",
        color_discrete_sequence=["#58a6ff", "#f0883e", "#3fb950"],
    )
    fig2.update_traces(textposition="top center", marker=dict(size=16))
    fig2.update_layout(showlegend=False)
    st.plotly_chart(fig2, width="stretch")

    # ──────────────────────────────────────────────
    # Section 4 — Sharpe & Sortino Ratio Grouped Bar
    # ──────────────────────────────────────────────
    st.subheader("Sharpe Ratio vs Sortino Ratio")
    st.caption(
        "Higher is better. Sharpe penalises all volatility; "
        "Sortino only penalises downside volatility."
    )
    ratio_fig = go.Figure()
    tickers = comp_df["Ticker"].tolist()
    ratio_fig.add_trace(
        go.Bar(
            name="Sharpe Ratio",
            x=tickers,
            y=comp_df["Sharpe Ratio"].tolist(),
            marker_color="#58a6ff",
            text=[f"{v:.3f}" for v in comp_df["Sharpe Ratio"]],
            textposition="outside",
        )
    )
    ratio_fig.add_trace(
        go.Bar(
            name="Sortino Ratio",
            x=tickers,
            y=comp_df["Sortino Ratio"].tolist(),
            marker_color="#3fb950",
            text=[f"{v:.3f}" for v in comp_df["Sortino Ratio"]],
            textposition="outside",
        )
    )
    ratio_fig.add_hline(y=0, line_color="gray", line_dash="dot")
    ratio_fig.update_layout(
        template="plotly_dark",
        barmode="group",
        title="Risk-Adjusted Return Ratios",
        yaxis_title="Ratio",
    )
    st.plotly_chart(ratio_fig, width="stretch")

    # ──────────────────────────────────────────────
    # Section 5 — Value-at-Risk Table
    # ──────────────────────────────────────────────
    st.subheader("Value-at-Risk (VaR) Summary")
    st.caption(
        "VaR estimates the maximum expected daily loss at a given confidence level "
        "(parametric normal assumption)."
    )
    var_cols = ["Ticker", "VaR 95% (daily %)", "VaR 99% (daily %)", "Max Drawdown (%)"]

    def color_var(val):
        """Redder = worse (more negative VaR)."""
        if val <= -5:
            return "color: #f85149; font-weight: bold"
        elif val <= -2:
            return "color: #f0883e; font-weight: bold"
        return ""

    var_styled = comp_df[var_cols].style.map(
        color_var,
        subset=["VaR 95% (daily %)", "VaR 99% (daily %)", "Max Drawdown (%)"],
    ).format(
        {
            "VaR 95% (daily %)": "{:.4f}",
            "VaR 99% (daily %)": "{:.4f}",
            "Max Drawdown (%)": "{:.4f}",
        }
    )
    st.dataframe(var_styled, width="stretch", hide_index=True)

    # Interpretation text
    riskiest = comp_df.loc[comp_df["Annualized Volatility (%)"].idxmax(), "Ticker"]
    safest = comp_df.loc[comp_df["Annualized Volatility (%)"].idxmin(), "Ticker"]
    best_sharpe = comp_df.loc[comp_df["Sharpe Ratio"].idxmax(), "Ticker"]

    st.markdown(
        f"""
        **Key Takeaways:**
        - **{riskiest}** has the highest annualized volatility — the riskiest stock in this set.
        - **{safest}** has the lowest annualized volatility — the most stable stock.
        - **{best_sharpe}** offers the best risk-adjusted return (highest Sharpe Ratio).
        """
    )

    # ──────────────────────────────────────────────
    # Section 6 — Download
    # ──────────────────────────────────────────────
    st.download_button(
        label="📥 Download Risk Table CSV",
        data=comp_df.to_csv(index=False),
        file_name="risk_comparison.csv",
        mime="text/csv",
    )


# ── Standalone test ──────────────────────────────
if __name__ == "__main__":
    from data_loader import fetch_stock_data
    data_dict = fetch_stock_data()
    render(data_dict)
