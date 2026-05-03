# ============================================================
#  PULSAR — App Shell & Page Router
#  Member  : Eshal Hussain (24F-0597)
#  File    : app.py
#  Project : Stock Price Volatility Analysis, Spring 2026
#
#  This file is the entry point of the entire application.
#  Run with: streamlit run app.py
# ============================================================

import streamlit as st
import page_gui
import page_dashboard
import page_statistics
import page_probability
import page_volatility
import page_correlation
import page_risk
import page_price_trend
import page_regression
from data_loader import fetch_stock_data, process_uploaded_data

# ─────────────────────────────────────────────────────────────
#  PAGE CONFIG — must be the very first Streamlit command
# ─────────────────────────────────────────────────────────────

st.set_page_config(
    page_title="PULSAR — Stock Analyzer",
    page_icon="📈",
    layout="wide",
    initial_sidebar_state="expanded"
)

# ─────────────────────────────────────────────────────────────
#  APPLY DARK THEME (from Faizan's page_gui.py)
# ─────────────────────────────────────────────────────────────

page_gui.apply_theme()

# ─────────────────────────────────────────────────────────────
#  SIDEBAR — Navigation + CSV Upload + Info
# ─────────────────────────────────────────────────────────────

with st.sidebar:
    # Logo and tagline (from Faizan's page_gui.py)
    page_gui.render_sidebar_logo()

    # Navigation
    page = st.radio(
        "Navigate",
        [
            "Dashboard Overview",
            "Price Trend Explorer",
            "Volatility Dashboard",
            "Statistical Analysis",
            "Probability Distribution",
            "Correlation Analysis",
            "Regression Forecaster",
            "Risk Comparator",
        ]
    )

    st.markdown("---")

    # CSV Upload
    st.markdown("### Upload CSV")
    uploaded = st.file_uploader(
        "Upload your own stock CSV",
        type=["csv"],
        help="File must have columns: Date, Open, High, Low, Close, Volume"
    )

    st.markdown("---")
    st.caption("Source: Yahoo Finance | 2021–2024")
    st.markdown("---")
    st.markdown("**Team Pulsar** | BCS-4F + BSE-4")

# ─────────────────────────────────────────────────────────────
#  DATA LOADING
#  fetch_stock_data() is cached — only downloads once per session
# ─────────────────────────────────────────────────────────────

@st.cache_data
def load_data():
    return fetch_stock_data()

data_dict = load_data()

# ─────────────────────────────────────────────────────────────
#  CSV UPLOAD HANDLER
#  If user uploads a file, add it to data_dict
# ─────────────────────────────────────────────────────────────

if uploaded is not None:
    uploaded_data = process_uploaded_data(uploaded)
    if uploaded_data:
        data_dict.update(uploaded_data)
        st.sidebar.success(
            f"Loaded: {list(uploaded_data.keys())[0]}"
        )

# ─────────────────────────────────────────────────────────────
#  PAGE ROUTER
#  Routes to the correct module based on sidebar selection
# ─────────────────────────────────────────────────────────────

if page == "Dashboard Overview":
    page_dashboard.render(data_dict)

elif page == "Price Trend Explorer":
    page_price_trend.render(data_dict)

elif page == "Volatility Dashboard":
    page_volatility.render(data_dict)

elif page == "Statistical Analysis":
    page_statistics.render(data_dict)

elif page == "Probability Distribution":
    page_probability.render(data_dict)

elif page == "Correlation Analysis":
    page_correlation.render(data_dict)

elif page == "Regression Forecaster":
    page_regression.render(data_dict)

elif page == "Risk Comparator":
    page_risk.render(data_dict)