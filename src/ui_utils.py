import pandas as pd
import streamlit as st


# ============================================================
# DATA FILES
# ============================================================

RESULT_FILE = "data/final_risk_results.csv"
TRANSACTION_FILE = "data/transactions.csv"
ML_EVALUATION_FILE = "data/ml_evaluation_summary.csv"
FEATURE_IMPORTANCE_FILE = "data/ml_feature_importance.csv"
MODEL_COMPARISON_FILE = "data/model_comparison.csv"


# ============================================================
# DATA LOADING
# ============================================================

@st.cache_data
def load_final_results():
    return pd.read_csv(
        RESULT_FILE,
        keep_default_na=False,
    )


@st.cache_data
def load_transactions():
    return pd.read_csv(
        TRANSACTION_FILE,
        keep_default_na=False,
    )


@st.cache_data
def load_ml_evaluation():
    return pd.read_csv(
        ML_EVALUATION_FILE,
        keep_default_na=False,
    )


@st.cache_data
def load_feature_importance():
    return pd.read_csv(
        FEATURE_IMPORTANCE_FILE,
        keep_default_na=False,
    )


@st.cache_data
def load_model_comparison():
    return pd.read_csv(
        MODEL_COMPARISON_FILE,
        keep_default_na=False,
    )


# ============================================================
# GLOBAL PAGE SETUP
# ============================================================

