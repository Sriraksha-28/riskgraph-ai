import pandas as pd
import streamlit as st

from ui_utils import (
    setup_page,
    render_sidebar,
    render_header,
    render_footer,
    render_kpi_row,
    render_panel_header,
    load_final_results,
    load_transactions,
    risk_counts,
)


# ============================================================
# PAGE SETUP
# ============================================================

setup_page("Overview", "🏠")
render_sidebar()


# ============================================================
# LOAD DATA
# ============================================================

df = load_final_results()
transactions = load_transactions()

counts = risk_counts(df)

total_users = len(df)
total_transactions = len(transactions)

suspicious_transactions = int(
    (transactions["is_suspicious"] == 1).sum()
)

suspicious_rate = (
    suspicious_transactions / total_transactions * 100
    if total_transactions > 0
    else 0
)


# ============================================================
# PAGE HEADER
# ============================================================

render_header(
    "Risk Intelligence Overview",
    "Graph-powered fraud detection and machine learning "
    "risk intelligence.",
)

st.success(
    "● System Active — Risk monitoring and analysis are operational."
)

st.write("")


# ============================================================
# KEY METRICS
# ============================================================

render_kpi_row(
    [
        {
            "label": "Total Users",
            "value": f"{total_users:,}",
            "icon": "👥",
            "caption": "Users analyzed",
            "variant": "blue",
        },
        {
            "label": "High Risk Users",
            "value": f"{counts['HIGH']:,}",
            "icon": "🔴",
            "caption": "Users requiring attention",
            "variant": "danger",
        },
        {
            "label": "Suspicious Activity",
            "value": f"{suspicious_transactions:,}",
            "icon": "⚠️",
            "caption": "Suspicious transactions detected",
            "variant": "warning",
        },
        {
            "label": "Suspicious Rate",
            "value": f"{suspicious_rate:.2f}%",
            "icon": "📈",
            "caption": "Percentage of all transactions",
            "variant": "blue",
        },
    ]
)

st.write("")


# ============================================================
# RISK DISTRIBUTION
# ============================================================

left, right = st.columns([1.5, 1])


# ------------------------------------------------------------
# LEFT — CHART
# ------------------------------------------------------------

with left:

    render_panel_header("Risk Distribution", icon="📊")

    chart_data = (
        df["final_risk_level"]
        .value_counts()
        .reindex(
            ["HIGH", "MEDIUM", "LOW"],
            fill_value=0,
        )
    )

    st.bar_chart(
        chart_data,
        height=320,
    )


# ------------------------------------------------------------
# RIGHT — RISK SUMMARY
# ------------------------------------------------------------

with right:

    render_panel_header("Threat Summary", icon="🛡️")

    with st.container(border=True):

        st.markdown("🔴 **High Risk**")

        st.metric(
            label="",
            value=f"{counts['HIGH']:,}",
        )

        st.divider()

        st.markdown("🟠 **Medium Risk**")

        st.metric(
            label="",
            value=f"{counts['MEDIUM']:,}",
        )

        st.divider()

        st.markdown("🟢 **Low Risk**")

        st.metric(
            label="",
            value=f"{counts['LOW']:,}",
        )


st.divider()


# ============================================================
# PRIORITY USERS
# ============================================================

render_panel_header(
    "Priority Users",
    "Users ranked by final risk score",
    icon="🚨",
)


top_users = (
    df[
        [
            "user_id",
            "final_risk_score",
            "final_risk_level",
            "ml_suspicious_probability",
            "risk_score",
        ]
    ]
    .sort_values(
        "final_risk_score",
        ascending=False,
    )
    .head(10)
    .copy()
)


# Format values for display

top_users["final_risk_score"] = (
    top_users["final_risk_score"]
    .round(2)
)

top_users["ml_suspicious_probability"] = (
    top_users["ml_suspicious_probability"]
    .round(2)
)

top_users["risk_score"] = (
    top_users["risk_score"]
    .round(2)
)


st.dataframe(
    top_users,
    hide_index=True,
    width="stretch",
    column_config={
        "user_id": st.column_config.TextColumn(
            "User ID",
        ),
        "final_risk_score": st.column_config.NumberColumn(
            "Final Risk Score",
            format="%.2f",
        ),
        "final_risk_level": st.column_config.TextColumn(
            "Risk Level",
        ),
        "ml_suspicious_probability": st.column_config.NumberColumn(
            "ML Probability",
            format="%.2f%%",
        ),
        "risk_score": st.column_config.NumberColumn(
            "Rule-Based Score",
            format="%.2f",
        ),
    },
)


st.divider()


# ============================================================
# RECENT SUSPICIOUS ACTIVITY
# ============================================================

render_panel_header(
    "Recent Suspicious Activity",
    "Latest transactions flagged by the fraud detection system",
    icon="⚠️",
)


suspicious = transactions[
    transactions["is_suspicious"] == 1
].copy()


# ------------------------------------------------------------
# Sort newest transactions first
# ------------------------------------------------------------

if "timestamp" in suspicious.columns:

    suspicious["timestamp"] = pd.to_datetime(
        suspicious["timestamp"],
        errors="coerce",
    )

    suspicious = suspicious.sort_values(
        "timestamp",
        ascending=False,
    )


# ------------------------------------------------------------
# Display latest suspicious transactions
# ------------------------------------------------------------

display_columns = [
    "transaction_id",
    "user_id",
    "device_id",
    "merchant_id",
    "timestamp",
    "amount",
    "location",
]


available_columns = [
    column
    for column in display_columns
    if column in suspicious.columns
]


recent_suspicious = suspicious[
    available_columns
].head(8)


st.dataframe(
    recent_suspicious,
    hide_index=True,
    width="stretch",
    column_config={
        "transaction_id": st.column_config.TextColumn(
            "Transaction ID",
        ),
        "user_id": st.column_config.TextColumn(
            "User ID",
        ),
        "device_id": st.column_config.TextColumn(
            "Device",
        ),
        "merchant_id": st.column_config.TextColumn(
            "Merchant",
        ),
        "timestamp": st.column_config.DatetimeColumn(
            "Timestamp",
            format="YYYY-MM-DD HH:mm",
        ),
        "amount": st.column_config.NumberColumn(
            "Amount",
            format="₹%.2f",
        ),
        "location": st.column_config.TextColumn(
            "Location",
        ),
    },
)


st.divider()


# ============================================================
# SYSTEM SNAPSHOT
# ============================================================

render_panel_header("System Snapshot", icon="🧭")

s1, s2, s3 = st.columns(3)


with s1:
    with st.container(border=True):
        st.markdown("#### 👥 User Coverage")
        st.metric(
            "Users Analyzed",
            f"{total_users:,}",
        )
        st.caption(
            "All users currently present in the risk dataset."
        )


with s2:
    with st.container(border=True):
        st.markdown("#### 💳 Transaction Coverage")
        st.metric(
            "Transactions Analyzed",
            f"{total_transactions:,}",
        )
        st.caption(
            "Transactions evaluated by the monitoring pipeline."
        )


with s3:
    with st.container(border=True):
        st.markdown("#### 🧠 Detection Engine")
        st.metric(
            "Detection Layers",
            "2",
        )
        st.caption(
            "Rule-based scoring + machine learning."
        )


# ============================================================
# FOOTER
# ============================================================

render_footer()