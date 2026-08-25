import streamlit as st

from ui_utils import (
    setup_page,
    render_sidebar,
    render_header,
    render_footer,
    render_panel_header,
    render_info_card
)


setup_page("About", "📋")
render_sidebar()

render_header(
    "About RiskGraph AI",
    "Intelligent fraud detection, built for clarity and trust"
)


# ============================================================
# WHAT IS RISKGRAPH AI
# ============================================================

render_panel_header("What is RiskGraph AI?", icon="🛡️")

st.write(
    "RiskGraph AI is a fraud-risk intelligence platform that helps "
    "teams spot suspicious users before they cause damage. It looks "
    "beyond individual transactions to understand how users, devices "
    "and merchants are connected — surfacing the kind of coordinated, "
    "hard-to-catch fraud that simple rule checks miss."
)

st.write(
    "Every user gets a clear, explainable risk score, so analysts "
    "always know not just *who* is risky, but *why*."
)

st.divider()


# ============================================================
# WHY RISKGRAPH AI
# ============================================================

render_panel_header(
    "Why RiskGraph AI",
    "What makes the platform effective",
    icon="✨",
)

col1, col2, col3 = st.columns(3)

with col1:
    render_info_card(
        "🕸️",
        "Network-Aware Detection",
        "Uncovers shared devices, merchant clusters and hidden "
        "connections that isolated transaction checks can't see.",
    )

with col2:
    render_info_card(
        "🤖",
        "Hybrid Intelligence",
        "Combines transparent rule-based scoring with a trained "
        "machine learning model for both accuracy and explainability.",
    )

with col3:
    render_info_card(
        "🔎",
        "Built for Investigation",
        "Every flagged user comes with the evidence behind the "
        "score — reasons, connections and transaction history.",
    )

st.divider()


# ============================================================
# WHAT YOU CAN DO
# ============================================================

render_panel_header(
    "What You Can Do",
    "Everything available across the platform",
    icon="🧭",
)

col1, col2 = st.columns(2)

with col1:
    st.markdown("**📊 Monitor risk at a glance**")
    st.write(
        "Track total users, risk distribution and the highest-priority "
        "accounts from a single dashboard."
    )

    st.write("")

    st.markdown("**🪪 Explore individual risk profiles**")
    st.write(
        "Compare rule-based scores against ML predictions for any "
        "user, side by side."
    )

with col2:
    st.markdown("**💳 Search and filter transactions**")
    st.write(
        "Drill into transaction activity by status, location or "
        "user to investigate specific behaviour."
    )

    st.write("")

    st.markdown("**🕵️ Investigate connections**")
    st.write(
        "See a user's shared devices, connected merchants and "
        "other accounts linked through the same device."
    )

st.divider()


# ============================================================
# PROJECT STATUS
# ============================================================

render_panel_header("Project Status", icon="📌")

st.success(
    "Milestones 1–4 completed. "
    "Milestone 5 focuses on UI/UX and product polish."
)

render_footer()