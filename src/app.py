import pandas as pd
import joblib


# --------------------------------------------------
# Configuration
# --------------------------------------------------

MODEL_FILE = "models/risk_model.pkl"
RISK_FILE = "data/user_risk_scores.csv"
EXPLANATION_FILE = "data/user_risk_explanations.csv"
TRANSACTION_FILE = "data/transactions.csv"
OUTPUT_FILE = "data/final_risk_results.csv"


print("RiskGraph AI - End-to-End Risk Application")
print("=" * 55)


# --------------------------------------------------
# Load model and data
# --------------------------------------------------

print("\nLoading model...")
model = joblib.load(MODEL_FILE)

print("Loading risk features...")
risk_df = pd.read_csv(RISK_FILE)

print("Loading risk explanations...")
explanation_df = pd.read_csv(EXPLANATION_FILE)

print("Loading transactions...")
transactions_df = pd.read_csv(TRANSACTION_FILE)

print(f"\nUsers loaded: {len(risk_df)}")
print(f"Transactions loaded: {len(transactions_df)}")


# --------------------------------------------------
# Add risk explanations
# --------------------------------------------------

if "risk_reasons" in explanation_df.columns:
    risk_df = risk_df.merge(
        explanation_df[["user_id", "risk_reasons"]],
        on="user_id",
        how="left"
    )
else:
    risk_df["risk_reasons"] = (
        "No major risk indicators detected"
    )


# --------------------------------------------------
# Build transaction features
# --------------------------------------------------

transaction_features = (
    transactions_df
    .groupby("user_id")
    .agg(
        total_transactions=("transaction_id", "count"),
        average_amount=("amount", "mean"),
        maximum_amount=("amount", "max"),
        unique_transaction_devices=("device_id", "nunique"),
        unique_transaction_merchants=("merchant_id", "nunique"),
        unique_locations=("location", "nunique")
    )
    .reset_index()
)


# --------------------------------------------------
# Combine user and transaction features
# --------------------------------------------------

user_df = risk_df.merge(
    transaction_features,
    on="user_id",
    how="left"
)

user_df = user_df.fillna(0)


# --------------------------------------------------
# ML feature list
# --------------------------------------------------

feature_columns = [
    "account_age_days",
    "transaction_count",
    "transactions_per_hour",
    "unique_merchant_count",
    "merchant_concentration_ratio",
    "unique_device_count",
    "max_shared_device_users",
    "max_users_on_device_in_window",
    "total_transactions",
    "average_amount",
    "maximum_amount",
    "unique_transaction_devices",
    "unique_transaction_merchants",
    "unique_locations"
]


X = user_df[feature_columns]


# --------------------------------------------------
# ML predictions
# --------------------------------------------------

print("\nRunning ML predictions...")

user_df["ml_prediction"] = model.predict(X)

probabilities = model.predict_proba(X)

user_df["ml_suspicious_probability"] = (
    probabilities[:, 1] * 100
).round(2)


# --------------------------------------------------
# ML risk level
# --------------------------------------------------

def get_ml_risk_level(probability):

    if probability >= 70:
        return "HIGH"

    elif probability >= 30:
        return "MEDIUM"

    return "LOW"


user_df["ml_risk_level"] = (
    user_df["ml_suspicious_probability"]
    .apply(get_ml_risk_level)
)


# --------------------------------------------------
# Unified risk decision
# --------------------------------------------------

def get_final_risk_level(row):

    if (
        row["risk_level"] == "HIGH"
        or row["ml_risk_level"] == "HIGH"
    ):
        return "HIGH"

    if (
        row["risk_level"] == "MEDIUM"
        or row["ml_risk_level"] == "MEDIUM"
    ):
        return "MEDIUM"

    return "LOW"


user_df["final_risk_level"] = (
    user_df.apply(
        get_final_risk_level,
        axis=1
    )
)


# --------------------------------------------------
# Final risk score
# --------------------------------------------------

user_df["final_risk_score"] = (
    (
        user_df["risk_score"]
        + user_df["ml_suspicious_probability"]
    ) / 2
).round(2)


# --------------------------------------------------
# Investigation information
# --------------------------------------------------

def get_user_devices(user_id):

    devices = (
        transactions_df[
            transactions_df["user_id"] == user_id
        ]["device_id"]
        .dropna()
        .unique()
        .tolist()
    )

    return ", ".join(sorted(devices))


def get_user_merchants(user_id):

    merchants = (
        transactions_df[
            transactions_df["user_id"] == user_id
        ]["merchant_id"]
        .dropna()
        .unique()
        .tolist()
    )

    return ", ".join(sorted(merchants))


def get_shared_users(user_id):

    user_transactions = transactions_df[
        transactions_df["user_id"] == user_id
    ]

    devices = (
        user_transactions["device_id"]
        .dropna()
        .unique()
        .tolist()
    )

    if not devices:
        return ""

    shared_users = (
        transactions_df[
            transactions_df["device_id"].isin(devices)
            & (transactions_df["user_id"] != user_id)
        ]["user_id"]
        .dropna()
        .unique()
        .tolist()
    )

    return ", ".join(sorted(shared_users))


user_df["connected_devices"] = (
    user_df["user_id"]
    .apply(get_user_devices)
)

user_df["connected_merchants"] = (
    user_df["user_id"]
    .apply(get_user_merchants)
)

user_df["shared_device_users"] = (
    user_df["user_id"]
    .apply(get_shared_users)
)


# --------------------------------------------------
# Select final output
# --------------------------------------------------

output_columns = [
    "user_id",
    "risk_score",
    "risk_level",
    "ml_prediction",
    "ml_suspicious_probability",
    "ml_risk_level",
    "final_risk_score",
    "final_risk_level",
    "connected_devices",
    "connected_merchants",
    "shared_device_users",
    "risk_reasons"
]


final_df = user_df[output_columns].copy()


# --------------------------------------------------
# Sort by risk
# --------------------------------------------------

final_df = final_df.sort_values(
    "final_risk_score",
    ascending=False
)


# --------------------------------------------------
# Display results
# --------------------------------------------------

print("\nTop 20 users by final risk:")

print(
    final_df[
        [
            "user_id",
            "risk_score",
            "ml_suspicious_probability",
            "final_risk_score",
            "final_risk_level"
        ]
    ]
    .head(20)
    .to_string(index=False)
)


# --------------------------------------------------
# Risk distribution
# --------------------------------------------------

print("\nFinal risk-level distribution:")

print(
    final_df["final_risk_level"]
    .value_counts()
)


# --------------------------------------------------
# Save final results
# --------------------------------------------------

final_df.to_csv(
    OUTPUT_FILE,
    index=False
)

print(
    f"\nSaved final risk results to: "
    f"{OUTPUT_FILE}"
)

print("\nRiskGraph AI application complete.")