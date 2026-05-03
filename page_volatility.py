import streamlit as st
import pandas as pd
import plotly.graph_objects as go


def render(data_dict: dict):
    # data_dict keys: 'AAPL', 'TSLA', 'JNJ'
    # DataFrame cols: Date, Open, High, Low, Close, Volume,
    #                 Daily Return (%), Volatility (Rolling Std)

    st.title("Volatility Dashboard")
    st.caption("Rolling 30-day volatility analysis across all three stocks.")

    # ── Color palette (matches project theme) ──────────────────────────────
    colors = {'AAPL': '#58a6ff', 'TSLA': '#f0883e', 'JNJ': '#3fb950'}

    # ── Build multi-line rolling volatility figure ─────────────────────────
    fig = go.Figure()
    summary_rows = []

    for ticker, df in data_dict.items():
        vol = df['Volatility (Rolling Std)'].dropna()
        dates = df['Date'][vol.index]

        fig.add_trace(go.Scatter(
            x=dates,
            y=vol,
            mode='lines',
            name=ticker,
            line=dict(color=colors.get(ticker, '#ffffff'), width=2),
            hovertemplate=(
                f"<b>{ticker}</b><br>"
                "Date: %{x|%Y-%m-%d}<br>"
                "Volatility: %{y:.4f}<extra></extra>"
            )
        ))

        peak_idx = vol.idxmax()
        summary_rows.append({
            "Ticker": ticker,
            "Avg Volatility": round(vol.mean(), 4),
            "Peak Volatility": round(vol.max(), 4),
            "Peak Date": df.loc[peak_idx, 'Date'].date()
        })

    # ── Market event annotations ───────────────────────────────────────────
    events = {
        '2022-01-01': '2022 Market Correction',
        '2022-11-01': 'Crypto/Tech Selloff',
        '2023-03-01': 'Banking Crisis'
    }

    for date_str, label in events.items():
        ts = pd.to_datetime(date_str).timestamp() * 1000
        fig.add_vline(
            x=ts,
            line_dash='dash',
            line_color='#8b949e',
            line_width=1.2,
            annotation_text=label,
            annotation_position='top left',
            annotation_font=dict(color='#8b949e', size=11)
        )

    fig.update_layout(
        template='plotly_dark',
        title='30-Day Rolling Volatility — AAPL vs TSLA vs JNJ',
        xaxis_title='Date',
        yaxis_title='Volatility (Rolling Std)',
        legend=dict(
            orientation='h',
            yanchor='bottom',
            y=1.02,
            xanchor='right',
            x=1
        ),
        hovermode='x unified',
        margin=dict(t=80, b=60),
        paper_bgcolor='rgba(0,0,0,0)',
        plot_bgcolor='rgba(13,17,23,0.6)'
    )

    st.plotly_chart(fig, use_container_width=True)

    # ── Volatility Summary Table ───────────────────────────────────────────
    st.subheader("Volatility Summary")
    summary_df = pd.DataFrame(summary_rows)
    st.dataframe(summary_df, use_container_width=True, hide_index=True)

    # ── Extra: individual ticker deep-dive ────────────────────────────────
    st.markdown("---")
    st.subheader("Single Stock Volatility Deep-Dive")

    selected = st.selectbox("Select Ticker", list(data_dict.keys()))
    df_sel = data_dict[selected].copy()
    vol_sel = df_sel['Volatility (Rolling Std)'].dropna()
    dates_sel = df_sel['Date'][vol_sel.index]

    fig2 = go.Figure()

    # Filled area for visual depth
    fig2.add_trace(go.Scatter(
        x=dates_sel,
        y=vol_sel,
        mode='lines',
        name='30-Day Vol',
        fill='tozeroy',
        line=dict(color=colors.get(selected, '#58a6ff'), width=2),
        fillcolor=f"rgba({','.join(str(int(colors.get(selected,'#58a6ff').lstrip('#')[i:i+2], 16)) for i in (0,2,4))},0.15)"
    ))

    # Horizontal mean line
    mean_vol = vol_sel.mean()
    fig2.add_hline(
        y=mean_vol,
        line_dash='dot',
        line_color='#f0883e',
        annotation_text=f"Mean: {mean_vol:.4f}",
        annotation_position='right',
        annotation_font=dict(color='#f0883e')
    )

    for date_str, label in events.items():
        ts = pd.to_datetime(date_str).timestamp() * 1000
        fig2.add_vline(
            x=ts,
            line_dash='dash',
            line_color='#8b949e',
            line_width=1,
            annotation_text=label,
            annotation_position='top left',
            annotation_font=dict(color='#8b949e', size=10)
        )

    fig2.update_layout(
        template='plotly_dark',
        title=f'{selected} — Rolling Volatility with Mean Reference',
        xaxis_title='Date',
        yaxis_title='Volatility (Rolling Std)',
        paper_bgcolor='rgba(0,0,0,0)',
        plot_bgcolor='rgba(13,17,23,0.6)'
    )

    st.plotly_chart(fig2, use_container_width=True)

    # Quick stats for the selected ticker
    c1, c2, c3 = st.columns(3)
    c1.metric("Average Volatility", f"{vol_sel.mean():.4f}")
    c2.metric("Peak Volatility", f"{vol_sel.max():.4f}")
    c3.metric("Current Volatility", f"{vol_sel.iloc[-1]:.4f}")