def setup_page(title, icon="🛡️"):

    st.set_page_config(
        page_title=f"RiskGraph AI | {title}",
        page_icon=icon,
        layout="wide",
        initial_sidebar_state="expanded",
    )

    st.markdown(
        """
        <style>

        /* =====================================================
           GLOBAL
        ===================================================== */

        #MainMenu {
            visibility: hidden;
        }

        footer {
            visibility: hidden;
        }

        header {
            background: transparent !important;
        }

        html,
        body,
        .stApp {
            font-family:
                Inter,
                ui-sans-serif,
                system-ui,
                -apple-system,
                BlinkMacSystemFont,
                "Segoe UI",
                sans-serif;
        }

        .stApp {
            background:
                radial-gradient(
                    circle at 85% 0%,
                    rgba(37, 99, 235, 0.10),
                    transparent 30%
                ),
                radial-gradient(
                    circle at 20% 100%,
                    rgba(14, 165, 233, 0.05),
                    transparent 25%
                ),
                #070b14;
        }

        .block-container {
            max-width: 1500px !important;

            padding-top: 2.5rem !important;
            padding-bottom: 4rem !important;

            padding-left: 3.5rem !important;
            padding-right: 3.5rem !important;
        }


        /* =====================================================
           SIDEBAR
        ===================================================== */

        section[data-testid="stSidebar"] {
            width: 300px !important;
            min-width: 300px !important;

            background:
                linear-gradient(
                    180deg,
                    #0b1222 0%,
                    #080d18 55%,
                    #070b14 100%
                ) !important;

            border-right: 1px solid #1e2a42;
        }

        section[data-testid="stSidebar"] > div {
            width: 300px !important;
        }

        section[data-testid="stSidebar"] .block-container {
            padding-top: 1.6rem !important;
            padding-left: 1.25rem !important;
            padding-right: 1.25rem !important;
        }


        /* =====================================================
           SIDEBAR BRAND
        ===================================================== */

        .sidebar-brand-box {
            padding: 18px 16px 16px 16px;

            border-radius: 16px;

            background:
                linear-gradient(
                    145deg,
                    rgba(30, 64, 175, 0.22),
                    rgba(15, 23, 42, 0.70)
                );

            border: 1px solid #243554;

            box-shadow:
                0 12px 30px rgba(0, 0, 0, 0.20);

            margin-bottom: 18px;
        }

        .sidebar-brand {
            display: flex;
            align-items: center;
            gap: 10px;

            color: #f8fafc;

            font-size: 21px;
            font-weight: 800;

            letter-spacing: -0.5px;
        }

        .sidebar-brand-icon {
            display: flex;
            align-items: center;
            justify-content: center;

            width: 38px;
            height: 38px;

            border-radius: 11px;

            background:
                linear-gradient(
                    135deg,
                    #2563eb,
                    #38bdf8
                );

            box-shadow:
                0 0 22px rgba(37, 99, 235, 0.35);

            font-size: 20px;
        }

        .sidebar-subtitle {
            color: #7f8da5;

            font-size: 10px;
            font-weight: 700;

            text-transform: uppercase;
            letter-spacing: 1.5px;

            margin-top: 10px;
        }

        .sidebar-description {
            color: #64748b;

            font-size: 12px;
            line-height: 1.5;

            margin-top: 7px;
        }


        /* =====================================================
           SYSTEM STATUS
        ===================================================== */

        .sidebar-status {
            display: flex;
            align-items: center;
            gap: 9px;

            padding: 10px 12px;

            border-radius: 10px;

            background: rgba(34, 197, 94, 0.06);

            border: 1px solid rgba(34, 197, 94, 0.16);

            color: #86efac;

            font-size: 12px;
            font-weight: 700;

            margin-bottom: 18px;
        }

        .sidebar-status-dot {
            width: 8px;
            height: 8px;

            border-radius: 50%;

            background: #22c55e;

            box-shadow:
                0 0 12px rgba(34, 197, 94, 0.85);
        }


        /* =====================================================
           STREAMLIT SIDEBAR NAVIGATION
        ===================================================== */

        div[data-testid="stSidebarNav"] {
            padding-top: 0.2rem;
        }

        div[data-testid="stSidebarNav"] ul {
            gap: 6px;
        }

        div[data-testid="stSidebarNav"] li {
            margin: 0 !important;
        }

        div[data-testid="stSidebarNav"] a {
            min-height: 44px !important;

            padding: 10px 13px !important;

            border-radius: 10px !important;

            color: #aebbd0 !important;

            font-size: 14px !important;
            font-weight: 600 !important;

            transition:
                background 0.15s ease,
                color 0.15s ease,
                transform 0.15s ease;
        }

        div[data-testid="stSidebarNav"] a:hover {
            background: rgba(59, 130, 246, 0.09) !important;

            color: #e2e8f0 !important;

            transform: translateX(2px);
        }

        div[data-testid="stSidebarNav"] a[aria-current="page"] {
            background:
                linear-gradient(
                    90deg,
                    rgba(37, 99, 235, 0.24),
                    rgba(37, 99, 235, 0.08)
                ) !important;

            color: #ffffff !important;

            border: 1px solid rgba(96, 165, 250, 0.20);

            box-shadow:
                inset 3px 0 0 #3b82f6,
                0 5px 18px rgba(0, 0, 0, 0.15);
        }


        /* =====================================================
           SIDEBAR DIVIDER
        ===================================================== */

        section[data-testid="stSidebar"] hr {
            border-color: #1e2a42 !important;

            margin-top: 20px !important;
            margin-bottom: 20px !important;
        }


        /* =====================================================
           MAIN PAGE HEADER
        ===================================================== */

        .page-header {
            position: relative;

            padding: 24px 28px;

            margin-bottom: 28px;

            border-radius: 16px;

            background:
                linear-gradient(
                    135deg,
                    rgba(15, 23, 42, 0.92),
                    rgba(10, 17, 31, 0.88)
                );

            border: 1px solid #1f304d;

            box-shadow:
                0 15px 40px rgba(0, 0, 0, 0.20);

            overflow: hidden;
        }

        .page-header::after {
            content: "";

            position: absolute;

            width: 180px;
            height: 180px;

            right: -60px;
            top: -80px;

            border-radius: 50%;

            background:
                radial-gradient(
                    circle,
                    rgba(59, 130, 246, 0.16),
                    transparent 68%
                );
        }

        .page-kicker {
            color: #60a5fa;

            font-size: 11px;
            font-weight: 800;

            letter-spacing: 2.4px;
            text-transform: uppercase;

            margin-bottom: 8px;
        }

        .page-title {
            color: #f8fafc;

            font-size: 38px;
            font-weight: 800;

            letter-spacing: -1.2px;
            line-height: 1.1;

            margin: 0;
        }

        .page-subtitle {
            color: #94a3b8;

            font-size: 15px;
            line-height: 1.6;

            margin-top: 9px;

            max-width: 850px;
        }


        /* =====================================================
           GENERAL TYPOGRAPHY
        ===================================================== */

        .stMarkdown p {
            font-size: 15px;
        }

        h1 {
            font-size: 38px !important;
        }

        h2 {
            font-size: 29px !important;
        }

        h3 {
            font-size: 23px !important;
        }

        h4 {
            font-size: 19px !important;
        }

        label {
            font-size: 14px !important;
            font-weight: 650 !important;
        }


        /* =====================================================
           HERO
        ===================================================== */

        .hero {
            position: relative;

            display: flex;
            justify-content: space-between;
            align-items: center;

            min-height: 200px;

            padding: 34px 38px;

            margin-bottom: 30px;

            border-radius: 20px;

            background:
                radial-gradient(
                    circle at 90% 20%,
                    rgba(59, 130, 246, 0.18),
                    transparent 35%
                ),
                linear-gradient(
                    135deg,
                    #101b30,
                    #0c1526 60%,
                    #09111f
                );

            border: 1px solid #263b5c;

            box-shadow:
                0 20px 50px rgba(0, 0, 0, 0.25);
        }

        .hero-kicker {
            color: #60a5fa;

            font-size: 11px;
            font-weight: 800;

            letter-spacing: 2.2px;

            margin-bottom: 10px;
        }

        .hero-title {
            color: #f8fafc;

            font-size: 46px;
            font-weight: 850;

            letter-spacing: -2px;

            line-height: 1.05;
        }

        .hero-description {
            color: #94a3b8;

            font-size: 15px;
            line-height: 1.6;

            margin-top: 11px;

            max-width: 650px;
        }

        .hero-status {
            display: flex;
            align-items: center;

            padding: 10px 15px;

            border-radius: 999px;

            background: rgba(34, 197, 94, 0.08);

            border: 1px solid rgba(34, 197, 94, 0.22);

            color: #4ade80;

            font-size: 12px;
            font-weight: 800;

            letter-spacing: 0.8px;
        }

        .status-dot {
            width: 8px;
            height: 8px;

            margin-right: 8px;

            border-radius: 50%;

            background: #4ade80;

            box-shadow:
                0 0 13px rgba(74, 222, 128, 0.85);
        }


        /* =====================================================
           SECTION LABELS
        ===================================================== */

        .section-label {
            color: #71819a;

            font-size: 11px;
            font-weight: 800;

            letter-spacing: 2px;
            text-transform: uppercase;

            margin-bottom: 14px;
        }

        .panel-title {
            color: #f1f5f9;

            font-size: 22px;
            font-weight: 750;

            letter-spacing: -0.4px;

            margin-bottom: 4px;
        }

        .section-subtitle {
            color: #8190a8;

            font-size: 13px;

            margin-bottom: 16px;
        }


        /* =====================================================
           KPI CARDS
        ===================================================== */

        .kpi-card {
            position: relative;

            min-height: 155px;

            padding: 21px;

            border-radius: 15px;

            background:
                linear-gradient(
                    145deg,
                    #111b2d,
                    #0e1727
                );

            border: 1px solid #273a59;

            box-shadow:
                0 10px 28px rgba(0, 0, 0, 0.18);

            transition:
                transform 0.15s ease,
                border-color 0.15s ease;
        }

        .kpi-card:hover {
            transform: translateY(-3px);

            border-color: #3d5c87;
        }

        .kpi-icon {
            display: flex;

            width: 36px;
            height: 36px;

            align-items: center;
            justify-content: center;

            border-radius: 10px;

            background: rgba(59, 130, 246, 0.12);

            color: #60a5fa;

            font-size: 15px;
            font-weight: 800;

            margin-bottom: 15px;
        }

        .kpi-label {
            color: #8190a8;

            font-size: 10px;
            font-weight: 800;

            letter-spacing: 1.4px;
        }

        .kpi-value {
            color: #f8fafc;

            font-size: 34px;
            font-weight: 800;

            letter-spacing: -1px;

            margin-top: 3px;
        }

        .kpi-caption {
            color: #64748b;

            font-size: 12px;

            margin-top: 5px;
        }

        .kpi-card.danger .kpi-icon {
            background: rgba(239, 68, 68, 0.13);
            color: #f87171;
        }

        .kpi-card.warning .kpi-icon {
            background: rgba(245, 158, 11, 0.13);
            color: #fbbf24;
        }

        .kpi-card.blue .kpi-icon {
            background: rgba(59, 130, 246, 0.13);
            color: #60a5fa;
        }

        .kpi-card.success .kpi-icon {
            background: rgba(34, 197, 94, 0.13);
            color: #4ade80;
        }


        /* =====================================================
           BADGES / PILLS
        ===================================================== */

        .badge {
            display: inline-flex;
            align-items: center;
            gap: 6px;

            padding: 5px 13px;

            border-radius: 999px;

            font-size: 12px;
            font-weight: 800;

            letter-spacing: 0.3px;

            white-space: nowrap;
        }

        .badge-high {
            background: rgba(239, 68, 68, 0.14);
            color: #f87171;
            border: 1px solid rgba(239, 68, 68, 0.35);
        }

        .badge-medium {
            background: rgba(245, 158, 11, 0.14);
            color: #fbbf24;
            border: 1px solid rgba(245, 158, 11, 0.35);
        }

        .badge-low {
            background: rgba(34, 197, 94, 0.14);
            color: #4ade80;
            border: 1px solid rgba(34, 197, 94, 0.35);
        }

        .badge-neutral {
            background: rgba(148, 163, 184, 0.12);
            color: #cbd5e1;
            border: 1px solid rgba(148, 163, 184, 0.28);
        }

        .stat-label {
            color: #8190a8;

            font-size: 10px;
            font-weight: 800;

            letter-spacing: 1.4px;
            text-transform: uppercase;

            margin-bottom: 8px;
        }


        /* =====================================================
           PROGRESS BARS
        ===================================================== */

        .progress-track {
            width: 100%;
            height: 8px;

            border-radius: 999px;

            background: #161f34;

            overflow: hidden;

            margin-top: 8px;
        }

        .progress-fill {
            height: 100%;

            border-radius: 999px;
        }

        .progress-fill.danger {
            background: linear-gradient(90deg, #ef4444, #f87171);
        }

        .progress-fill.warning {
            background: linear-gradient(90deg, #f59e0b, #fbbf24);
        }

        .progress-fill.success {
            background: linear-gradient(90deg, #22c55e, #4ade80);
        }

        .progress-fill.blue {
            background: linear-gradient(90deg, #2563eb, #38bdf8);
        }

        .progress-caption {
            display: flex;
            justify-content: space-between;

            color: #64748b;

            font-size: 11px;
            font-weight: 650;

            margin-top: 6px;
        }


        /* =====================================================
           INFO / FEATURE CARDS
        ===================================================== */

        .info-card {
            height: 100%;

            padding: 20px;

            border-radius: 15px;

            background:
                linear-gradient(
                    145deg,
                    #111b2d,
                    #0e1727
                );

            border: 1px solid #273a59;

            box-shadow:
                0 10px 24px rgba(0, 0, 0, 0.16);
        }

        .info-card-icon {
            display: flex;

            width: 40px;
            height: 40px;

            align-items: center;
            justify-content: center;

            border-radius: 11px;

            background: rgba(59, 130, 246, 0.13);

            font-size: 18px;

            margin-bottom: 14px;
        }

        .info-card-title {
            color: #f1f5f9;

            font-size: 16px;
            font-weight: 750;

            margin-bottom: 7px;
        }

        .info-card-text {
            color: #94a3b8;

            font-size: 13px;
            line-height: 1.6;
        }


        /* =====================================================
           STEP TIMELINE
        ===================================================== */

        .step-timeline {
            border-radius: 15px;

            padding: 6px 24px;

            background:
                linear-gradient(
                    145deg,
                    #111b2d,
                    #0e1727
                );

            border: 1px solid #273a59;
        }

        .step-row {
            display: flex;

            gap: 18px;

            padding: 18px 0;
        }

        .step-row:not(:last-child) {
            border-bottom: 1px solid #1c2740;
        }

        .step-index {
            display: flex;

            width: 36px;
            height: 36px;

            flex-shrink: 0;

            align-items: center;
            justify-content: center;

            border-radius: 10px;

            background: linear-gradient(135deg, #2563eb, #38bdf8);

            color: #ffffff;

            font-size: 14px;
            font-weight: 800;

            box-shadow: 0 0 16px rgba(37, 99, 235, 0.30);
        }

        .step-body-title {
            color: #f1f5f9;

            font-size: 15px;
            font-weight: 750;

            margin-bottom: 3px;
        }

        .step-body-text {
            color: #8b98ae;

            font-size: 13px;

            line-height: 1.5;
        }


        /* =====================================================
           TABS
        ===================================================== */

        div[data-baseweb="tab-list"] {
            gap: 4px;

            border-bottom: 1px solid #1e2a42;
        }

        button[data-baseweb="tab"] {
            color: #8190a8 !important;

            font-size: 14px !important;
            font-weight: 700 !important;

            padding: 10px 18px !important;
        }

        button[data-baseweb="tab"][aria-selected="true"] {
            color: #60a5fa !important;
        }

        div[data-baseweb="tab-highlight"] {
            background-color: #3b82f6 !important;
        }


        /* =====================================================
           THREAT PANEL
        ===================================================== */

        .threat-panel {
            min-height: 320px;

            padding: 21px;

            border-radius: 15px;

            background:
                linear-gradient(
                    145deg,
                    #111b2d,
                    #0e1727
                );

            border: 1px solid #273a59;
        }

        .threat-row {
            display: flex;

            justify-content: space-between;
            align-items: center;

            padding: 15px 4px;

            color: #cbd5e1;

            font-size: 14px;
        }

        .threat-row strong {
            color: #f8fafc;
            font-size: 18px;
        }

        .threat-dot {
            display: inline-block;

            width: 9px;
            height: 9px;

            border-radius: 50%;

            margin-right: 9px;
        }

        .threat-dot.red {
            background: #ef4444;
            box-shadow: 0 0 10px rgba(239, 68, 68, 0.5);
        }

        .threat-dot.orange {
            background: #f59e0b;
            box-shadow: 0 0 10px rgba(245, 158, 11, 0.4);
        }

        .threat-dot.green {
            background: #22c55e;
            box-shadow: 0 0 10px rgba(34, 197, 94, 0.4);
        }

        .threat-divider {
            height: 1px;

            background: #263449;

            margin: 9px 0;
        }

        .threat-total {
            display: flex;

            justify-content: space-between;

            padding-top: 11px;

            color: #8190a8;

            font-size: 12px;
        }

        .threat-total strong {
            color: #60a5fa;
        }


        /* =====================================================
           STREAMLIT CONTAINERS
        ===================================================== */

        div[data-testid="stVerticalBlockBorderWrapper"] {
            border-color: #263650 !important;
            border-radius: 15px !important;
            background: rgba(15, 23, 42, 0.45) !important;
        }


        /* =====================================================
           DATA TABLES
        ===================================================== */

        div[data-testid="stDataFrame"] {
            border: 1px solid #263650 !important;

            border-radius: 12px !important;

            overflow: hidden;

            box-shadow:
                0 8px 25px rgba(0, 0, 0, 0.14);
        }


        /* =====================================================
           SELECT BOXES / INPUTS
        ===================================================== */

        div[data-baseweb="select"] > div {
            min-height: 46px !important;

            background: #111827 !important;

            border-radius: 10px !important;

            border-color: #334155 !important;

            font-size: 14px !important;
        }

        div[data-baseweb="input"] > div {
            min-height: 46px !important;

            background: #111827 !important;

            border-radius: 10px !important;

            border-color: #334155 !important;
        }

        input {
            color: #f8fafc !important;
            font-size: 14px !important;
        }


        /* =====================================================
           BUTTONS
        ===================================================== */

        .stButton > button {
            min-height: 42px;

            padding: 0 18px;

            border-radius: 10px;

            font-size: 14px;
            font-weight: 700;

            border: 1px solid #334155;

            background: #111827;

            color: #e2e8f0;

            transition:
                all 0.15s ease;
        }

        .stButton > button:hover {
            border-color: #4b6b96;

            background: #172238;

            transform: translateY(-1px);
        }


        /* =====================================================
           METRICS
        ===================================================== */

        div[data-testid="stMetric"] {
            padding: 4px 0;
        }

        div[data-testid="stMetricLabel"] {
            font-size: 13px !important;
        }

        div[data-testid="stMetricValue"] {
            font-size: 30px !important;
            font-weight: 750 !important;
        }

        div[data-testid="stMetricDelta"] {
            font-size: 12px !important;
        }


        /* =====================================================
           DIVIDERS
        ===================================================== */

        hr {
            border-color: #1e2a42 !important;
        }


        /* =====================================================
           TABS
        ===================================================== */

        div[data-testid="stTabs"] button[data-baseweb="tab"] {
            height: 44px;

            padding: 0 18px;

            font-size: 14px;
            font-weight: 700;

            color: #8190a8;
        }

        div[data-testid="stTabs"] button[aria-selected="true"] {
            color: #60a5fa !important;
        }

        div[data-testid="stTabs"] div[data-baseweb="tab-highlight"] {
            background-color: #3b82f6 !important;
            height: 3px !important;
        }

        div[data-testid="stTabs"] div[data-baseweb="tab-border"] {
            background-color: #1e2a42 !important;
        }


        /* =====================================================
           CHECKBOX / RADIO
        ===================================================== */

        .stCheckbox label p,
        .stRadio label p {
            font-size: 14px !important;
        }


        /* =====================================================
           FOOTER
        ===================================================== */

        .app-footer {
            text-align: center;

            color: #526078;

            font-size: 11px;

            padding-top: 30px;
            padding-bottom: 10px;

            letter-spacing: 0.3px;
        }


        /* =====================================================
           RESPONSIVE
        ===================================================== */

        @media (max-width: 1100px) {

            .block-container {
                padding-left: 2rem !important;
                padding-right: 2rem !important;
            }

            .hero-title {
                font-size: 40px;
            }
        }


        @media (max-width: 900px) {

            section[data-testid="stSidebar"] {
                width: 260px !important;
                min-width: 260px !important;
            }

            section[data-testid="stSidebar"] > div {
                width: 260px !important;
            }

            .block-container {
                padding-left: 1.2rem !important;
                padding-right: 1.2rem !important;
            }

            .hero {
                flex-direction: column;
                align-items: flex-start;
                gap: 20px;
            }

            .hero-title {
                font-size: 36px;
            }

            .page-title {
                font-size: 30px;
            }
        }

        </style>
        """,
        unsafe_allow_html=True,
    )


