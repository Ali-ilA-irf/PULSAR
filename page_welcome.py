# page_welcome.py — Welcome Screen with Video Integration
# Author: Added via Assistant
import streamlit as st
import base64
import os

import re
def clean_html(html_str):
    return re.sub(r'\n\s*', ' ', html_str)




def render():
    video_path = "Video Project 5.mp4"
    
    if os.path.exists(video_path):
        with open(video_path, "rb") as video_file:
            video_bytes = video_file.read()
        video_base64 = base64.b64encode(video_bytes).decode()
        video_src = f"data:video/mp4;base64,{video_base64}"
    else:
        video_src = ""

    st.markdown(
        clean_html(f"""
        <style>
        .welcome-container {{
            display: flex;
            flex-direction: column;
            align-items: center;
            justify-content: center;
            width: 100%;
            height: 45vh;
            min-height: 350px;
            background: #000000;
            border: 1px solid var(--border-bright);
            border-radius: 20px;
            overflow: hidden;
            position: relative;
            margin-top: 15px;
            box-shadow: 0 0 50px rgba(56, 189, 248, 0.15);
        }}
        .welcome-video {{
            width: 100%;
            height: 100%;
            object-fit: contain;
            position: absolute;
            top: 0;
            left: 0;
            z-index: 0;
            opacity: 0.95;
        }}
        </style>
        
        <div class="welcome-container">
            <video class="welcome-video" autoplay loop muted playsinline>
                <source src="{video_src}" type="video/mp4">
            </video>
        </div>
        """),
        unsafe_allow_html=True
    )
    
    st.markdown("<div style='height: 20px;'></div>", unsafe_allow_html=True)
    
    col1, col2, col3 = st.columns([1, 2, 1])
    with col2:
        st.markdown(
            clean_html("""
            <div style="text-align: center; margin-bottom: 20px; animation: fadeInUp 1s ease both;">
                <h2 style="font-family: 'Space Grotesk', sans-serif; font-size: 28px; font-weight: 700; color: #38bdf8; margin-bottom: 15px;">
                    Welcome to Pulsar
                </h2>
                <p style="font-family: 'Space Grotesk', sans-serif; font-size: 15px; color: #e2eaf4; line-height: 1.6; margin-bottom: 20px;">
                    Pulsar is an advanced, interactive platform engineered to analyze historical stock data, 
                    price trends, and market volatility for AAPL, TSLA, and JNJ over the period 2021–2024. 
                    Leveraging sophisticated statistical models and probability methods, this tool empowers 
                    data-driven decision making and comprehensive market analysis.
                </p>
            </div>
            """),
            unsafe_allow_html=True
        )
        
        # Adding some custom CSS for the Streamlit button to make it look prominent
        st.markdown(
            clean_html("""
            <style>
            div.stButton > button {
                padding: 16px 24px;
                font-family: 'JetBrains Mono', monospace;
                font-size: 16px;
                font-weight: 700;
                letter-spacing: 0.1em;
                background: linear-gradient(135deg, #38bdf8, #a78bfa);
                color: #080c12;
                border: none;
                border-radius: 0px;
                white-space: nowrap;
                box-shadow: 0 10px 25px rgba(56, 189, 248, 0.3);
                transition: all 0.3s ease;
            }
            div.stButton > button:hover {
                transform: translateY(-3px);
                box-shadow: 0 15px 35px rgba(56, 189, 248, 0.5);
                color: #ffffff;
            }
            </style>
            """),
            unsafe_allow_html=True
        )
        
        b_col1, b_col2, b_col3 = st.columns([1, 2.5, 1])
        with b_col2:
            if st.button("🚀 LET'S MOVE TO THE DASHBOARD", width="stretch"):
                st.session_state['entered_app'] = True
                st.rerun()
            
    st.markdown("<div style='height: 20px;'></div>", unsafe_allow_html=True)
