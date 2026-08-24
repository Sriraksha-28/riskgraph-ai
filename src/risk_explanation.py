import pandas as pd

INPUT_PATH = "data/user_risk_scores.csv"
OUTPUT_PATH = "data/user_risk_explanations.csv"

print("RiskGraph AI risk explanation")

df = pd.read_csv(INPUT_PATH)

def generate_reasons(row):
    reasons = []

    if row["transactions_per_hour"] >= 60:
        reasons.append("Very high transaction velocity")
    elif row["transactions_per_hour"] >= 30:
        reasons.append("High transaction velocity")

    if row["max_users_on_device_in_window"] >= 6:
        reasons.append("Multiple users sharing the same device")

    if row["max_shared_device_users"] >= 6:
        reasons.append("Device connected to many users")

    if row["merchant_concentration_ratio"] >= 0.80:
        reasons.append("High merchant concentration")

    if row["account_age_days"] <= 7:
        reasons.append("Very new account")

    if row["account_age_days"] <= 30:
        reasons.append("Recently created account")

    if not reasons:
        reasons.append("No major risk indicators detected")

    return "; ".join(reasons)


df["risk_reasons"] = df.apply(generate_reasons, axis=1)

df.to_csv(OUTPUT_PATH, index=False)

print("\nTop users with explanations:")

print(
    df[
        [
            "user_id",
            "risk_score",
            "risk_level",
            "risk_reasons"
        ]
    ]
    .sort_values("risk_score", ascending=False)
    .head(20)
)

print(f"\nSaved explanations to: {OUTPUT_PATH}")
print("Risk explanation complete.")