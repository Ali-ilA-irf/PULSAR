# page_dashboard.py — Dashboard Overview
# Author: Muhammad Faizan (24F-3103)
# Module Contract: render(data_dict: dict)
# data_dict keys: 'AAPL', 'TSLA', 'JNJ'
# DataFrame cols: Date, Open, High, Low, Close, Volume,
#                 Daily Return (%), Volatility (Rolling Std)

import streamlit as st
import pandas as pd
import numpy as np
import plotly.graph_objects as go
import page_gui


# ─────────────────────────────────────────────────────────────
#  CONSTANTS
# ─────────────────────────────────────────────────────────────

TICKER_COLORS = {
    'AAPL': {'line': '#38bdf8', 'fill': 'rgba(56,189,248,0.08)',  'border': 'rgba(56,189,248,0.3)'},
    'TSLA': {'line': '#fb923c', 'fill': 'rgba(251,146,60,0.08)',  'border': 'rgba(251,146,60,0.3)'},
    'JNJ':  {'line': '#4ade80', 'fill': 'rgba(74,222,128,0.08)',  'border': 'rgba(74,222,128,0.3)'},
}

TICKER_LABELS = {
    'AAPL': 'Apple Inc.',
    'TSLA': 'Tesla Inc.',
    'JNJ':  'Johnson & Johnson',
}

TEAM_MEMBERS = [
    ("Ali Irfan",    "24F-0517", "Leader",          "⬡", "#38bdf8"),
    ("Eshal Hussain","24F-0597", "Data Engineer",   "◈", "#fb923c"),
    ("Maryam Zahid", "24F-0658", "Statistician",    "◉", "#a78bfa"),
    ("Hassan",       "24F-3101", "Analyst",         "◆", "#4ade80"),
    ("Faizan",       "24F-3103", "UI Designer",     "◇", "#f472b6"),
]


# ─────────────────────────────────────────────────────────────
#  HELPER : build_sparkline()
# ─────────────────────────────────────────────────────────────

def build_sparkline(series: pd.Series, color: str, fill_color: str) -> go.Figure:
    """30-day sparkline — no axes, transparent background."""
    fig = go.Figure()
    fig.add_trace(go.Scatter(
        y=series,
        mode='lines',
        line=dict(color=color, width=2),
        fill='tozeroy',
        fillcolor=fill_color,
        hoverinfo='skip',
    ))
    fig.update_layout(
        height=70,
        margin=dict(l=0, r=0, t=0, b=0),
        paper_bgcolor='rgba(0,0,0,0)',
        plot_bgcolor='rgba(0,0,0,0)',
        xaxis=dict(visible=False, fixedrange=True),
        yaxis=dict(visible=False, fixedrange=True),
        showlegend=False,
    )
    return fig


# ─────────────────────────────────────────────────────────────
#  HELPER : build_multi_close_chart()
# ─────────────────────────────────────────────────────────────

def build_multi_close_chart(data_dict: dict) -> go.Figure:
    """Normalized closing price for all tickers on one chart."""
    fig = go.Figure()
    for ticker, df in data_dict.items():
        if ticker not in TICKER_COLORS:
            continue
        close = df['Close'].dropna()
        normalized = (close / close.iloc[0]) * 100        # base-100 index
        color = TICKER_COLORS[ticker]['line']
        fig.add_trace(go.Scatter(
            x=df['Date'],
            y=normalized,
            mode='lines',
            name=ticker,
            line=dict(color=color, width=2),
            hovertemplate=f'<b>{ticker}</b><br>Date: %{{x|%b %d, %Y}}<br>Index: %{{y:.1f}}<extra></extra>',
        ))
    fig.update_layout(
        template='plotly_dark',
        title='Normalized Closing Price (Base = 100)',
        xaxis_title='Date',
        yaxis_title='Price Index',
        paper_bgcolor='rgba(0,0,0,0)',
        plot_bgcolor='rgba(8,12,18,0.6)',
        legend=dict(
            orientation='h',
            yanchor='bottom', y=1.02,
            xanchor='right',  x=1,
            font=dict(family='JetBrains Mono', size=11),
        ),
        xaxis=dict(gridcolor='#1e2d3d', showgrid=True),
        yaxis=dict(gridcolor='#1e2d3d', showgrid=True),
        font=dict(family='Space Grotesk'),
        margin=dict(t=50, b=40, l=50, r=20),
    )
    return fig