# ============================================================
# PAGE HEADER
# ============================================================

def render_header(
    title,
    subtitle=None,
    kicker="RISK INTELLIGENCE",
):

    subtitle_html = ""

    if subtitle:
        subtitle_html = (
            f'<div class="page-subtitle">{subtitle}</div>'
        )

    # NOTE: this HTML is built as a single flush-left string
    # (no leading indentation, no blank lines). Streamlit's
    # markdown renderer follows CommonMark HTML-block rules,
    # which only treat a <div> as real HTML if it starts with
    # 3 or fewer leading spaces and isn't interrupted by a
    # blank line — otherwise it renders as literal text.
    html = (
        '<div class="page-header">'
        f'<div class="page-kicker">{kicker}</div>'
        f'<div class="page-title">🛡️ {title}</div>'
        f'{subtitle_html}'
        '</div>'
    )

    # Use markdown here instead of st.html.
    # This prevents raw HTML from appearing as page text
    # on Streamlit versions/configurations where st.html
    # behaves unexpectedly.
    st.markdown(
        html,
        unsafe_allow_html=True,
    )


# ============================================================
# SIDEBAR
# ============================================================

def render_sidebar():

    with st.sidebar:

        # Flush-left, single-line HTML — see note in render_header
        # about why indentation/blank lines break rendering.
        st.markdown(
            '<div class="sidebar-brand-box">'
            '<div class="sidebar-brand">'
            '<div class="sidebar-brand-icon">🛡️</div>'
            '<div>RiskGraph AI</div>'
            '</div>'
            '<div class="sidebar-subtitle">Fraud Risk Intelligence</div>'
            '<div class="sidebar-description">'
            'Graph analytics, machine learning, '
            'and transaction intelligence.'
            '</div>'
            '</div>',
            unsafe_allow_html=True,
        )

        st.markdown(
            '<div class="sidebar-status">'
            '<span class="sidebar-status-dot"></span>'
            'System Active'
            '</div>',
            unsafe_allow_html=True,
        )

        st.divider()


