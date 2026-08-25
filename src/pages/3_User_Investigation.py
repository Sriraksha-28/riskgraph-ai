import pandas as pd
import streamlit as st

from ui_utils import (
    setup_page,
    render_sidebar,
    render_header,
    render_footer,
    render_panel_header,
    render_badge_stat,
    style_levels,
    load_final_results,
    load_transactions,
)


setup_page("User Investigation", "👤")
render_sidebar()

df = load_final_results()
transactions = load_transactions()

render_header(
    "User Investigation",
    "Detailed investigation of an individual user"
)

user_ids = sorted(df["user_id"].tolist())


selected_user = st.selectbox(
    "Select User",
    user_ids
)

user = df[
    df["user_id"] == selected_user
].iloc[0]

user_transactions = transactions[
    transactions["user_id"] == selected_user
].copy()

suspicious = user_transactions[
    user_transactions["is_suspicious"] == 1
]

render_panel_header(f"Investigation — {selected_user}", icon="🕵️")

with st.container(border=True):

    col1, col2, col3 = st.columns(3)

    with col1:
        st.metric(
            "Final Risk Score",
            f"{user['final_risk_score']:.2f}"
        )

    with col2:
        st.metric(
            "ML Probability",
            f"{user['ml_suspicious_probability']:.2f}%"
        )

    with col3:
        render_badge_stat("Risk Level", user["final_risk_level"])

st.divider()

render_panel_header("Risk Reasons", icon="📝")

for reason in str(user["risk_reasons"]).split(";"):
    st.write(f"• {reason.strip()}")

st.divider()

render_panel_header("Graph Connections", icon="🕸️")

col1, col2, col3 = st.columns(3)

with col1:
    with st.container(border=True):
        st.write("**Devices**")
        st.write(user["connected_devices"] or "None")

with col2:
    with st.container(border=True):
        st.write("**Merchants**")
        st.write(user["connected_merchants"] or "None")

with col3:
    with st.container(border=True):
        st.write("**Shared Users**")
        st.write(user["shared_device_users"] or "None")

st.divider()

render_panel_header("Transaction Summary", icon="📊")

col1, col2, col3 = st.columns(3)

with col1:
    st.metric(
        "Total Transactions",
        len(user_transactions)
    )

with col2:
    st.metric(
        "Suspicious Transactions",
        len(suspicious)
    )

with col3:
    suspicious_rate = (
        len(suspicious)
        / len(user_transactions)
        * 100
        if len(user_transactions)
        else 0
    )

    st.metric(
        "Suspicious Rate",
        f"{suspicious_rate:.2f}%"
    )

st.divider()

render_panel_header("Transactions", icon="💳")

if user_transactions.empty:

    st.info("No transactions found.")

else:

    show_all = st.checkbox(
        "Show all transactions",
        value=False
    )

    if show_all:
        display = user_transactions.copy()
    else:
        display = suspicious.copy()

    display["status"] = display[
        "is_suspicious"
    ].map({
        1: "Suspicious",
        0: "Normal"
    })

    display = display.drop(
        columns=["is_suspicious"]
    )

    st.dataframe(
        style_levels(display, ["status"]),
        hide_index=True,
        width="stretch"
    )

render_footer()