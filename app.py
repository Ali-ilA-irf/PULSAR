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
import page_welcome
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
#  APP STATE & ROUTING
# ─────────────────────────────────────────────────────────────

if 'entered_app' not in st.session_state:
    st.session_state['entered_app'] = False

if not st.session_state['entered_app']:
    # Completely hide the sidebar and its toggle button on the welcome page
    st.markdown("""
        <style>
        [data-testid="stSidebar"] { display: none !important; }
        [data-testid="collapsedControl"] { display: none !important; }
        /* Remove top padding for a true full-screen landing */
        .block-container { padding-top: 1rem !important; }
        </style>
    """, unsafe_allow_html=True)
    
    page_welcome.render()

else:
    # ─────────────────────────────────────────────────────────────
    #  SIDEBAR — Navigation + CSV Upload + Info
    # ─────────────────────────────────────────────────────────────
    with st.sidebar:
        page_gui.render_sidebar_logo()
        
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
    # ─────────────────────────────────────────────────────────────
    @st.cache_data
    def load_data():
        return fetch_stock_data()
    
    data_dict = load_data()

    if uploaded is not None:
        uploaded_data = process_uploaded_data(uploaded)
        if uploaded_data:
            data_dict.update(uploaded_data)
            st.sidebar.success(f"Loaded: {list(uploaded_data.keys())[0]}")

    # ─────────────────────────────────────────────────────────────
    #  PAGE ROUTER
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