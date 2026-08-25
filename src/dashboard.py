import pandas as pd
import streamlit as st

from ui_utils import (
    setup_page,
    render_sidebar,
    render_header,
    render_footer,
    render_kpi_row,
    render_panel_header,
    render_badge_stat,
    render_progress,
    style_levels,
    load_final_results,
    load_transactions,
)


# ============================================================
# PAGE SETUP
# ============================================================

setup_page("Dashboard", "🛡️")
render_sidebar()


# ============================================================
# LOAD DATA
# ============================================================

df = load_final_results()
transactions_df = load_transactions()


# ============================================================
# HEADER
# ============================================================

render_header(
    "RiskGraph AI Dashboard",
    "End-to-end user risk analysis using graph-based "
    "risk features and machine learning.",
)


# ============================================================
# SUMMARY METRICS
# ============================================================

total_users = len(df)

high_risk = int((df["final_risk_level"] == "HIGH").sum())
medium_risk = int((df["final_risk_level"] == "MEDIUM").sum())
low_risk = int((df["final_risk_level"] == "LOW").sum())

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
            "label": "High Risk",
            "value": f"{high_risk:,}",
            "icon": "🔴",
            "caption": "Requires attention",
            "variant": "danger",
        },
        {
            "label": "Medium Risk",
            "value": f"{medium_risk:,}",
            "icon": "🟠",
            "caption": "Worth monitoring",
            "variant": "warning",
        },
        {
            "label": "Low Risk",
            "value": f"{low_risk:,}",
            "icon": "🟢",
            "caption": "No action needed",
            "variant": "success",
        },
    ]
)

st.write("")


# ============================================================
# RISK DISTRIBUTION
# ============================================================

render_panel_header(
    "Risk Distribution",
    "Breakdown of all analyzed users by final risk level",
    icon="📊",
)

risk_counts_series = (
    df["final_risk_level"]
    .value_counts()
    .reindex(["HIGH", "MEDIUM", "LOW"], fill_value=0)
)

st.bar_chart(risk_counts_series, height=320)

st.divider()


# ============================================================
# HIGHEST-RISK USERS
# ============================================================

render_panel_header(
    "Highest-Risk Users",
    "Top 20 users ranked by final risk score",
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
    .sort_values("final_risk_score", ascending=False)
    .head(20)
    .copy()
)

st.dataframe(
    style_levels(top_users, ["final_risk_level"]),
    hide_index=True,
    width="stretch",
    column_config={
        "user_id": st.column_config.TextColumn("User ID"),
        "final_risk_score": st.column_config.NumberColumn(
            "Final Risk Score", format="%.2f"
        ),
        "final_risk_level": st.column_config.TextColumn("Risk Level"),
        "ml_suspicious_probability": st.column_config.NumberColumn(
            "ML Probability", format="%.2f%%"
        ),
        "risk_score": st.column_config.NumberColumn(
            "Rule-Based Score", format="%.2f"
        ),
    },
)

st.divider()


# ============================================================
# INVESTIGATE A USER
# ============================================================

render_panel_header(
    "Investigate a User",
    "Full risk profile, graph connections and transaction history",
    icon="🔎",
)

with st.container(border=True):

    user_ids = sorted(df["user_id"].dropna().unique().tolist())

    selected_user = st.selectbox("Select User", user_ids)

    user = df[df["user_id"] == selected_user].iloc[0]

    st.write("")

    col1, col2, col3 = st.columns(3)

    with col1:
        st.metric("Final Risk Score", f"{user['final_risk_score']:.2f}")

    with col2:
        st.metric(
            "ML Probability", f"{user['ml_suspicious_probability']:.2f}%"
        )
        render_progress(
            user["ml_suspicious_probability"],
            variant="danger" if user["ml_suspicious_probability"] >= 70
            else "warning" if user["ml_suspicious_probability"] >= 30
            else "success",
        )

    with col3:
        render_badge_stat("Risk Level", user["final_risk_level"])

    st.write("")

    left, right = st.columns(2)

    with left:
        with st.container(border=True):
            st.markdown("**Rule-Based Assessment**")
            st.write(f"Risk Score: **{user['risk_score']:.2f}**")
            st.write(f"Risk Level: **{user['risk_level']}**")

    with right:
        with st.container(border=True):
            st.markdown("**Machine Learning Assessment**")
            st.write(
                f"Suspicious Probability: "
                f"**{user['ml_suspicious_probability']:.2f}%**"
            )
            st.write(f"ML Risk Level: **{user['ml_risk_level']}**")

    st.write("")

    st.markdown("**Risk Reasons**")

    reasons = str(user["risk_reasons"]).split(";")

    for reason in reasons:
        st.write(f"• {reason.strip()}")

    st.write("")

    st.markdown("**Graph Connections**")

    gc1, gc2, gc3 = st.columns(3)

    with gc1:
        st.caption("Connected Devices")
        st.write(user["connected_devices"] or "None")

    with gc2:
        st.caption("Connected Merchants")
        st.write(user["connected_merchants"] or "None")

    with gc3:
        st.caption("Other Users Sharing Devices")
        st.write(user["shared_device_users"] or "None")

st.divider()


# ============================================================
# TRANSACTION DETAILS
# ============================================================

render_panel_header(
    "Transaction Details",
    f"Transaction activity for {selected_user}",
    icon="💳",
)

user_transactions = transactions_df[
    transactions_df["user_id"] == selected_user
].copy()

if user_transactions.empty:

    st.info("No transactions found for this user.")

else:

    show_all = st.checkbox("Show all transactions", value=False)

    if not show_all:
        display_transactions = user_transactions[
            user_transactions["is_suspicious"] == 1
        ].copy()

        st.caption(
            f"Showing suspicious transactions: "
            f"{len(display_transactions)}"
        )

    else:
        display_transactions = user_transactions.copy()

        st.caption(
            f"Showing all transactions: {len(display_transactions)}"
        )

    transaction_columns = [
        "transaction_id",
        "device_id",
        "merchant_id",
        "timestamp",
        "amount",
        "location",
        "is_suspicious",
    ]

    display_transactions = display_transactions[transaction_columns].copy()

    display_transactions["status"] = display_transactions[
        "is_suspicious"
    ].map({1: "Suspicious", 0: "Normal"})

    display_transactions = display_transactions.drop(
        columns=["is_suspicious"]
    )

    st.dataframe(
        style_levels(display_transactions, ["status"]),
        hide_index=True,
        width="stretch",
    )


# ============================================================
# FOOTER
# ============================================================

render_footer()