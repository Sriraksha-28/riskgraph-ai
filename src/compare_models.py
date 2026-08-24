import pandas as pd

RISK_FILE = "data/user_risk_scores.csv"
ML_FILE = "data/ml_risk_predictions.csv"
TRANSACTION_FILE = "data/transactions.csv"
OUTPUT_FILE = "data/model_comparison.csv"

print("RiskGraph AI model comparison")
print("=" * 50)

# Load data
risk_df = pd.read_csv(RISK_FILE)
ml_df = pd.read_csv(ML_FILE)
transactions_df = pd.read_csv(TRANSACTION_FILE)

# Get actual user-level suspicious label
actual_df = (
    transactions_df
    .groupby("user_id")["is_suspicious"]
    .max()
    .reset_index()
    .rename(columns={"is_suspicious": "actual_suspicious"})
)

# Combine rule-based risk, ML prediction, and actual label
comparison_df = (
    risk_df[
        [
            "user_id",
            "risk_score",
            "risk_level"
        ]
    ]
    .merge(
        ml_df[
            [
                "user_id",
                "ml_prediction",
                "ml_suspicious_probability",
                "ml_risk_level"
            ]
        ],
        on="user_id",
        how="left"
    )
    .merge(
        actual_df,
        on="user_id",
        how="left"
    )
)

comparison_df["actual_suspicious"] = (
    comparison_df["actual_suspicious"]
    .fillna(0)
    .astype(int)
)

# Rule-based prediction
comparison_df["rule_prediction"] = (
    comparison_df["risk_level"] == "HIGH"
).astype(int)

# Compare rule-based predictions
rule_correct = (
    comparison_df["rule_prediction"]
    == comparison_df["actual_suspicious"]
).sum()

rule_accuracy = (
    rule_correct / len(comparison_df)
)

# Compare ML predictions
ml_correct = (
    comparison_df["ml_prediction"]
    == comparison_df["actual_suspicious"]
).sum()

ml_accuracy = (
    ml_correct / len(comparison_df)
)

print("\nRule-based risk engine:")
print(
    f"Accuracy: {rule_accuracy:.4f}"
)

print(
    f"Correct predictions: "
    f"{rule_correct}/{len(comparison_df)}"
)

print("\nML model:")
print(
    f"Accuracy: {ml_accuracy:.4f}"
)

print(
    f"Correct predictions: "
    f"{ml_correct}/{len(comparison_df)}"
)

# Agreement between systems
agreement = (
    comparison_df["rule_prediction"]
    == comparison_df["ml_prediction"]
).sum()

agreement_rate = agreement / len(comparison_df)

print("\nModel agreement:")
print(
    f"{agreement}/{len(comparison_df)} "
    f"({agreement_rate:.2%})"
)

# Users where the systems disagree
disagreements = comparison_df[
    comparison_df["rule_prediction"]
    != comparison_df["ml_prediction"]
].copy()

print(
    f"\nUsers where rule-based and ML predictions disagree: "
    f"{len(disagreements)}"
)

if not disagreements.empty:
    print(
        disagreements[
            [
                "user_id",
                "risk_score",
                "risk_level",
                "ml_suspicious_probability",
                "ml_risk_level",
                "actual_suspicious"
            ]
        ]
        .sort_values(
            "ml_suspicious_probability",
            ascending=False
        )
        .head(20)
        .to_string(index=False)
    )

# Save comparison
comparison_df.to_csv(
    OUTPUT_FILE,
    index=False
)

print(
    f"\nSaved comparison to: {OUTPUT_FILE}"
)

print("\nModel comparison complete.")