# ─────────────────────────────────────────────────────────────
#  HELPER : build_volume_chart()
# ─────────────────────────────────────────────────────────────

def build_volume_chart(data_dict: dict) -> go.Figure:
    """Grouped bar chart of average monthly volume per ticker."""
    fig = go.Figure()
    for ticker, df in data_dict.items():
        if ticker not in TICKER_COLORS:
            continue
        df2 = df.copy()
        df2['Month'] = pd.to_datetime(df2['Date']).dt.to_period('Q').astype(str)
        avg_vol = df2.groupby('Month')['Volume'].mean().reset_index()
        color = TICKER_COLORS[ticker]['line']
        fig.add_trace(go.Bar(
            x=avg_vol['Month'],
            y=avg_vol['Volume'],
            name=ticker,
            marker_color=color,
            opacity=0.8,
        ))
    fig.update_layout(
        template='plotly_dark',
        title='Average Quarterly Volume',
        xaxis_title='Quarter',
        yaxis_title='Avg Volume',
        barmode='group',
        paper_bgcolor='rgba(0,0,0,0)',
        plot_bgcolor='rgba(8,12,18,0.6)',
        legend=dict(
            orientation='h',
            yanchor='bottom', y=1.02,
            xanchor='right',  x=1,
            font=dict(family='JetBrains Mono', size=11),
        ),
        xaxis=dict(gridcolor='#1e2d3d', tickfont=dict(size=10, family='JetBrains Mono')),
        yaxis=dict(gridcolor='#1e2d3d'),
        font=dict(family='Space Grotesk'),
        margin=dict(t=50, b=40, l=60, r=20),
    )
    return fig


# ─────────────────────────────────────────────────────────────
#  MAIN : render()
# ─────────────────────────────────────────────────────────────