# ============================================================
# PANEL / SECTION HEADER
# ============================================================

def render_panel_header(title, subtitle=None, icon=None):
    """
    Consistent section heading used above charts, tables and
    panels throughout the app — replaces bare st.markdown("### ...").
    """

    icon_html = f"{icon} " if icon else ""

    subtitle_html = ""

    if subtitle:
        subtitle_html = f'<div class="section-subtitle">{subtitle}</div>'

    html = (
        f'<div class="panel-title">{icon_html}{title}</div>'
        f'{subtitle_html}'
    )

    st.markdown(html, unsafe_allow_html=True)


# ============================================================
# KPI CARD
# ============================================================

def render_kpi_card(label, value, icon="●", caption=None, variant=""):
    """
    Renders a single styled KPI card matching the app's
    design system (see .kpi-card CSS in setup_page).

    variant: "" | "danger" | "warning" | "blue" | "success"
    """

    caption_html = ""

    if caption:
        caption_html = f'<div class="kpi-caption">{caption}</div>'

    # Flush-left, single-line HTML — see note in render_header.
    html = (
        f'<div class="kpi-card {variant}">'
        f'<div class="kpi-icon">{icon}</div>'
        f'<div class="kpi-label">{label.upper()}</div>'
        f'<div class="kpi-value">{value}</div>'
        f'{caption_html}'
        '</div>'
    )

    st.markdown(html, unsafe_allow_html=True)


