# page_probability.py — Probability Distribution
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
    st.title("Probability Distribution")
    st.caption(
        "Normal distribution fit on daily returns with probability analysis and Q-Q plot."
    )

    ticker = st.selectbox("Select Ticker", list(data_dict.keys()), key="prob_ticker")
    df = data_dict[ticker]
    returns = df["Daily Return (%)"].dropna()

    # ──────────────────────────────────────────────
    # Section 1 — Fit Parameters
    # ──────────────────────────────────────────────
    mu, std = stats.norm.fit(returns)

    c1, c2, c3, c4 = st.columns(4)
    c1.metric("Mean (μ)", f"{mu:.4f}%")
    c2.metric("Std Dev (σ)", f"{std:.4f}%")
    c3.metric("Observations", f"{len(returns):,}")
    # Shapiro-Wilk normality test (sample up to 5000)
    sample = returns.sample(min(5000, len(returns)), random_state=42)
    _, p_val = stats.shapiro(sample)
    c4.metric(
        "Shapiro-Wilk p-value",
        f"{p_val:.4f}",
        delta="Normal" if p_val > 0.05 else "Non-normal",
        delta_color="normal" if p_val > 0.05 else "inverse",
    )

    # ──────────────────────────────────────────────
    # Section 2 — Histogram + Normal PDF Overlay
    # ──────────────────────────────────────────────
    st.subheader("Distribution with Normal Fit")

    x_range = np.linspace(returns.min(), returns.max(), 300)
    pdf = stats.norm.pdf(x_range, mu, std)

    fig = go.Figure()
    fig.add_trace(
        go.Histogram(
            x=returns,
            nbinsx=50,
            histnorm="probability density",
            name="Returns",
            marker_color="#8957e5",
            opacity=0.7,
        )
    )
    fig.add_trace(
        go.Scatter(
            x=x_range,
            y=pdf,
            mode="lines",
            name="Normal PDF",
            line=dict(color="#f0883e", width=2.5),
        )
    )
    # Mark μ ± σ bands
    for sign, label in [(1, "μ+σ"), (-1, "μ−σ")]:
        fig.add_vline(
            x=mu + sign * std,
            line_dash="dot",
            line_color="#3fb950",
            annotation_text=label,
            annotation_position="top",
        )
    fig.add_vline(
        x=mu,
        line_dash="dash",
        line_color="#58a6ff",
        annotation_text="μ",
        annotation_position="top",
    )
    fig.update_layout(
        template="plotly_dark",
        title=f"{ticker} — Probability Distribution of Daily Returns",
        xaxis_title="Daily Return (%)",
        yaxis_title="Density",
        legend=dict(orientation="h", yanchor="bottom", y=1.02, xanchor="right", x=1),
    )
    st.plotly_chart(fig, width="stretch")

    # ──────────────────────────────────────────────
    # Section 3 — Probability Table
    # ──────────────────────────────────────────────
    st.subheader("Probability Table")

    threshold = st.slider(
        "Custom threshold for extreme return (%)",
        min_value=0.5,
        max_value=5.0,
        value=2.0,
        step=0.5,
        help="Adjust to compute P(gain > X%) and P(loss < -X%)",
        key="prob_threshold",
    )

    prob_data = {
        "Event": [
            "P(Daily Gain > 0%)",
            "P(Daily Loss < 0%)",
            f"P(Extreme Loss < −{threshold:.1f}%)",
            f"P(Extreme Gain > +{threshold:.1f}%)",
            "P(Within 1 Std Dev)",
            "P(Within 2 Std Dev)",
        ],
        "Probability": [
            round(1 - stats.norm.cdf(0, mu, std), 4),
            round(stats.norm.cdf(0, mu, std), 4),
            round(stats.norm.cdf(-threshold, mu, std), 4),
            round(1 - stats.norm.cdf(threshold, mu, std), 4),
            round(
                stats.norm.cdf(mu + std, mu, std)
                - stats.norm.cdf(mu - std, mu, std),
                4,
            ),
            round(
                stats.norm.cdf(mu + 2 * std, mu, std)
                - stats.norm.cdf(mu - 2 * std, mu, std),
                4,
            ),
        ],
    }
    prob_df = pd.DataFrame(prob_data)

    def color_prob(val):
        if val > 0.5:
            return "color: #3fb950; font-weight: bold"
        elif val < 0.1:
            return "color: #f85149; font-weight: bold"
        return "color: #f0883e; font-weight: bold"

    styled = prob_df.style.map(color_prob, subset=["Probability"]).format(
        {"Probability": "{:.4f}"}
    )
    st.dataframe(styled, width="stretch", hide_index=True)

    # ──────────────────────────────────────────────
    # Section 4 — CDF Plot
    # ──────────────────────────────────────────────
    st.subheader("Cumulative Distribution Function (CDF)")

    cdf_vals = stats.norm.cdf(x_range, mu, std)
    empirical_sorted = np.sort(returns.values)
    empirical_cdf = np.arange(1, len(empirical_sorted) + 1) / len(empirical_sorted)

    fig_cdf = go.Figure()
    fig_cdf.add_trace(
        go.Scatter(
            x=empirical_sorted,
            y=empirical_cdf,
            mode="markers",
            name="Empirical CDF",
            marker=dict(color="#58a6ff", size=3, opacity=0.5),
        )
    )
    fig_cdf.add_trace(
        go.Scatter(
            x=x_range,
            y=cdf_vals,
            mode="lines",
            name="Normal CDF",
            line=dict(color="#f0883e", width=2),
        )
    )
    fig_cdf.add_hline(y=0.5, line_dash="dot", line_color="gray", annotation_text="50%")
    fig_cdf.update_layout(
        template="plotly_dark",
        title=f"{ticker} — Empirical vs Normal CDF",
        xaxis_title="Daily Return (%)",
        yaxis_title="Cumulative Probability",
    )
    st.plotly_chart(fig_cdf, width="stretch")

    # ──────────────────────────────────────────────
    # Section 5 — Q-Q Plot
    # ──────────────────────────────────────────────
    st.subheader("Q-Q Plot")
    st.caption(
        "Points near the reference line indicate the returns are approximately normally distributed."
    )

    (theoretical_q, sample_q), _ = stats.probplot(returns)
    slope, intercept, _, _, _ = stats.linregress(theoretical_q, sample_q)
    ref_line = slope * np.array(theoretical_q) + intercept

    fig2 = go.Figure()
    fig2.add_trace(
        go.Scatter(
            x=theoretical_q,
            y=sample_q,
            mode="markers",
            name="Quantiles",
            marker=dict(color="#58a6ff", size=4, opacity=0.7),
        )
    )
    fig2.add_trace(
        go.Scatter(
            x=theoretical_q,
            y=ref_line,
            mode="lines",
            name="Reference Line",
            line=dict(color="#f0883e", width=2),
        )
    )
    fig2.update_layout(
        template="plotly_dark",
        title=f"{ticker} — Q-Q Plot (Points near the line = normally distributed returns)",
        xaxis_title="Theoretical Quantiles",
        yaxis_title="Sample Quantiles",
    )
    st.plotly_chart(fig2, width="stretch")

    # Interpretation text under Q-Q
    dev = np.max(np.abs(np.array(sample_q) - ref_line))
    if dev < 1.0:
        st.success(
            "Returns are approximately normal — the Q-Q points closely follow the reference line."
        )
    else:
        st.warning(
            "Returns show heavy tails — the Q-Q points deviate at the extremes, "
            "indicating more frequent large moves than a normal distribution predicts."
        )


# ── Standalone test ──────────────────────────────
if __name__ == "__main__":
    from data_loader import fetch_stock_data
    data_dict = fetch_stock_data()
    render(data_dict)
