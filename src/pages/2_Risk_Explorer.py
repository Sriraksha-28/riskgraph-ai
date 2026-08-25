import streamlit as st

from ui_utils import (
    setup_page,
    render_sidebar,
    render_header,
    render_footer,
    render_panel_header,
    render_badge_stat,
    render_progress,
    load_final_results,
)


setup_page("Risk Explorer", "🔎")
render_sidebar()

df = load_final_results()

render_header(
    "Risk Explorer",
    "Explore and compare user risk assessments"
)

user_ids = sorted(df["user_id"].tolist())

selected_user = st.selectbox(
    "Select User",
    user_ids
)

user = df[df["user_id"] == selected_user].iloc[0]

render_panel_header(f"Risk Profile — {selected_user}", icon="🪪")

with st.container(border=True):

    col1, col2, col3, col4 = st.columns(4)

    with col1:
        st.metric(
            "Final Risk Score",
            f"{user['final_risk_score']:.2f}"
        )

    with col2:
        st.metric(
            "Rule-Based Score",
            f"{user['risk_score']:.2f}"
        )

    with col3:
        st.metric(
            "ML Probability",
            f"{user['ml_suspicious_probability']:.2f}%"
        )
        render_progress(
            user["ml_suspicious_probability"],
            variant="danger" if user["ml_suspicious_probability"] >= 70
            else "warning" if user["ml_suspicious_probability"] >= 30
            else "success",
        )

    with col4:
        render_badge_stat("Final Level", user["final_risk_level"])

st.write("")

left, right = st.columns(2)

with left:
    with st.container(border=True):
        st.subheader("Rule-Based Assessment")

        st.write(
            f"Risk Score: **{user['risk_score']:.2f}**"
        )

        st.write(
            f"Risk Level: **{user['risk_level']}**"
        )

with right:
    with st.container(border=True):
        st.subheader("Machine Learning Assessment")

        st.write(
            f"Suspicious Probability: "
            f"**{user['ml_suspicious_probability']:.2f}%**"
        )

        st.write(
            f"ML Risk Level: **{user['ml_risk_level']}**"
        )

st.divider()

render_panel_header("Risk Reasons", icon="📝")

for reason in str(user["risk_reasons"]).split(";"):
    st.write(f"• {reason.strip()}")

st.divider()

render_panel_header("Risk Comparison", icon="⚖️")

comparison = {
    "Assessment": [
        "Rule-Based",
        "ML",
        "Final"
    ],
    "Score / Probability": [
        float(user["risk_score"]),
        float(user["ml_suspicious_probability"]),
        float(user["final_risk_score"])
    ]
}

st.dataframe(
    comparison,
    hide_index=True,
    width="stretch"
)

render_footer()