def render_kpi_row(cards):
    """
    Renders a row of KPI cards evenly split across columns.

    cards: list of dicts with keys:
        label, value, icon (optional), caption (optional),
        variant (optional)
    """

    columns = st.columns(len(cards))

    for column, card in zip(columns, cards):
        with column:
            render_kpi_card(
                label=card.get("label", ""),
                value=card.get("value", ""),
                icon=card.get("icon", "●"),
                caption=card.get("caption"),
                variant=card.get("variant", ""),
            )


# ============================================================
# RISK HELPERS
# ============================================================

def risk_badge(level):

    level = str(level).upper()

    if level == "HIGH":
        return "🔴 HIGH"

    if level == "MEDIUM":
        return "🟠 MEDIUM"

    return "🟢 LOW"


def risk_badge_html(level):
    """
    Returns a styled HTML pill for a risk level
    (HIGH / MEDIUM / LOW).
    """

    level = str(level).upper()

    if level == "HIGH":
        return '<span class="badge badge-high">🔴 HIGH</span>'

    if level == "MEDIUM":
        return '<span class="badge badge-medium">🟠 MEDIUM</span>'

    if level == "LOW":
        return '<span class="badge badge-low">🟢 LOW</span>'

    return f'<span class="badge badge-neutral">{level}</span>'