def render(data_dict: dict):

    # ── Hero ──────────────────────────────────────────────────
    page_gui.render_hero()

    st.title("Dashboard Overview")
    st.caption("Real-time overview of AAPL, TSLA, and JNJ | Source: Yahoo Finance 2021–2024")

    # ── Section 1 : Metric Cards + Sparklines ─────────────────
    st.subheader("Live Snapshot")

    primary_tickers = [t for t in ['AAPL', 'TSLA', 'JNJ'] if t in data_dict]
    cols = st.columns(len(primary_tickers))

    for i, ticker in enumerate(primary_tickers):
        df    = data_dict[ticker]
        price = df['Close'].iloc[-1]
        delta = df['Daily Return (%)'].iloc[-1]
        vol   = df['Volatility (Rolling Std)'].dropna().iloc[-1]
        color = TICKER_COLORS.get(ticker, {})

        with cols[i]:
            # Metric card
            st.metric(
                label=f"{ticker} — {TICKER_LABELS.get(ticker, ticker)}",
                value=f"${price:.2f}",
                delta=f"{delta:+.2f}%",
            )
            # Sparkline (last 30 trading days)
            spark = df['Close'].tail(30)
            fig_spark = build_sparkline(
                spark,
                color.get('line', '#38bdf8'),
                color.get('fill', 'rgba(56,189,248,0.08)'),
            )
            st.plotly_chart(fig_spark, use_container_width=True, config={'displayModeBar': False})

            # Mini stats row
            st.markdown(
                f"""
                <div style="
                    display: flex;
                    justify-content: space-between;
                    font-family: 'JetBrains Mono', monospace;
                    font-size: 10px;
                    color: #64748b;
                    padding: 4px 2px 10px;
                    border-bottom: 1px solid #1e2d3d;
                ">
                    <span>30D HIGH <span style="color:{color.get('line','#38bdf8')};">${df['Close'].tail(30).max():.2f}</span></span>
                    <span>30D LOW <span style="color:{color.get('line','#38bdf8')};">${df['Close'].tail(30).min():.2f}</span></span>
                    <span>VOL σ <span style="color:{color.get('line','#38bdf8')};">{vol:.3f}</span></span>
                </div>
                """,
                unsafe_allow_html=True,
            )

    st.markdown("---")

    # ── Section 2 : Normalized Price Chart ────────────────────
    st.subheader("Comparative Performance")
    st.caption("All tickers normalized to 100 at Jan 1, 2021 — see relative growth.")
    fig_multi = build_multi_close_chart(data_dict)
    st.plotly_chart(fig_multi, use_container_width=True)

    # ── Section 3 : Volume Chart ──────────────────────────────
    st.subheader("Trading Activity")
    st.caption("Average quarterly trading volume per ticker — larger bars = more market activity.")
    fig_vol = build_volume_chart(data_dict)
    st.plotly_chart(fig_vol, use_container_width=True)

    st.markdown("---")

    # ── Section 4 : Dataset Info Cards ────────────────────────
    st.subheader("Dataset Information")

    info_cols = st.columns(len(primary_tickers))
    for i, ticker in enumerate(primary_tickers):
        df = data_dict[ticker]
        c  = TICKER_COLORS.get(ticker, {})
        with info_cols[i]:
            avg_ret = df['Daily Return (%)'].mean()
            avg_vol = df['Volatility (Rolling Std)'].mean()
            st.markdown(
                f"""
                <div style="
                    background: linear-gradient(135deg, #111820, #0d1520);
                    border: 1px solid {c.get('border', '#1e2d3d')};
                    border-radius: 12px;
                    padding: 20px 18px;
                    font-family: 'Space Grotesk', sans-serif;
                ">
                    <div style="
                        font-family: 'JetBrains Mono', monospace;
                        font-size: 14px;
                        font-weight: 700;
                        color: {c.get('line','#38bdf8')};
                        letter-spacing: 0.12em;
                        margin-bottom: 14px;
                        display: flex;
                        align-items: center;
                        gap: 8px;
                    ">⬡ {ticker}
                        <span style="
                            font-size: 9px;
                            color: #3d5166;
                            font-weight: 400;
                            letter-spacing: 0.06em;
                        ">{TICKER_LABELS.get(ticker,'')}</span>
                    </div>
                    <div style="display: grid; gap: 8px;">
                        <div style="display:flex;justify-content:space-between;font-size:12px;color:#64748b;">
                            <span>Records</span>
                            <span style="color:#e2eaf4;font-weight:600;">{len(df):,}</span>
                        </div>
                        <div style="display:flex;justify-content:space-between;font-size:12px;color:#64748b;">
                            <span>From</span>
                            <span style="color:#e2eaf4;font-weight:600;">{df['Date'].min().strftime('%b %d, %Y')}</span>
                        </div>
                        <div style="display:flex;justify-content:space-between;font-size:12px;color:#64748b;">
                            <span>To</span>
                            <span style="color:#e2eaf4;font-weight:600;">{df['Date'].max().strftime('%b %d, %Y')}</span>
                        </div>
                        <div style="display:flex;justify-content:space-between;font-size:12px;color:#64748b;">
                            <span>Avg Daily Return</span>
                            <span style="color:{'#4ade80' if avg_ret >= 0 else '#f87171'};font-weight:600;">{avg_ret:+.4f}%</span>
                        </div>
                        <div style="display:flex;justify-content:space-between;font-size:12px;color:#64748b;">
                            <span>Avg Volatility</span>
                            <span style="color:{c.get('line','#38bdf8')};font-weight:600;">{avg_vol:.4f}</span>
                        </div>
                    </div>
                </div>
                """,
                unsafe_allow_html=True,
            )

    st.markdown("---")

    # ── Section 5 : Recent Data Table ─────────────────────────
    st.subheader("Recent Trading Data")
    ticker_select = st.selectbox("Select Ticker", primary_tickers, key="dash_ticker_select")
    display_df = data_dict[ticker_select].tail(10).copy()
    display_df['Date'] = display_df['Date'].dt.strftime('%b %d, %Y')
    numeric_cols = ['Open', 'High', 'Low', 'Close', 'Daily Return (%)', 'Volatility (Rolling Std)']
    for col in numeric_cols:
        if col in display_df.columns:
            display_df[col] = display_df[col].round(4)
    st.dataframe(display_df, use_container_width=True, hide_index=True)

    st.markdown("---")

    # ── Section 6 : About Box ──────────────────────────────────
    st.markdown(
        """
        <div style="
            background: linear-gradient(135deg, #0d1520, #0a1018);
            border: 1px solid #1e2d3d;
            border-left: 3px solid #38bdf8;
            border-radius: 10px;
            padding: 20px 22px;
            font-family: 'Space Grotesk', sans-serif;
            font-size: 13px;
            color: #64748b;
            line-height: 1.7;
            margin-bottom: 24px;
        ">
            <span style="color:#38bdf8;font-weight:700;font-family:'JetBrains Mono',monospace;letter-spacing:0.08em;">
                ⬡ ABOUT PULSAR
            </span><br/><br/>
            An interactive web application analyzing historical stock price volatility of
            <strong style="color:#38bdf8;">Apple Inc. (AAPL)</strong>,
            <strong style="color:#fb923c;">Tesla Inc. (TSLA)</strong>, and
            <strong style="color:#4ade80;">Johnson &amp; Johnson (JNJ)</strong>
            over the period 2021–2024 using advanced statistical and probability methods.
            Built with Python, Streamlit, Plotly, Scipy, and Scikit-Learn.
        </div>
        """,
        unsafe_allow_html=True,
    )

    # ── Section 7 : Team Cards ────────────────────────────────
    st.subheader("Development Team")

    team_cols = st.columns(5)
    for col, (name, roll, role, icon, color) in zip(team_cols, TEAM_MEMBERS):
        with col:
            st.markdown(
                f"""
                <div style="
                    background: linear-gradient(135deg, #111820, #0d1520);
                    border: 1px solid #1e2d3d;
                    border-top: 2px solid {color};
                    border-radius: 12px;
                    padding: 18px 14px;
                    text-align: center;
                    font-family: 'Space Grotesk', sans-serif;
                    transition: all 0.3s ease;
                ">
                    <div style="
                        font-size: 22px;
                        color: {color};
                        margin-bottom: 10px;
                        opacity: 0.9;
                    ">{icon}</div>
                    <div style="
                        font-size: 13px;
                        font-weight: 700;
                        color: #e2eaf4;
                        margin-bottom: 4px;
                        letter-spacing: -0.01em;
                    ">{name}</div>
                    <div style="
                        font-family: 'JetBrains Mono', monospace;
                        font-size: 10px;
                        color: #3d5166;
                        letter-spacing: 0.06em;
                        margin-bottom: 8px;
                    ">{roll}</div>
                    <div style="
                        font-size: 10px;
                        font-weight: 600;
                        color: {color};
                        background: {color}14;
                        border: 1px solid {color}30;
                        border-radius: 4px;
                        padding: 3px 8px;
                        display: inline-block;
                        letter-spacing: 0.05em;
                        text-transform: uppercase;
                    ">{role}</div>
                </div>
                """,
                unsafe_allow_html=True,
            )

    # ── Footer ────────────────────────────────────────────────
    st.markdown(
        """
        <div style="
            text-align: center;
            margin-top: 40px;
            padding: 20px;
            font-family: 'JetBrains Mono', monospace;
            font-size: 10px;
            letter-spacing: 0.12em;
            color: #1e2d3d;
            border-top: 1px solid #1e2d3d;
        ">
            PULSAR · BCS-4F + BSE-4 · DATA SOURCE: YAHOO FINANCE · 2021–2024
        </div>
        """,
        unsafe_allow_html=True,
    )


# ── Standalone test ──────────────────────────────────────────
if __name__ == "__main__":
    from data_loader import fetch_stock_data
    data_dict = fetch_stock_data()
    render(data_dict)
