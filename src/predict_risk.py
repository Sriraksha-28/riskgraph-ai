import joblib
import pandas as pd


MODEL_FILE = "models/risk_model.pkl"
RISK_FILE = "data/user_risk_scores.csv"
TRANSACTION_FILE = "data/transactions.csv"
OUTPUT_FILE = "data/ml_risk_predictions.csv"


print("RiskGraph AI ML risk prediction")
print("=" * 50)


# --------------------------------------------------
# Load trained model
# --------------------------------------------------

model = joblib.load(MODEL_FILE)

print(f"Loaded model: {MODEL_FILE}")


# --------------------------------------------------
# Load data
# --------------------------------------------------

risk_df = pd.read_csv(RISK_FILE)
transactions_df = pd.read_csv(TRANSACTION_FILE)

print(f"Loaded {len(risk_df)} user risk records")
print(f"Loaded {len(transactions_df)} transactions")


# --------------------------------------------------
# Build transaction-level user features
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
# Merge features
# --------------------------------------------------

model_df = risk_df.merge(
    transaction_features,
    on="user_id",
    how="left"
)

model_df = model_df.fillna(0)


# --------------------------------------------------
# Features must match training
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


X = model_df[feature_columns]


# --------------------------------------------------
# Generate predictions
# --------------------------------------------------

predictions = model.predict(X)

probabilities = model.predict_proba(X)

model_df["ml_prediction"] = predictions

model_df["ml_suspicious_probability"] = (
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

    else:
        return "LOW"


model_df["ml_risk_level"] = (
    model_df["ml_suspicious_probability"]
    .apply(get_ml_risk_level)
)


# --------------------------------------------------
# Display top predictions
# --------------------------------------------------

top_predictions = model_df.sort_values(
    "ml_suspicious_probability",
    ascending=False
).head(20)


print("\nTop 20 users by ML suspicious probability:")

print(
    top_predictions[
        [
            "user_id",
            "ml_prediction",
            "ml_suspicious_probability",
            "ml_risk_level"
        ]
    ].to_string(index=False)
)


# --------------------------------------------------
# Distribution
# --------------------------------------------------

print("\nML risk-level distribution:")

print(
    model_df["ml_risk_level"].value_counts()
)


# --------------------------------------------------
# Save predictions
# --------------------------------------------------

output_columns = [
    "user_id",
    "ml_prediction",
    "ml_suspicious_probability",
    "ml_risk_level"
]

model_df[output_columns].to_csv(
    OUTPUT_FILE,
    index=False
)

print(
    f"\nSaved ML predictions to: {OUTPUT_FILE}"
)

print("\nML risk prediction complete.")