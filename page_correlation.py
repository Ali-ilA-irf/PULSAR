import streamlit as st
import pandas as pd
import plotly.express as px
import plotly.graph_objects as go


def render(data_dict: dict):
    # data_dict keys: 'AAPL', 'TSLA', 'JNJ'
    # DataFrame cols: Date, Open, High, Low, Close, Volume,
    #                 Daily Return (%), Volatility (Rolling Std)

    st.title("Correlation Analysis")
    st.caption("Heatmap showing relationships between stock variables.")

    ticker = st.selectbox("Select Ticker", list(data_dict.keys()))
    df = data_dict[ticker]

    cols = ['Open', 'High', 'Low', 'Close', 'Volume',
            'Daily Return (%)', 'Volatility (Rolling Std)']

    corr_matrix = df[cols].dropna().corr()

    # ── Correlation Heatmap ────────────────────────────────────────────────
    st.subheader("Correlation Heatmap")

    fig = px.imshow(
        corr_matrix,
        text_auto=".2f",
        color_continuous_scale='RdBu',
        zmin=-1,
        zmax=1,
        aspect='auto'
    )

    fig.update_layout(
        template='plotly_dark',
        title=f'{ticker} — Correlation Matrix',
        paper_bgcolor='rgba(0,0,0,0)',
        plot_bgcolor='rgba(13,17,23,0.6)',
        coloraxis_colorbar=dict(
            title="r",
            tickvals=[-1, -0.5, 0, 0.5, 1],
            ticktext=['-1.0', '-0.5', '0.0', '+0.5', '+1.0']
        )
    )

    fig.update_xaxes(side='bottom')
    st.plotly_chart(fig, use_container_width=True)

    # ── Key Correlations (auto-text) ───────────────────────────────────────
    st.subheader("Key Correlations")

    pairs = []
    for i in range(len(cols)):
        for j in range(i + 1, len(cols)):
            pairs.append((cols[i], cols[j], corr_matrix.iloc[i, j]))

    pairs.sort(key=lambda x: abs(x[2]), reverse=True)

    for a, b, r in pairs[:3]:
        strength = "strongly" if abs(r) > 0.7 else "moderately"
        direction = "positively" if r > 0 else "negatively"
        icon = "🟢" if r > 0 else "🔴"
        st.write(
            f"{icon} **{a}** & **{b}** are {strength} {direction} correlated "
            f"*(r = {r:.2f})*"
        )

    st.caption(
        "r > 0.7 = strong positive  |  r < -0.7 = strong negative  |  r ≈ 0 = no correlation"
    )

    # ── Full Ranked Pairs Table ────────────────────────────────────────────
    st.markdown("---")
    st.subheader("All Correlation Pairs (Ranked by Strength)")

    pairs_df = pd.DataFrame(pairs, columns=["Variable A", "Variable B", "Correlation (r)"])
    pairs_df["Abs(r)"] = pairs_df["Correlation (r)"].abs().round(4)
    pairs_df["Correlation (r)"] = pairs_df["Correlation (r)"].round(4)
    pairs_df = pairs_df.sort_values("Abs(r)", ascending=False).drop(columns="Abs(r)")

    def color_corr(val):
        if val > 0.7:
            return 'color: #3fb950; font-weight: bold'
        elif val < -0.7:
            return 'color: #f85149; font-weight: bold'
        elif abs(val) > 0.4:
            return 'color: #f0883e'
        return 'color: #8b949e'

    st.dataframe(
        pairs_df.style.applymap(color_corr, subset=["Correlation (r)"]),
        use_container_width=True,
        hide_index=True
    )

    # ── Cross-Stock Daily Return Correlation ──────────────────────────────
    st.markdown("---")
    st.subheader("Cross-Stock Daily Return Correlation")
    st.caption("How closely do AAPL, TSLA, and JNJ move together?")

    tickers_available = list(data_dict.keys())

    if len(tickers_available) >= 2:
        returns_data = {}
        for t in tickers_available:
            returns_data[t] = data_dict[t].set_index('Date')['Daily Return (%)']

        returns_df = pd.DataFrame(returns_data).dropna()
        cross_corr = returns_df.corr()

        fig2 = px.imshow(
            cross_corr,
            text_auto=".2f",
            color_continuous_scale='RdBu',
            zmin=-1,
            zmax=1,
            aspect='auto'
        )

        fig2.update_layout(
            template='plotly_dark',
            title='Cross-Stock Daily Return Correlation',
            paper_bgcolor='rgba(0,0,0,0)',
            plot_bgcolor='rgba(13,17,23,0.6)'
        )

        st.plotly_chart(fig2, use_container_width=True)

        # Interpretation
        for i in range(len(tickers_available)):
            for j in range(i + 1, len(tickers_available)):
                t1, t2 = tickers_available[i], tickers_available[j]
                r = cross_corr.loc[t1, t2]
                strength = "strongly" if abs(r) > 0.7 else ("moderately" if abs(r) > 0.4 else "weakly")
                direction = "positively" if r > 0 else "negatively"
                icon = "🟢" if r > 0.4 else ("🔴" if r < -0.4 else "⚪")
                st.write(f"{icon} **{t1}** & **{t2}** daily returns are {strength} {direction} correlated *(r = {r:.2f})*")
    else:
        st.info("Load at least two tickers to see cross-stock correlation.")