def status_badge_html(is_suspicious):
    """
    Returns a styled HTML pill for a transaction status,
    accepting 1/0, True/False, or "Suspicious"/"Normal".
    """

    value = str(is_suspicious).strip().upper()

    is_flagged = value in ("1", "TRUE", "SUSPICIOUS")

    if is_flagged:
        return '<span class="badge badge-high">⚠ Suspicious</span>'

    return '<span class="badge badge-low">✓ Normal</span>'


def render_badge_stat(label, level_or_status, kind="risk"):
    """
    Renders a label + colored badge in place of a plain
    st.metric — used for risk levels / statuses so they
    show as pills instead of bare text.

    kind: "risk" uses risk_badge_html, "status" uses
    status_badge_html.
    """

    if kind == "status":
        badge_html = status_badge_html(level_or_status)
    else:
        badge_html = risk_badge_html(level_or_status)

    html = (
        f'<div class="stat-label">{label.upper()}</div>'
        f'{badge_html}'
    )

    st.markdown(html, unsafe_allow_html=True)


def render_progress(value, max_value=100, variant="blue", caption=None):
    """
    Renders a horizontal progress bar for a 0..max_value score.
    variant: "blue" | "danger" | "warning" | "success"
    """

    try:
        pct = max(0.0, min(100.0, (float(value) / max_value) * 100))
    except (TypeError, ZeroDivisionError):
        pct = 0.0

    caption_html = ""

    if caption:
        caption_html = f'<div class="progress-caption">{caption}</div>'

    html = (
        '<div class="progress-track">'
        f'<div class="progress-fill {variant}" '
        f'style="width:{pct:.1f}%"></div>'
        '</div>'
        f'{caption_html}'
    )

    st.markdown(html, unsafe_allow_html=True)


