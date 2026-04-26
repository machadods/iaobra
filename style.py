import streamlit as st

def load_css():
    st.markdown("""
    <style>
    @import url('https://fonts.googleapis.com/css2?family=Inter:wght@300;400;500;600;700;800;900&display=swap');

    /* BASE */
    html, body, [data-testid="stAppViewContainer"] {
        background: #07090f !important;
        font-family: 'Inter', -apple-system, sans-serif !important;
        color: #cbd5e1 !important;
    }

    [data-testid="stMain"], .main .block-container {
        background: transparent !important;
        padding: 1.5rem 2.5rem !important;
        max-width: 1300px !important;
    }

    /* SIDEBAR */
    [data-testid="stSidebar"] {
        background: #0d1117 !important;
        border-right: 1px solid #1e2433 !important;
    }

    [data-testid="stSidebar"] > div:first-child {
        padding-top: 1.5rem !important;
    }

    [data-testid="stSidebarContent"] p,
    [data-testid="stSidebarContent"] small,
    [data-testid="stSidebarContent"] span {
        color: #4b5563 !important;
        font-size: 0.82rem !important;
    }

    [data-testid="stSidebarContent"] strong,
    [data-testid="stSidebarContent"] b {
        color: #94a3b8 !important;
    }

    [data-testid="stSidebarContent"] h3 {
        color: #e2e8f0 !important;
        font-size: 1.1rem !important;
        font-weight: 700 !important;
        letter-spacing: -0.3px;
    }

    /* BOTOES SIDEBAR */
    [data-testid="stSidebar"] .stButton > button {
        background: transparent !important;
        border: 1px solid #1e2433 !important;
        color: #64748b !important;
        border-radius: 8px !important;
        font-size: 0.82rem !important;
        font-weight: 500 !important;
        padding: 0.55rem 1rem !important;
        text-align: left !important;
        transition: all 0.18s ease !important;
        box-shadow: none !important;
        letter-spacing: 0.01em;
    }

    [data-testid="stSidebar"] .stButton > button:hover {
        background: #111827 !important;
        border-color: #2d3a4f !important;
        color: #e2e8f0 !important;
        transform: none !important;
        box-shadow: none !important;
    }

    /* BOTOES PRINCIPAIS */
    .stButton > button {
        background: #1a2235 !important;
        color: #e2e8f0 !important;
        border: 1px solid #2d3a4f !important;
        border-radius: 8px !important;
        font-weight: 600 !important;
        font-size: 0.88rem !important;
        padding: 0.6rem 1.4rem !important;
        transition: all 0.18s ease !important;
        box-shadow: none !important;
        letter-spacing: 0.01em;
    }

    .stButton > button:hover {
        background: #1e293b !important;
        border-color: #3b4f6e !important;
        color: #f1f5f9 !important;
        box-shadow: none !important;
        transform: none !important;
    }

    /* BOTAO DE SUBMIT — laranja discreta */
    [data-testid="stForm"] .stButton > button {
        background: #c2410c !important;
        color: #fff !important;
        border-color: #c2410c !important;
    }
    [data-testid="stForm"] .stButton > button:hover {
        background: #d4500f !important;
        border-color: #d4500f !important;
    }

    /* INPUTS */
    [data-testid="stTextInput"] input,
    [data-testid="stTextArea"] textarea,
    [data-testid="stNumberInput"] input {
        background: #0d1117 !important;
        border: 1px solid #1e2433 !important;
        border-radius: 8px !important;
        color: #cbd5e1 !important;
        font-family: 'Inter', sans-serif !important;
        font-size: 0.9rem !important;
    }

    [data-testid="stTextInput"] input:focus,
    [data-testid="stTextArea"] textarea:focus {
        border-color: #2d3a4f !important;
        box-shadow: none !important;
        outline: none !important;
    }

    label, [data-testid="stWidgetLabel"] p {
        color: #475569 !important;
        font-size: 0.76rem !important;
        font-weight: 600 !important;
        text-transform: uppercase !important;
        letter-spacing: 0.08em !important;
    }

    /* SELECT */
    [data-testid="stSelectbox"] > div > div {
        background: #0d1117 !important;
        border: 1px solid #1e2433 !important;
        border-radius: 8px !important;
        color: #cbd5e1 !important;
    }

    /* MULTISELECT */
    [data-testid="stMultiSelect"] > div > div {
        background: #0d1117 !important;
        border: 1px solid #1e2433 !important;
        border-radius: 8px !important;
    }

    /* METRICAS */
    [data-testid="stMetric"] {
        background: #0d1117 !important;
        border: 1px solid #1e2433 !important;
        border-radius: 10px !important;
        padding: 1.1rem 1.3rem !important;
    }

    [data-testid="stMetricLabel"] p {
        color: #475569 !important;
        font-size: 0.73rem !important;
        font-weight: 600 !important;
        text-transform: uppercase !important;
        letter-spacing: 0.08em !important;
    }

    [data-testid="stMetricValue"] {
        color: #e2e8f0 !important;
        font-size: 1.8rem !important;
        font-weight: 800 !important;
        letter-spacing: -0.5px !important;
    }

    /* ABAS */
    [data-testid="stTabs"] [role="tablist"] {
        background: transparent !important;
        border-bottom: 1px solid #1e2433 !important;
        padding: 0 !important;
        gap: 0 !important;
    }

    [data-testid="stTabs"] [role="tab"] {
        background: transparent !important;
        color: #475569 !important;
        border-radius: 0 !important;
        font-weight: 500 !important;
        font-size: 0.84rem !important;
        padding: 0.6rem 1.2rem !important;
        border: none !important;
        border-bottom: 2px solid transparent !important;
        transition: all 0.18s ease !important;
    }

    [data-testid="stTabs"] [role="tab"][aria-selected="true"] {
        background: transparent !important;
        color: #e2e8f0 !important;
        border-bottom: 2px solid #c2410c !important;
        font-weight: 600 !important;
    }

    [data-testid="stTabs"] [role="tab"]:hover:not([aria-selected="true"]) {
        color: #94a3b8 !important;
        background: transparent !important;
    }

    /* ALERTS */
    [data-testid="stAlert"] {
        border-radius: 8px !important;
        font-size: 0.87rem !important;
    }

    /* EXPANDER */
    [data-testid="stExpander"] {
        background: #0d1117 !important;
        border: 1px solid #1e2433 !important;
        border-radius: 8px !important;
    }

    /* CHAT */
    [data-testid="stChatMessage"] {
        background: #0d1117 !important;
        border: 1px solid #1e2433 !important;
        border-radius: 10px !important;
    }

    /* DIVIDER */
    hr {
        border-color: #1e2433 !important;
        margin: 1.2rem 0 !important;
    }

    /* SCROLLBAR */
    ::-webkit-scrollbar { width: 4px; height: 4px; }
    ::-webkit-scrollbar-track { background: #07090f; }
    ::-webkit-scrollbar-thumb { background: #1e2433; border-radius: 4px; }
    ::-webkit-scrollbar-thumb:hover { background: #2d3a4f; }

    /* OCULTAR ELEMENTOS PADRAO STREAMLIT */
    #MainMenu, footer { visibility: hidden !important; }
    [data-testid="stDecoration"] { display: none !important; }
    [data-testid="stHeader"] { background: transparent !important; }

    /* CARD */
    .card {
        background: #0d1117;
        border: 1px solid #1e2433;
        border-radius: 10px;
        padding: 1.4rem;
        margin-bottom: 1rem;
    }

    .card-accent {
        border-left: 2px solid #c2410c;
    }

    .badge {
        display: inline-block;
        background: rgba(194,65,12,0.12);
        border: 1px solid rgba(194,65,12,0.25);
        color: #ea580c;
        font-size: 0.7rem;
        font-weight: 700;
        letter-spacing: 0.12em;
        text-transform: uppercase;
        padding: 3px 10px;
        border-radius: 20px;
    }
    </style>
    """, unsafe_allow_html=True)
