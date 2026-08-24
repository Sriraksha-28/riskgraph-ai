import pandas as pd
import streamlit as st


RESULT_FILE = "data/final_risk_results.csv"


# --------------------------------------------------
# Page configuration
# --------------------------------------------------

st.set_page_config(
    page_title="RiskGraph AI",
    page_icon="🛡️",
    layout="wide"
)


# --------------------------------------------------
# Load results
# --------------------------------------------------

@st.cache_data
def load_results():
   return pd.read_csv(
    RESULT_FILE,
    keep_default_na=False
)

df = load_results()


# --------------------------------------------------
# Header
# --------------------------------------------------

st.title("🛡️ RiskGraph AI")
st.subheader("Fraud Risk Detection Dashboard")

st.write(
    "End-to-end user risk analysis using graph-based "
    "risk features and machine learning."
)


# --------------------------------------------------
# Summary metrics
# --------------------------------------------------

total_users = len(df)

high_risk = (
    df["final_risk_level"] == "HIGH"
).sum()

medium_risk = (
    df["final_risk_level"] == "MEDIUM"
).sum()

low_risk = (
    df["final_risk_level"] == "LOW"
).sum()


col1, col2, col3, col4 = st.columns(4)

with col1:
    st.metric(
        "Total Users",
        total_users
    )

with col2:
    st.metric(
        "High Risk",
        high_risk
    )

with col3:
    st.metric(
        "Medium Risk",
        medium_risk
    )

with col4:
    st.metric(
        "Low Risk",
        low_risk
    )


st.divider()


# --------------------------------------------------
# Risk distribution
# --------------------------------------------------

st.subheader("Risk Distribution")

risk_counts = (
    df["final_risk_level"]
    .value_counts()
    .rename_axis("Risk Level")
    .reset_index(name="Users")
)

st.bar_chart(
    risk_counts.set_index("Risk Level")
)


# --------------------------------------------------
# Highest-risk users
# --------------------------------------------------

st.subheader("Highest-Risk Users")

top_users = df[
    [
        "user_id",
        "final_risk_score",
        "final_risk_level",
        "ml_suspicious_probability",
        "risk_score"
    ]
].head(20)

st.dataframe(
    top_users,
    use_container_width=True
)


# --------------------------------------------------
# User investigation
# --------------------------------------------------

st.divider()

st.subheader("Investigate a User")

user_ids = sorted(
    df["user_id"]
    .dropna()
    .unique()
    .tolist()
)

selected_user = st.selectbox(
    "Select User",
    user_ids
)


user = df[
    df["user_id"] == selected_user
].iloc[0]


# --------------------------------------------------
# User risk summary
# --------------------------------------------------

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
    st.metric(
        "Risk Level",
        user["final_risk_level"]
    )


# --------------------------------------------------
# Risk details
# --------------------------------------------------

st.write(
    f"**Rule-Based Risk Score:** "
    f"{user['risk_score']:.2f}"
)

st.write(
    f"**Rule-Based Risk Level:** "
    f"{user['risk_level']}"
)

st.write(
    f"**ML Risk Level:** "
    f"{user['ml_risk_level']}"
)


# --------------------------------------------------
# Risk reasons
# --------------------------------------------------

st.subheader("Risk Reasons")

reasons = str(
    user["risk_reasons"]
).split(";")

for reason in reasons:
    st.write(f"• {reason.strip()}")


# --------------------------------------------------
# Graph connections
# --------------------------------------------------

st.subheader("Graph Connections")

st.write(
    f"**Connected Devices:** "
    f"{user['connected_devices'] or 'None'}"
)

st.write(
    f"**Connected Merchants:** "
    f"{user['connected_merchants'] or 'None'}"
)

st.write(
    f"**Other Users Sharing Devices:** "
    f"{user['shared_device_users'] or 'None'}"
)

# --------------------------------------------------
# Transaction details
# --------------------------------------------------

st.subheader("Transaction Details")

transactions_df = pd.read_csv(
    "data/transactions.csv"
)

user_transactions = transactions_df[
    transactions_df["user_id"] == selected_user
].copy()

if user_transactions.empty:

    st.info("No transactions found for this user.")

else:

    show_all = st.checkbox(
        "Show all transactions",
        value=False
    )

    if not show_all:

        display_transactions = user_transactions[
            user_transactions["is_suspicious"] == 1
        ].copy()

        st.write(
            f"Showing suspicious transactions: "
            f"{len(display_transactions)}"
        )

    else:

        display_transactions = user_transactions.copy()

        st.write(
            f"Showing all transactions: "
            f"{len(display_transactions)}"
        )

    transaction_columns = [
        "transaction_id",
        "device_id",
        "merchant_id",
        "timestamp",
        "amount",
        "location",
        "is_suspicious"
    ]

    display_transactions = display_transactions[
        transaction_columns
    ].copy()

    display_transactions["status"] = (
        display_transactions["is_suspicious"]
        .map({
            1: "Suspicious",
            0: "Normal"
        })
    )

    display_transactions = display_transactions.drop(
        columns=["is_suspicious"]
    )

    st.dataframe(
        display_transactions,
        use_container_width=True
    )

# --------------------------------------------------
# Footer
# --------------------------------------------------

st.divider()

st.caption(
    "RiskGraph AI — Graph-based fraud detection "
    "with machine learning"
)