def variant_for_level(level):
    """
    Maps a risk level string to a progress-bar / kpi-card
    color variant.
    """

    level = str(level).upper()

    if level == "HIGH":
        return "danger"

    if level == "MEDIUM":
        return "warning"

    return "success"


# ============================================================
# STYLED TABLES
# ============================================================

_LEVEL_STYLE_MAP = {
    "HIGH": "background-color: rgba(239, 68, 68, 0.14); "
            "color: #fca5a5; font-weight: 700;",
    "SUSPICIOUS": "background-color: rgba(239, 68, 68, 0.14); "
                  "color: #fca5a5; font-weight: 700;",
    "MEDIUM": "background-color: rgba(245, 158, 11, 0.14); "
              "color: #fcd34d; font-weight: 700;",
    "LOW": "background-color: rgba(34, 197, 94, 0.14); "
           "color: #86efac; font-weight: 700;",
    "NORMAL": "background-color: rgba(34, 197, 94, 0.14); "
              "color: #86efac; font-weight: 700;",
}


def _level_cell_style(value):
    return _LEVEL_STYLE_MAP.get(str(value).upper(), "")


def style_levels(df, columns):
    """
    Returns a pandas Styler that color-codes the given
    columns (risk levels or Suspicious/Normal status)
    for use directly in st.dataframe(). Falls back to the
    plain DataFrame if none of the given columns exist.
    """

    existing = [c for c in columns if c in df.columns]

    if not existing:
        return df

    styler = df.style

    try:
        return styler.map(_level_cell_style, subset=existing)
    except AttributeError:
        # Older pandas versions use applymap instead of map.
        return styler.applymap(_level_cell_style, subset=existing)


