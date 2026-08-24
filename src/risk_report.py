import pandas as pd

RISK_FILE = "data/user_risk_explanations.csv"
TRANSACTION_FILE = "data/transactions.csv"

print("RiskGraph AI risk report")

# Load data
risk_df = pd.read_csv(RISK_FILE)
transactions_df = pd.read_csv(TRANSACTION_FILE)

print(f"Loaded {len(risk_df)} user risk records")
print(f"Loaded {len(transactions_df)} transactions")

# --------------------------------------------------
# Risk-level summary
# --------------------------------------------------

print("\nRisk-level distribution:")
print(risk_df["risk_level"].value_counts())

# --------------------------------------------------
# Highest-risk users
# --------------------------------------------------

print("\nTop 10 highest-risk users:")

top_users = risk_df.sort_values(
    "risk_score",
    ascending=False
).head(10)

print(
    top_users[
        [
            "user_id",
            "risk_score",
            "risk_level",
            "risk_reasons"
        ]
    ].to_string(index=False)
)

# --------------------------------------------------
# Suspicious transactions
# --------------------------------------------------

suspicious_transactions = transactions_df[
    transactions_df["is_suspicious"] == 1
]

print(
    f"\nSuspicious transactions: "
    f"{len(suspicious_transactions)}"
)

print(
    f"Normal transactions: "
    f"{len(transactions_df) - len(suspicious_transactions)}"
)

# --------------------------------------------------
# Suspicious transaction percentage
# --------------------------------------------------

suspicious_percentage = (
    len(suspicious_transactions)
    / len(transactions_df)
) * 100

print(
    f"Suspicious transaction percentage: "
    f"{suspicious_percentage:.2f}%"
)

# --------------------------------------------------
# Suspicious devices
# --------------------------------------------------

print("\nTop devices involved in suspicious transactions:")

suspicious_devices = (
    suspicious_transactions
    .groupby("device_id")
    .agg(
        suspicious_transactions=("transaction_id", "count"),
        affected_users=("user_id", "nunique")
    )
    .sort_values(
        "suspicious_transactions",
        ascending=False
    )
    .head(10)
)

print(suspicious_devices)

# --------------------------------------------------
# High-risk users
# --------------------------------------------------

high_risk_users = risk_df[
    risk_df["risk_level"] == "HIGH"
]

print(
    f"\nHigh-risk users: "
    f"{len(high_risk_users)}"
)

# --------------------------------------------------
# Save report
# --------------------------------------------------

report = {
    "total_users": len(risk_df),
    "total_transactions": len(transactions_df),
    "normal_transactions": len(transactions_df) - len(suspicious_transactions),
    "suspicious_transactions": len(suspicious_transactions),
    "suspicious_transaction_percentage": round(
        suspicious_percentage,
        2
    ),
    "low_risk_users": int(
        (risk_df["risk_level"] == "LOW").sum()
    ),
    "medium_risk_users": int(
        (risk_df["risk_level"] == "MEDIUM").sum()
    ),
    "high_risk_users": int(
        (risk_df["risk_level"] == "HIGH").sum()
    )
}

report_df = pd.DataFrame(
    [report]
)

report_df.to_csv(
    "data/risk_summary.csv",
    index=False
)

print("\nSaved report to: data/risk_summary.csv")
print("Risk report complete.")