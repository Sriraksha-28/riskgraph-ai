import pandas as pd
from sklearn.metrics import (
    accuracy_score,
    precision_score,
    recall_score,
    f1_score,
    confusion_matrix
)

RISK_FILE = "data/user_risk_scores.csv"
ML_FILE = "data/ml_risk_predictions.csv"
TRANSACTION_FILE = "data/transactions.csv"
OUTPUT_FILE = "data/ml_evaluation_summary.csv"

print("RiskGraph AI ML evaluation")
print("=" * 50)

# --------------------------------------------------
# Load data
# --------------------------------------------------

risk_df = pd.read_csv(RISK_FILE)
ml_df = pd.read_csv(ML_FILE)
transactions_df = pd.read_csv(TRANSACTION_FILE)

print(f"Loaded {len(risk_df)} risk records")
print(f"Loaded {len(ml_df)} ML predictions")
print(f"Loaded {len(transactions_df)} transactions")

# --------------------------------------------------
# Build actual user-level labels
# --------------------------------------------------

actual_df = (
    transactions_df
    .groupby("user_id")["is_suspicious"]
    .max()
    .reset_index()
    .rename(
        columns={
            "is_suspicious": "actual_suspicious"
        }
    )
)

# --------------------------------------------------
# Merge predictions with actual labels
# --------------------------------------------------

evaluation_df = ml_df.merge(
    actual_df,
    on="user_id",
    how="left"
)

evaluation_df["actual_suspicious"] = (
    evaluation_df["actual_suspicious"]
    .fillna(0)
    .astype(int)
)

y_true = evaluation_df["actual_suspicious"]
y_pred = evaluation_df["ml_prediction"]

# --------------------------------------------------
# Calculate metrics
# --------------------------------------------------

accuracy = accuracy_score(
    y_true,
    y_pred
)

precision = precision_score(
    y_true,
    y_pred,
    zero_division=0
)

recall = recall_score(
    y_true,
    y_pred,
    zero_division=0
)

f1 = f1_score(
    y_true,
    y_pred,
    zero_division=0
)

matrix = confusion_matrix(
    y_true,
    y_pred
)

print("\nML evaluation metrics:")
print(f"Accuracy : {accuracy:.4f}")
print(f"Precision: {precision:.4f}")
print(f"Recall   : {recall:.4f}")
print(f"F1 Score : {f1:.4f}")

print("\nConfusion matrix:")
print(matrix)

# --------------------------------------------------
# Compare with rule-based system
# --------------------------------------------------

rule_df = risk_df[
    [
        "user_id",
        "risk_score",
        "risk_level"
    ]
].copy()

evaluation_df = evaluation_df.merge(
    rule_df,
    on="user_id",
    how="left"
)

evaluation_df["rule_prediction"] = (
    evaluation_df["risk_level"] == "HIGH"
).astype(int)

rule_accuracy = accuracy_score(
    y_true,
    evaluation_df["rule_prediction"]
)

ml_accuracy = accuracy

print("\nRule-based vs ML:")
print(
    f"Rule-based accuracy: {rule_accuracy:.4f}"
)

print(
    f"ML accuracy        : {ml_accuracy:.4f}"
)

print(
    f"Improvement        : "
    f"{ml_accuracy - rule_accuracy:.4f}"
)

# --------------------------------------------------
# Create summary
# --------------------------------------------------

summary_df = pd.DataFrame([
    {
        "model": "Rule-based",
        "accuracy": rule_accuracy,
        "precision": None,
        "recall": None,
        "f1_score": None
    },
    {
        "model": "Random Forest ML",
        "accuracy": accuracy,
        "precision": precision,
        "recall": recall,
        "f1_score": f1
    }
])

# --------------------------------------------------
# Save summary
# --------------------------------------------------

summary_df.to_csv(
    OUTPUT_FILE,
    index=False
)

print(
    f"\nSaved evaluation summary to: "
    f"{OUTPUT_FILE}"
)

print("\nML evaluation complete.")