import pandas as pd
import joblib

from sklearn.model_selection import train_test_split, cross_validate, StratifiedKFold
from sklearn.ensemble import RandomForestClassifier
from sklearn.metrics import (
    classification_report,
    confusion_matrix,
    accuracy_score,
    precision_score,
    recall_score,
    f1_score
)

RISK_FILE = "data/user_risk_scores.csv"
TRANSACTION_FILE = "data/transactions.csv"

print("RiskGraph AI ML training")
print("=" * 50)

# --------------------------------------------------
# Load data
# --------------------------------------------------

risk_df = pd.read_csv(RISK_FILE)
transactions_df = pd.read_csv(TRANSACTION_FILE)

print(f"Loaded {len(risk_df)} user risk records")
print(f"Loaded {len(transactions_df)} transactions")

# --------------------------------------------------
# Aggregate transaction features per user
# --------------------------------------------------

transaction_features = (
    transactions_df
    .groupby("user_id")
    .agg(
        total_transactions=("transaction_id", "count"),
        average_amount=("amount", "mean"),
        maximum_amount=("amount", "max"),
        suspicious_transaction_count=(
            "is_suspicious",
            "sum"
        ),
        unique_transaction_devices=(
            "device_id",
            "nunique"
        ),
        unique_transaction_merchants=(
            "merchant_id",
            "nunique"
        ),
        unique_locations=(
            "location",
            "nunique"
        )
    )
    .reset_index()
)

# --------------------------------------------------
# Merge user risk features with transaction features
# --------------------------------------------------

model_df = risk_df.merge(
    transaction_features,
    on="user_id",
    how="left"
)

# Fill missing values
model_df = model_df.fillna(0)

print(
    f"Combined model dataset: "
    f"{len(model_df)} users"
)

# --------------------------------------------------
# Select ML features
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
y = model_df["is_suspicious"].astype(int)

print("\nFeature columns:")
for feature in feature_columns:
    print(f"- {feature}")

print("\nTarget distribution:")
print(y.value_counts())

# --------------------------------------------------
# Train/test split
# --------------------------------------------------

X_train, X_test, y_train, y_test = train_test_split(
    X,
    y,
    test_size=0.20,
    random_state=42,
    stratify=y
)

print(
    f"\nTraining samples: {len(X_train)}"
)

print(
    f"Testing samples: {len(X_test)}"
)

# --------------------------------------------------
# Train Random Forest model
# --------------------------------------------------

model = RandomForestClassifier(
    n_estimators=200,
    random_state=42,
    class_weight="balanced",
    max_depth=8,
    min_samples_leaf=2
)

print("\nTraining Random Forest model...")

model.fit(
    X_train,
    y_train
)

print("Model training complete.")

# --------------------------------------------------
# Predictions
# --------------------------------------------------

y_pred = model.predict(X_test)

# --------------------------------------------------
# Evaluation
# --------------------------------------------------

accuracy = accuracy_score(
    y_test,
    y_pred
)

precision = precision_score(
    y_test,
    y_pred,
    zero_division=0
)

recall = recall_score(
    y_test,
    y_pred,
    zero_division=0
)

f1 = f1_score(
    y_test,
    y_pred,
    zero_division=0
)

print("\nModel evaluation:")
print(f"Accuracy : {accuracy:.4f}")
print(f"Precision: {precision:.4f}")
print(f"Recall   : {recall:.4f}")
print(f"F1 Score : {f1:.4f}")

print("\nClassification report:")
print(
    classification_report(
        y_test,
        y_pred,
        zero_division=0
    )
)

print("\nConfusion matrix:")
print(
    confusion_matrix(
        y_test,
        y_pred
    )
)

# --------------------------------------------------
# Feature importance
# --------------------------------------------------

importance_df = pd.DataFrame({
    "feature": feature_columns,
    "importance": model.feature_importances_
}).sort_values(
    "importance",
    ascending=False
)

print("\nFeature importance:")
print(
    importance_df.to_string(index=False)
)

# --------------------------------------------------
# Save feature importance
# --------------------------------------------------

importance_df.to_csv(
    "data/ml_feature_importance.csv",
    index=False
)

print(
    "\nSaved feature importance to: "
    "data/ml_feature_importance.csv"
)
# --------------------------------------------------
# 5-fold cross-validation
# --------------------------------------------------

print("\n5-fold cross-validation:")

cv = StratifiedKFold(
    n_splits=5,
    shuffle=True,
    random_state=42
)

cv_results = cross_validate(
    model,
    X,
    y,
    cv=cv,
    scoring=[
        "accuracy",
        "precision",
        "recall",
        "f1"
    ]
)

print(
    f"CV Accuracy : "
    f"{cv_results['test_accuracy'].mean():.4f}"
)

print(
    f"CV Precision: "
    f"{cv_results['test_precision'].mean():.4f}"
)

print(
    f"CV Recall   : "
    f"{cv_results['test_recall'].mean():.4f}"
)

print(
    f"CV F1 Score : "
    f"{cv_results['test_f1'].mean():.4f}"
)
# --------------------------------------------------
# Save trained model
# --------------------------------------------------

model_path = "models/risk_model.pkl"

joblib.dump(
    model,
    model_path
)

print(
    f"\nSaved trained model to: {model_path}"
)
print("\nML training complete.")