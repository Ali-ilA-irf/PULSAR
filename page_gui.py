# page_gui.py — Full Professional UI & Theme
# Author: Muhammad Faizan (24F-3103)
# Module Contract: apply_theme(), render_sidebar_logo(), render_hero()

import streamlit as st


def apply_theme():
    st.markdown(
        """
        <style>
        @import url('https://fonts.googleapis.com/css2?family=Space+Grotesk:wght@300;400;500;600;700&family=JetBrains+Mono:wght@400;500;700&display=swap');

        /* ── Root Variables ── */
        :root {
            --bg-primary:    #080c12;
            --bg-secondary:  #0d1117;
            --bg-card:       #111820;
            --bg-card-hover: #161e28;
            --border:        #1e2d3d;
            --border-bright: #2a3f55;
            --accent-blue:   #38bdf8;
            --accent-cyan:   #22d3ee;
            --accent-green:  #4ade80;
            --accent-orange: #fb923c;
            --accent-purple: #a78bfa;
            --text-primary:  #e2eaf4;
            --text-muted:    #64748b;
            --text-dim:      #3d5166;
            --glow-blue:     rgba(56,189,248,0.12);
            --glow-cyan:     rgba(34,211,238,0.08);
        }

        /* ── Global Reset ── */
        *, *::before, *::after { box-sizing: border-box; }

        html, body, [class*="css"] {
            font-family: 'Space Grotesk', sans-serif;
            color: var(--text-primary);
        }

        /* ── App Background ── */
        .stApp {
            background:
                radial-gradient(ellipse 80% 50% at 20% 0%, rgba(56,189,248,0.05) 0%, transparent 60%),
                radial-gradient(ellipse 60% 40% at 80% 100%, rgba(167,139,250,0.04) 0%, transparent 60%),
                var(--bg-primary);
            color: var(--text-primary);
        }

        /* ── Sidebar ── */
        [data-testid="stSidebar"] {
            background:
                linear-gradient(180deg, #0d1520 0%, #080c12 100%) !important;
            border-right: 1px solid var(--border) !important;
        }
        [data-testid="stSidebar"] > div:first-child {
            padding-top: 0 !important;
        }

        /* ── Metric Cards ── */
        [data-testid="stMetric"] {
            background: linear-gradient(135deg, var(--bg-card) 0%, #0f1923 100%);
            border: 1px solid var(--border);
            border-radius: 14px;
            padding: 22px 20px 18px;
            transition: all 0.3s cubic-bezier(0.4, 0, 0.2, 1);
            position: relative;
            overflow: hidden;
        }
        [data-testid="stMetric"]::before {
            content: '';
            position: absolute;
            top: 0; left: 0; right: 0;
            height: 2px;
            background: linear-gradient(90deg, var(--accent-blue), var(--accent-cyan));
            opacity: 0;
            transition: opacity 0.3s ease;
        }
        [data-testid="stMetric"]:hover {
            transform: translateY(-4px);
            border-color: var(--border-bright);
            box-shadow: 0 12px 40px rgba(56,189,248,0.12), 0 4px 16px rgba(0,0,0,0.4);
            background: linear-gradient(135deg, var(--bg-card-hover) 0%, #131f2e 100%);
        }
        [data-testid="stMetric"]:hover::before {
            opacity: 1;
        }
        [data-testid="metric-container"] [data-testid="stMetricLabel"] {
            font-family: 'JetBrains Mono', monospace;
            font-size: 11px;
            font-weight: 500;
            letter-spacing: 0.12em;
            color: var(--text-muted);
            text-transform: uppercase;
        }
        [data-testid="metric-container"] [data-testid="stMetricValue"] {
            font-family: 'Space Grotesk', sans-serif;
            font-size: 28px;
            font-weight: 700;
            color: var(--text-primary);
            letter-spacing: -0.02em;
        }
        [data-testid="metric-container"] [data-testid="stMetricDelta"] {
            font-family: 'JetBrains Mono', monospace;
            font-size: 12px;
            font-weight: 500;
        }

        /* ── Typography ── */
        h1 {
            font-family: 'Space Grotesk', sans-serif !important;
            font-size: 32px !important;
            font-weight: 700 !important;
            letter-spacing: -0.03em !important;
            color: var(--text-primary) !important;
            border-bottom: 1px solid var(--border) !important;
            padding-bottom: 12px !important;
            margin-bottom: 8px !important;
        }
        h2 {
            font-family: 'Space Grotesk', sans-serif !important;
            font-size: 20px !important;
            font-weight: 600 !important;
            color: var(--accent-blue) !important;
            letter-spacing: -0.01em !important;
        }
        h3 {
            font-family: 'Space Grotesk', sans-serif !important;
            font-weight: 600 !important;
            color: var(--text-primary) !important;
        }
        p, li, span {
            font-family: 'Space Grotesk', sans-serif;
            color: var(--text-primary);
        }

        /* ── Buttons ── */
        .stButton > button {
            background: linear-gradient(135deg, #1a3a5c, #0f2840);
            color: var(--accent-blue);
            border: 1px solid var(--border-bright);
            border-radius: 8px;
            font-family: 'JetBrains Mono', monospace;
            font-size: 12px;
            font-weight: 500;
            letter-spacing: 0.05em;
            padding: 10px 20px;
            transition: all 0.25s ease;
        }
        .stButton > button:hover {
            background: linear-gradient(135deg, #1e4570, #132f50);
            border-color: var(--accent-blue);
            color: #fff;
            box-shadow: 0 0 20px rgba(56,189,248,0.2);
            transform: translateY(-1px);
        }

        /* ── Download Button ── */
        .stDownloadButton > button {
            background: linear-gradient(135deg, #164430, #0e2d1e);
            color: var(--accent-green);
            border: 1px solid #2a4a3a;
            border-radius: 8px;
            font-family: 'JetBrains Mono', monospace;
            font-size: 12px;
            font-weight: 500;
            letter-spacing: 0.05em;
            transition: all 0.25s ease;
        }
        .stDownloadButton > button:hover {
            background: linear-gradient(135deg, #1a5238, #113525);
            border-color: var(--accent-green);
            box-shadow: 0 0 20px rgba(74,222,128,0.15);
            transform: translateY(-1px);
        }

        /* ── Select / Inputs ── */
        .stSelectbox div[data-baseweb="select"],
        .stMultiSelect div[data-baseweb="select"] {
            background-color: var(--bg-card) !important;
            border: 1px solid var(--border) !important;
            border-radius: 8px !important;
            font-family: 'Space Grotesk', sans-serif !important;
        }
        .stSelectbox div[data-baseweb="select"]:focus-within,
        .stMultiSelect div[data-baseweb="select"]:focus-within {
            border-color: var(--accent-blue) !important;
            box-shadow: 0 0 0 2px rgba(56,189,248,0.15) !important;
        }
        [data-baseweb="menu"] {
            background-color: var(--bg-card) !important;
            border: 1px solid var(--border-bright) !important;
            border-radius: 8px !important;
        }

        /* ── Sliders ── */
        [data-testid="stSlider"] > div > div > div > div {
            background: linear-gradient(90deg, var(--accent-blue), var(--accent-cyan)) !important;
        }

        /* ── Radio Buttons ── */
        .stRadio label {
            font-family: 'Space Grotesk', sans-serif !important;
            font-size: 13px !important;
            font-weight: 500 !important;
            color: var(--text-muted) !important;
            transition: color 0.2s;
        }
        .stRadio label:hover { color: var(--accent-blue) !important; }

        /* ── DataFrames ── */
        .stDataFrame {
            border: 1px solid var(--border) !important;
            border-radius: 10px !important;
            overflow: hidden !important;
        }
        [data-testid="stDataFrameResizable"] {
            background: var(--bg-card) !important;
        }

        /* ── Info / Success / Warning Boxes ── */
        [data-testid="stAlert"] {
            background: var(--bg-card) !important;
            border-radius: 10px !important;
            border: 1px solid var(--border) !important;
        }
        div[data-baseweb="notification"] {
            border-radius: 10px !important;
        }

        /* ── Divider ── */
        hr {
            border: none !important;
            border-top: 1px solid var(--border) !important;
            margin: 20px 0 !important;
        }

        /* ── Caption Text ── */
        .stCaption, [data-testid="stCaptionContainer"] {
            font-family: 'JetBrains Mono', monospace !important;
            font-size: 11px !important;
            color: var(--text-muted) !important;
            letter-spacing: 0.04em !important;
        }

        /* ── Scrollbar ── */
        ::-webkit-scrollbar       { width: 5px; height: 5px; }
        ::-webkit-scrollbar-track { background: var(--bg-primary); }
        ::-webkit-scrollbar-thumb {
            background: var(--border-bright);
            border-radius: 3px;
        }
        ::-webkit-scrollbar-thumb:hover { background: #3d5a75; }

        /* ── Plotly Chart Wrapper ── */
        [data-testid="stPlotlyChart"] {
            border: 1px solid var(--border);
            border-radius: 12px;
            overflow: hidden;
            transition: border-color 0.3s ease;
        }
        [data-testid="stPlotlyChart"]:hover {
            border-color: var(--border-bright);
        }

        /* ── Sidebar Nav Styles ── */
        .sidebar-nav-item {
            font-family: 'JetBrains Mono', monospace;
            font-size: 11px;
            letter-spacing: 0.08em;
        }

        /* ── Fade-in Animation ── */
        @keyframes fadeInUp {
            from { opacity: 0; transform: translateY(18px); }
            to   { opacity: 1; transform: translateY(0); }
        }
        .main > div { animation: fadeInUp 0.45s ease both; }

        /* ── Ticker Badge ── */
        .ticker-badge {
            display: inline-block;
            font-family: 'JetBrains Mono', monospace;
            font-size: 10px;
            font-weight: 700;
            letter-spacing: 0.12em;
            padding: 3px 8px;
            border-radius: 4px;
            border: 1px solid var(--border-bright);
            color: var(--accent-blue);
            background: rgba(56,189,248,0.07);
            margin: 0 3px;
        }

        /* ── Glow Pulse ── */
        @keyframes glowPulse {
            0%, 100% { box-shadow: 0 0 20px rgba(56,189,248,0.08); }
            50%       { box-shadow: 0 0 35px rgba(56,189,248,0.18); }
        }
        </style>
        """,
        unsafe_allow_html=True,
    )