# ============================================================
# STEP TIMELINE / INFO CARDS
# ============================================================

def render_step_timeline(steps):
    """
    Renders a vertical numbered timeline.
    steps: list of (title, description) tuples.
    """

    rows = ""

    for index, (title, description) in enumerate(steps, start=1):
        rows += (
            '<div class="step-row">'
            f'<div class="step-index">{index}</div>'
            '<div>'
            f'<div class="step-body-title">{title}</div>'
            f'<div class="step-body-text">{description}</div>'
            '</div>'
            '</div>'
        )

    html = f'<div class="step-timeline">{rows}</div>'

    st.markdown(html, unsafe_allow_html=True)


def render_info_card(icon, title, text):
    """
    Renders a single info/feature card (icon + title + text).
    Meant to be placed inside an st.columns() cell.
    """

    html = (
        '<div class="info-card">'
        f'<div class="info-card-icon">{icon}</div>'
        f'<div class="info-card-title">{title}</div>'
        f'<div class="info-card-text">{text}</div>'
        '</div>'
    )

    st.markdown(html, unsafe_allow_html=True)


def risk_counts(df):

    return {
        "HIGH": int(
            (df["final_risk_level"] == "HIGH").sum()
        ),

        "MEDIUM": int(
            (df["final_risk_level"] == "MEDIUM").sum()
        ),

        "LOW": int(
            (df["final_risk_level"] == "LOW").sum()
        ),
    }


# ============================================================
# FORMATTING
# ============================================================

def format_number(value):
    return f"{value:,.0f}"


def format_score(value):
    return f"{value:.2f}"


# ============================================================
# FOOTER
# ============================================================

def render_footer():

    st.divider()

    # Flush-left, single-line HTML — see note in render_header.
    st.markdown(
        '<div class="app-footer">'
        'RiskGraph AI · Graph-based fraud detection '
        'powered by machine learning'
        '</div>',
        unsafe_allow_html=True,
    )