import streamlit as st
import plotly.graph_objects as go
import pandas as pd

from data_loader import fetch_stock_data

def render(data_dict: dict):
    # 1. Ticker selectbox and date range filter (two columns)
    col1, col2 = st.columns(2)
    with col1:
        ticker = st.selectbox("Select Ticker", options=list(data_dict.keys()))
    
    df = data_dict[ticker].copy()
    df['Date'] = pd.to_datetime(df['Date'], errors='coerce')
    df = df.dropna(subset=['Date'])
    
    if df.empty:
        st.warning(f"No valid date data available for {ticker}.")
        return
        
    min_date = df['Date'].min().date()
    max_date = df['Date'].max().date()
    
    with col2:
        date_range = st.date_input(
            "Select Date Range", 
            value=(min_date, max_date), 
            min_value=min_date, 
            max_value=max_date
        )
    
    if len(date_range) == 2:
        start_date, end_date = date_range
        mask = (df['Date'].dt.date >= start_date) & (df['Date'].dt.date <= end_date)
        filtered_df = df.loc[mask].copy()
    else:
        filtered_df = df.copy()

    # 2. Closing price line chart with moving average overlay
    st.subheader("Closing Price & Moving Averages")
    ma_options = [20, 50, 100, 200]
    ma_selected = st.multiselect("Select Moving Averages", options=ma_options, default=[20, 50])
    
    fig_close = go.Figure()
    fig_close.add_trace(go.Scatter(
        x=filtered_df['Date'], y=filtered_df['Close'], 
        mode='lines', name='Close', 
        line=dict(color='#58a6ff')
    ))
    
    ma_colors = {20: '#f0883e', 50: '#3fb950', 100: '#d2a8ff', 200: '#ffa657'}
    
    for ma in ma_selected:
        # Calculate moving average on the whole series then slice
        df[f'MA_{ma}'] = df['Close'].rolling(window=ma).mean()
        if len(date_range) == 2:
            ma_data = df.loc[mask, f'MA_{ma}']
        else:
            ma_data = df[f'MA_{ma}']
            
        fig_close.add_trace(go.Scatter(
            x=filtered_df['Date'], y=ma_data, 
            mode='lines', name=f'MA {ma}', 
            line=dict(color=ma_colors[ma])
        ))
    
    fig_close.update_layout(template='plotly_dark', xaxis_title="Date", yaxis_title="Price")
    st.plotly_chart(fig_close, width="stretch")
    
    # 3. Candlestick chart with range slider
    st.subheader("Candlestick Chart")
    fig_candle = go.Figure(data=[go.Candlestick(
        x=filtered_df['Date'],
        open=filtered_df['Open'],
        high=filtered_df['High'],
        low=filtered_df['Low'],
        close=filtered_df['Close'],
        increasing_line_color='#3fb950',
        decreasing_line_color='#f85149'
    )])
    fig_candle.update_layout(
        template='plotly_dark',
        xaxis_title="Date",
        yaxis_title="Price",
        xaxis_rangeslider_visible=True
    )
    st.plotly_chart(fig_candle, width="stretch")
    
    # 4. Volume bar chart
    st.subheader("Trading Volume")
    fig_vol = go.Figure()
    fig_vol.add_trace(go.Bar(
        x=filtered_df['Date'],
        y=filtered_df['Volume'],
        name='Volume',
        marker_color='#238636'
    ))
    fig_vol.update_layout(template='plotly_dark', xaxis_title="Date", yaxis_title="Volume")
    st.plotly_chart(fig_vol, width="stretch")
    
    # 5. Daily Return (%) bar chart
    st.subheader("Daily Return (%)")
    colors = ['#3fb950' if val >= 0 else '#f85149' for val in filtered_df['Daily Return (%)']]
    fig_ret = go.Figure()
    fig_ret.add_trace(go.Bar(
        x=filtered_df['Date'],
        y=filtered_df['Daily Return (%)'],
        name='Daily Return',
        marker_color=colors
    ))
    fig_ret.update_layout(template='plotly_dark', xaxis_title="Date", yaxis_title="Return (%)")
    st.plotly_chart(fig_ret, width="stretch")
    
    # 6. A download button for filtered CSV
    csv_data = filtered_df.to_csv(index=False).encode('utf-8')
    st.download_button(
        label="Download Filtered CSV",
        data=csv_data,
        file_name=f"{ticker}_filtered_data.csv",
        mime='text/csv'
    )

if __name__ == "__main__":
    render(data_dict)