def render_sidebar_logo():
    st.markdown(
        """
        <div style="
            padding: 28px 16px 16px;
            border-bottom: 1px solid #1e2d3d;
            margin-bottom: 8px;
        ">
            <div style="
                font-family: 'JetBrains Mono', monospace;
                font-size: 22px;
                font-weight: 700;
                letter-spacing: 0.25em;
                background: linear-gradient(90deg, #38bdf8 0%, #22d3ee 50%, #a78bfa 100%);
                -webkit-background-clip: text;
                -webkit-text-fill-color: transparent;
                background-clip: text;
                text-align: center;
                margin-bottom: 4px;
            ">⬡ PULSAR</div>
            <div style="
                font-family: 'JetBrains Mono', monospace;
                font-size: 9px;
                letter-spacing: 0.22em;
                color: #3d5166;
                text-align: center;
                text-transform: uppercase;
                margin-bottom: 6px;
            ">STOCK VOLATILITY ANALYZER</div>
            <div style="
                display: flex;
                justify-content: center;
                gap: 6px;
                margin-top: 10px;
            ">
                <span style="
                    font-family: 'JetBrains Mono', monospace;
                    font-size: 9px;
                    font-weight: 700;
                    letter-spacing: 0.1em;
                    padding: 2px 7px;
                    border-radius: 3px;
                    border: 1px solid #1e2d3d;
                    color: #38bdf8;
                    background: rgba(56,189,248,0.06);
                ">AAPL</span>
                <span style="
                    font-family: 'JetBrains Mono', monospace;
                    font-size: 9px;
                    font-weight: 700;
                    letter-spacing: 0.1em;
                    padding: 2px 7px;
                    border-radius: 3px;
                    border: 1px solid #1e2d3d;
                    color: #fb923c;
                    background: rgba(251,146,60,0.06);
                ">TSLA</span>
                <span style="
                    font-family: 'JetBrains Mono', monospace;
                    font-size: 9px;
                    font-weight: 700;
                    letter-spacing: 0.1em;
                    padding: 2px 7px;
                    border-radius: 3px;
                    border: 1px solid #1e2d3d;
                    color: #4ade80;
                    background: rgba(74,222,128,0.06);
                ">JNJ</span>
            </div>
        </div>
        """,
        unsafe_allow_html=True,
    )


