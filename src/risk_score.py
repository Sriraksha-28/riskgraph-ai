import pandas as pd

print("RiskGraph AI risk scoring")

# Load the engineered user features
features_path = "data/user_features.csv"

try:
    df = pd.read_csv(features_path)
except FileNotFoundError:
    print(f"ERROR: {features_path} not found.")
    print("First make sure build_graph.py saves user_features.csv.")
    raise

print(f"Loaded {len(df)} user feature rows")

# --------------------------------------------------
# Fill missing values
# --------------------------------------------------

numeric_columns = [
    "account_age_days",
    "transaction_count",
    "transactions_per_hour",
    "unique_merchant_count",
    "merchant_concentration_ratio",
    "unique_device_count",
    "max_shared_device_users",
    "max_users_on_device_in_window",
]

for column in numeric_columns:
    if column in df.columns:
        df[column] = df[column].fillna(0)

# --------------------------------------------------
# Risk components
# --------------------------------------------------

# 1. Transaction velocity
df["velocity_score"] = (
    df["transactions_per_hour"]
    .clip(upper=100)
    / 100
)

# 2. Short-window shared-device activity
df["short_window_device_score"] = (
    (df["max_users_on_device_in_window"] - 1)
    / 5
).clip(lower=0, upper=1)

# 3. Merchant concentration
df["merchant_score"] = (
    df["merchant_concentration_ratio"]
    .clip(lower=0, upper=1)
)

# 4. Account age risk
df["account_age_score"] = (
    (30 - df["account_age_days"])
    / 30
).clip(lower=0, upper=1)

# 5. Long-term shared-device activity
df["shared_device_score"] = (
    (df["max_shared_device_users"] - 1)
    / 5
).clip(lower=0, upper=1)

# --------------------------------------------------
# Combined risk score
# --------------------------------------------------

df["risk_score"] = (
    0.30 * df["velocity_score"]
    + 0.30 * df["short_window_device_score"]
    + 0.15 * df["merchant_score"]
    + 0.10 * df["account_age_score"]
    + 0.15 * df["shared_device_score"]
)

# Convert to 0-100
df["risk_score"] = (df["risk_score"] * 100).round(2)

# --------------------------------------------------
# Risk categories
# --------------------------------------------------

def classify_risk(score):
    if score >= 70:
        return "HIGH"
    elif score >= 40:
        return "MEDIUM"
    else:
        return "LOW"


df["risk_level"] = df["risk_score"].apply(classify_risk)

# --------------------------------------------------
# Display results
# --------------------------------------------------

print("\nTop 20 users by risk score:")

print(
    df[
        [
            "user_id",
            "risk_score",
            "risk_level",
            "transactions_per_hour",
            "max_shared_device_users",
            "max_users_on_device_in_window",
            "merchant_concentration_ratio",
            "account_age_days",
        ]
    ]
    .sort_values("risk_score", ascending=False)
    .head(20)
)

print("\nRisk-level distribution:")
print(df["risk_level"].value_counts())

print("\nSuspicious users with highest risk scores:")

if "is_suspicious" in df.columns:
    suspicious = df[df["is_suspicious"] == 1].sort_values(
        "risk_score",
        ascending=False
    )

    print(
        suspicious[
            [
                "user_id",
                "risk_score",
                "risk_level",
                "transactions_per_hour",
                "max_shared_device_users",
                "max_users_on_device_in_window",
                "merchant_concentration_ratio",
                "account_age_days",
            ]
        ].head(20)
    )

# --------------------------------------------------
# Save results
# --------------------------------------------------

output_path = "data/user_risk_scores.csv"

df.to_csv(output_path, index=False)

print(f"\nSaved risk scores to: {output_path}")
print("Risk scoring complete.")