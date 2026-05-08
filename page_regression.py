import streamlit as st
import plotly.graph_objects as go
import pandas as pd
import numpy as np
from sklearn.metrics import r2_score, mean_absolute_error, mean_squared_error

from data_loader import fetch_stock_data

def render(data_dict: dict):
    # 1. Ticker selectbox
    ticker = st.selectbox("Select Ticker", options=list(data_dict.keys()), key="reg_ticker")
    df = data_dict[ticker].copy()
    
    # Ensure Date is datetime and sorted
    df['Date'] = pd.to_datetime(df['Date'])
    df = df.sort_values('Date').reset_index(drop=True)
    
    # 2. Radio button to choose model
    model_choice = st.radio(
        "Choose Model",
        options=["Linear Regression", "Polynomial (deg 2)", "Polynomial (deg 3)"]
    )
    
    # 3. Use numpy polyfit - determine degree
    degree = 1
    if model_choice == "Polynomial (deg 2)":
        degree = 2
    elif model_choice == "Polynomial (deg 3)":
        degree = 3
        
    # Prepare data for regression (using simple indices representing time)
    x_all = np.arange(len(df))
    y_all = df['Close'].values
    
    # 4. Train/Test split at 80% (NO shuffle, time-series order preserved)
    split_idx = int(len(df) * 0.8)
    
    x_train = x_all[:split_idx]
    y_train = y_all[:split_idx]
    
    x_test = x_all[split_idx:]
    y_test = y_all[split_idx:]
    
    # Fit the model
    coeffs = np.polyfit(x_train, y_train, deg=degree)
    poly = np.poly1d(coeffs)
    
    # Predictions
    y_train_pred = poly(x_train)
    y_test_pred = poly(x_test)
    y_all_pred = poly(x_all)
    
    # 5. Metrics table showing R², MAE, RMSE for both Train and Test sets
    def compute_metrics(y_true, y_pred):
        return {
            "R²": r2_score(y_true, y_pred),
            "MAE": mean_absolute_error(y_true, y_pred),
            "RMSE": np.sqrt(mean_squared_error(y_true, y_pred))
        }
        
    train_metrics = compute_metrics(y_train, y_train_pred)
    test_metrics = compute_metrics(y_test, y_test_pred)
    
    metrics_df = pd.DataFrame([train_metrics, test_metrics], index=["Train", "Test"])
    st.subheader("Model Evaluation Metrics")
    st.table(metrics_df)
    
    # 7. Slider for forecast days (10 to 90, default 30)
    forecast_days = st.slider("Forecast Days", min_value=10, max_value=90, value=30, step=1)
    
    # Forecast using pd.date_range with freq='B'
    last_date = df['Date'].iloc[-1]
    future_dates = pd.date_range(start=last_date, periods=forecast_days + 1, freq='B')[1:]
    
    x_future = np.arange(len(df), len(df) + forecast_days)
    y_future_pred = poly(x_future)
    
    forecast_df = pd.DataFrame({
        'Date': future_dates,
        'Forecast': y_future_pred
    })
    
    # 6. Plotly chart showing: actual close prices, fitted curve, future forecast line, and a vertical dashed line
    st.subheader("Regression & Price Forecast")
    fig = go.Figure()
    
    # Actual
    fig.add_trace(go.Scatter(
        x=df['Date'], y=df['Close'], 
        mode='lines', name='Actual Close',
        line=dict(color='#58a6ff')
    ))
    
    # Fitted Curve (plotted over all historical dates)
    fig.add_trace(go.Scatter(
        x=df['Date'], y=y_all_pred, 
        mode='lines', name='Fitted Curve',
        line=dict(color='#f0883e', dash='dot')
    ))
    
    # Forecast
    fig.add_trace(go.Scatter(
        x=forecast_df['Date'], y=forecast_df['Forecast'], 
        mode='lines', name='Forecast',
        line=dict(color='#3fb950')
    ))
    
    # Vertical dashed line at train/test split
    split_date = df['Date'].iloc[split_idx]
    fig.add_vline(
        x=split_date.timestamp() * 1000 if isinstance(split_date, pd.Timestamp) else split_date, 
        line_width=2, line_dash="dash", line_color="white", 
        annotation_text="Train/Test Split"
    )
    
    fig.update_layout(template='plotly_dark', xaxis_title="Date", yaxis_title="Price")
    st.plotly_chart(fig, width="stretch")
    
    # 8. Download button for forecast CSV (Date, Forecast columns)
    csv_forecast = forecast_df.to_csv(index=False).encode('utf-8')
    st.download_button(
        label="Download Forecast CSV",
        data=csv_forecast,
        file_name=f"{ticker}_forecast.csv",
        mime='text/csv'
    )

if __name__ == "__main__":
    render(data_dict)