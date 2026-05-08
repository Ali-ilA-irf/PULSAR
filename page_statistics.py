# page_statistics.py — Statistical Analysis
# Author: Maryam Zahid (24F-0658)
# Module Contract: render(data_dict: dict)
# data_dict keys: 'AAPL', 'TSLA', 'JNJ'
# DataFrame cols: Date, Open, High, Low, Close, Volume,
#                 Daily Return (%), Volatility (Rolling Std)

import streamlit as st
import pandas as pd
import numpy as np
import plotly.graph_objects as go
from scipy import stats
from data_loader import fetch_stock_data


def render(data_dict: dict):
    st.title("Statistical Analysis")
    st.caption(
        "Descriptive statistics and distribution analysis of daily stock returns."
    )

    ticker = st.selectbox("Select Ticker", list(data_dict.keys()), key="stats_ticker")
    df = data_dict[ticker]
    returns = df["Daily Return (%)"].dropna()

    # ──────────────────────────────────────────────
    # Section 1 — Descriptive Statistics Table (10 rows)
    # ──────────────────────────────────────────────
    st.subheader("Descriptive Statistics")

    ci = stats.t.interval(
        0.95,
        df=len(returns) - 1,
        loc=returns.mean(),
        scale=stats.sem(returns),
    )

    stats_data = {
        "Metric": [
            "Mean Return (%)",
            "Median Return (%)",
            "Std Deviation",
            "Variance",
            "Skewness",
            "Kurtosis",
            "Min Daily Return (%)",
            "Max Daily Return (%)",
            "95% CI Lower",
            "95% CI Upper",
        ],
        "Value": [
            round(returns.mean(), 4),
            round(returns.median(), 4),
            round(returns.std(), 4),
            round(returns.var(), 4),
            round(returns.skew(), 4),
            round(returns.kurtosis(), 4),
            round(returns.min(), 4),
            round(returns.max(), 4),
            round(ci[0], 4),
            round(ci[1], 4),
        ],
    }

    stats_df = pd.DataFrame(stats_data)
    st.dataframe(stats_df, width="stretch", hide_index=True)

    # ──────────────────────────────────────────────
    # Section 2 — Histogram with Normal PDF Overlay
    # ──────────────────────────────────────────────
    st.subheader("Return Distribution")

    mu, std = stats.norm.fit(returns)
    x_range = np.linspace(returns.min(), returns.max(), 300)
    pdf = stats.norm.pdf(x_range, mu, std)

    fig = go.Figure()
    fig.add_trace(
        go.Histogram(
            x=returns,
            nbinsx=50,
            histnorm="probability density",
            name="Daily Returns",
            marker_color="#58a6ff",
            opacity=0.7,
        )
    )
    fig.add_trace(
        go.Scatter(
            x=x_range,
            y=pdf,
            mode="lines",
            name="Normal PDF",
            line=dict(color="#f0883e", width=2),
        )
    )
    fig.update_layout(
        template="plotly_dark",
        title=f"{ticker} — Return Distribution",
        xaxis_title="Daily Return (%)",
        yaxis_title="Density",
        legend=dict(orientation="h", yanchor="bottom", y=1.02, xanchor="right", x=1),
    )
    st.plotly_chart(fig, width="stretch")

    # ──────────────────────────────────────────────
    # Section 3 — Skewness Interpretation
    # ──────────────────────────────────────────────
    skew = returns.skew()
    kurt = returns.kurtosis()

    if skew > 0.5:
        st.success(
            f"Right-skewed (skewness = {skew:.4f}): "
            "The distribution has a longer right tail — more instances of extreme positive returns."
        )
    elif skew < -0.5:
        st.warning(
            f"Left-skewed (skewness = {skew:.4f}): "
            "The distribution has a longer left tail — more instances of extreme negative returns."
        )
    else:
        st.info(
            f"Approximately symmetric (skewness = {skew:.4f}): "
            "Return distribution is fairly balanced around the mean."
        )

    if kurt > 0:
        st.info(
            f"Leptokurtic (excess kurtosis = {kurt:.4f}): "
            "Fatter tails than a normal distribution — higher probability of extreme returns."
        )
    else:
        st.info(
            f"Platykurtic (excess kurtosis = {kurt:.4f}): "
            "Thinner tails than a normal distribution — lower probability of extreme returns."
        )

    # ──────────────────────────────────────────────
    # Section 4 — Download
    # ──────────────────────────────────────────────
    st.download_button(
        label="📥 Download Stats CSV",
        data=stats_df.to_csv(index=False),
        file_name=f"{ticker}_statistics.csv",
        mime="text/csv",
    )


# ── Standalone test ──────────────────────────────
if __name__ == "__main__":
    from data_loader import fetch_stock_data
    data_dict = fetch_stock_data()
    render(data_dict)