def render_hero():
    st.markdown(
        """
        <div style="
            position: relative;
            text-align: center;
            padding: 56px 32px 48px;
            background:
                radial-gradient(ellipse 70% 60% at 50% 0%, rgba(56,189,248,0.08) 0%, transparent 70%),
                linear-gradient(135deg, #0d1520 0%, #080c12 100%);
            border-radius: 16px;
            border: 1px solid #1e2d3d;
            margin-bottom: 32px;
            overflow: hidden;
        ">
            <!-- Decorative grid lines -->
            <div style="
                position: absolute;
                inset: 0;
                background-image:
                    linear-gradient(rgba(56,189,248,0.03) 1px, transparent 1px),
                    linear-gradient(90deg, rgba(56,189,248,0.03) 1px, transparent 1px);
                background-size: 40px 40px;
                border-radius: 16px;
                pointer-events: none;
            "></div>

            <!-- Top accent line -->
            <div style="
                position: absolute;
                top: 0; left: 20%; right: 20%;
                height: 1px;
                background: linear-gradient(90deg, transparent, #38bdf8, #a78bfa, transparent);
            "></div>

            <!-- Status pill -->
            <div style="
                display: inline-flex;
                align-items: center;
                gap: 7px;
                font-family: 'JetBrains Mono', monospace;
                font-size: 10px;
                letter-spacing: 0.14em;
                color: #4ade80;
                background: rgba(74,222,128,0.08);
                border: 1px solid rgba(74,222,128,0.2);
                border-radius: 20px;
                padding: 5px 14px;
                margin-bottom: 24px;
            ">
                <span style="
                    width: 6px; height: 6px;
                    border-radius: 50%;
                    background: #4ade80;
                    display: inline-block;
                    animation: glowPulse 2s ease-in-out infinite;
                "></span>
                LIVE DATA · 2021–2024 · YAHOO FINANCE
            </div>

            <!-- Title -->
            <div style="
                font-family: 'JetBrains Mono', monospace;
                font-size: clamp(36px, 6vw, 60px);
                font-weight: 700;
                letter-spacing: 0.3em;
                background: linear-gradient(90deg, #38bdf8 0%, #e2eaf4 40%, #a78bfa 100%);
                -webkit-background-clip: text;
                -webkit-text-fill-color: transparent;
                background-clip: text;
                margin-bottom: 10px;
                line-height: 1.1;
            ">⬡ PULSAR</div>

            <!-- Subtitle -->
            <div style="
                font-family: 'Space Grotesk', sans-serif;
                font-size: 13px;
                font-weight: 400;
                letter-spacing: 0.2em;
                color: #64748b;
                text-transform: uppercase;
                margin-bottom: 28px;
            ">Stock Price Volatility Analyzer</div>

            <!-- Ticker chips row -->
            <div style="
                display: flex;
                justify-content: center;
                align-items: center;
                gap: 12px;
                flex-wrap: wrap;
            ">
                <div style="
                    font-family: 'JetBrains Mono', monospace;
                    font-size: 11px;
                    font-weight: 700;
                    letter-spacing: 0.12em;
                    padding: 8px 20px;
                    border-radius: 8px;
                    border: 1px solid rgba(56,189,248,0.3);
                    color: #38bdf8;
                    background: rgba(56,189,248,0.08);
                ">AAPL</div>
                <div style="
                    color: #1e2d3d;
                    font-size: 18px;
                ">—</div>
                <div style="
                    font-family: 'JetBrains Mono', monospace;
                    font-size: 11px;
                    font-weight: 700;
                    letter-spacing: 0.12em;
                    padding: 8px 20px;
                    border-radius: 8px;
                    border: 1px solid rgba(251,146,60,0.3);
                    color: #fb923c;
                    background: rgba(251,146,60,0.08);
                ">TSLA</div>
                <div style="
                    color: #1e2d3d;
                    font-size: 18px;
                ">—</div>
                <div style="
                    font-family: 'JetBrains Mono', monospace;
                    font-size: 11px;
                    font-weight: 700;
                    letter-spacing: 0.12em;
                    padding: 8px 20px;
                    border-radius: 8px;
                    border: 1px solid rgba(74,222,128,0.3);
                    color: #4ade80;
                    background: rgba(74,222,128,0.08);
                ">JNJ</div>
            </div>
        </div>
        """,
        unsafe_allow_html=True,
    )
