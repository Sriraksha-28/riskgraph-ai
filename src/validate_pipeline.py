from pathlib import Path
import pandas as pd


# ============================================================
# PROJECT PATHS
# ============================================================

PROJECT_ROOT = Path(__file__).resolve().parent.parent
DATA_DIR = PROJECT_ROOT / "data"

FEATURES_FILE = DATA_DIR / "user_features.csv"
RISK_FILE = DATA_DIR / "user_risk_scores.csv"
ML_FILE = DATA_DIR / "ml_risk_predictions.csv"
FINAL_FILE = DATA_DIR / "final_risk_results.csv"


# ============================================================
# HEADER
# ============================================================

print()
print("=" * 70)
print("RISKGRAPH AI — PIPELINE CONSISTENCY VALIDATION")
print("=" * 70)


# ============================================================
# CHECK FILES
# ============================================================

files = {
    "Graph Features": FEATURES_FILE,
    "Risk Scores": RISK_FILE,
    "ML Predictions": ML_FILE,
    "Final Results": FINAL_FILE,
}

print()
print("[1] FILE CHECK")
print("-" * 70)

for name, path in files.items():

    if path.exists():
        print(f"PASS  {name}")
        print(f"      {path}")
    else:
        print(f"FAIL  {name} file not found")
        print(f"      {path}")
        raise SystemExit(1)


# ============================================================
# LOAD DATA
# ============================================================

features = pd.read_csv(FEATURES_FILE)
risk = pd.read_csv(RISK_FILE)
ml = pd.read_csv(ML_FILE)
final = pd.read_csv(FINAL_FILE)


datasets = {
    "Graph Features": features,
    "Risk Scores": risk,
    "ML Predictions": ml,
    "Final Results": final,
}


# ============================================================
# ROW COUNT CHECK
# ============================================================

print()
print("[2] ROW COUNT CONSISTENCY")
print("-" * 70)

for name, df in datasets.items():
    print(f"{name:<20}: {len(df):,}")


row_counts = {
    len(df)
    for df in datasets.values()
}


if len(row_counts) == 1:

    print()
    print(
        "PASS  All pipeline datasets contain "
        "the same number of rows."
    )

else:

    print()
    print(
        "FAIL  Pipeline datasets have different "
        "row counts."
    )


# ============================================================
# USER ID CHECK
# ============================================================

print()
print("[3] USER ID CONSISTENCY")
print("-" * 70)

user_sets = {}

for name, df in datasets.items():

    if "user_id" not in df.columns:

        print(
            f"FAIL  {name} is missing user_id"
        )

        raise SystemExit(1)

    user_sets[name] = set(
        df["user_id"]
        .dropna()
        .astype(str)
    )


base_users = user_sets["Graph Features"]

all_users_match = True


for name, users in user_sets.items():

    if users == base_users:

        print(
            f"PASS  {name} contains the same users"
        )

    else:

        all_users_match = False

        missing = base_users - users
        extra = users - base_users

        print(
            f"FAIL  {name} user IDs do not match"
        )

        print(
            f"      Missing users: {len(missing)}"
        )

        print(
            f"      Extra users:   {len(extra)}"
        )


# ============================================================
# DUPLICATE USER CHECK
# ============================================================

print()
print("[4] DUPLICATE USER CHECK")
print("-" * 70)

for name, df in datasets.items():

    duplicates = (
        df["user_id"]
        .duplicated()
        .sum()
    )

    if duplicates == 0:

        print(
            f"PASS  {name} has no duplicate users"
        )

    else:

        print(
            f"FAIL  {name} contains "
            f"{duplicates} duplicate users"
        )


# ============================================================
# RULE-BASED RISK SCORE CHECK
# ============================================================

print()
print("[5] RULE-BASED RISK SCORE")
print("-" * 70)

if "risk_score" not in risk.columns:

    print(
        "FAIL  risk_score column missing"
    )

else:

    risk_scores = pd.to_numeric(
        risk["risk_score"],
        errors="coerce"
    )

    invalid = (
        risk_scores.isna()
        | (risk_scores < 0)
        | (risk_scores > 100)
    ).sum()

    if invalid == 0:

        print(
            "PASS  All rule-based risk scores "
            "are between 0 and 100"
        )

    else:

        print(
            f"FAIL  {invalid} invalid "
            f"rule-based risk scores"
        )

    print(
        f"Minimum: {risk_scores.min():.2f}"
    )

    print(
        f"Maximum: {risk_scores.max():.2f}"
    )

    print(
        f"Average: {risk_scores.mean():.2f}"
    )


# ============================================================
# ML PROBABILITY CHECK
# ============================================================

print()
print("[6] ML PROBABILITY")
print("-" * 70)

if "ml_suspicious_probability" not in ml.columns:

    print(
        "FAIL  ml_suspicious_probability "
        "column missing"
    )

else:

    probabilities = pd.to_numeric(
        ml["ml_suspicious_probability"],
        errors="coerce"
    )

    invalid = (
        probabilities.isna()
        | (probabilities < 0)
        | (probabilities > 100)
    ).sum()

    if invalid == 0:

        print(
            "PASS  All ML probabilities "
            "are between 0 and 100"
        )

    else:

        print(
            f"FAIL  {invalid} invalid ML probabilities"
        )

    print(
        f"Minimum: {probabilities.min():.2f}%"
    )

    print(
        f"Maximum: {probabilities.max():.2f}%"
    )

    print(
        f"Average: {probabilities.mean():.2f}%"
    )


# ============================================================
# FINAL SCORE CHECK
# ============================================================

print()
print("[7] FINAL RISK SCORE")
print("-" * 70)

if "final_risk_score" not in final.columns:

    print(
        "FAIL  final_risk_score column missing"
    )

else:

    final_scores = pd.to_numeric(
        final["final_risk_score"],
        errors="coerce"
    )

    invalid = (
        final_scores.isna()
        | (final_scores < 0)
        | (final_scores > 100)
    ).sum()

    if invalid == 0:

        print(
            "PASS  All final risk scores "
            "are between 0 and 100"
        )

    else:

        print(
            f"FAIL  {invalid} invalid "
            f"final risk scores"
        )

    print(
        f"Minimum: {final_scores.min():.2f}"
    )

    print(
        f"Maximum: {final_scores.max():.2f}"
    )

    print(
        f"Average: {final_scores.mean():.2f}"
    )


# ============================================================
# RISK LEVEL CHECK
# ============================================================

print()
print("[8] RISK LEVEL VALIDATION")
print("-" * 70)

valid_levels = {
    "LOW",
    "MEDIUM",
    "HIGH",
}


def validate_levels(
    df,
    column,
    name
):

    if column not in df.columns:

        print(
            f"WARNING  {name}: "
            f"{column} column not found"
        )

        return

    levels = set(
        df[column]
        .dropna()
        .astype(str)
        .str.upper()
        .unique()
    )

    invalid = levels - valid_levels

    if not invalid:

        print(
            f"PASS  {name} contains only "
            f"LOW / MEDIUM / HIGH"
        )

    else:

        print(
            f"FAIL  {name} contains invalid levels:"
        )

        for level in invalid:
            print(
                f"      {level}"
            )


validate_levels(
    risk,
    "risk_level",
    "Rule-based risk"
)

validate_levels(
    ml,
    "ml_risk_level",
    "ML risk"
)

validate_levels(
    final,
    "final_risk_level",
    "Final risk"
)


# ============================================================
# FINAL DISTRIBUTION
# ============================================================

print()
print("[9] FINAL RISK DISTRIBUTION")
print("-" * 70)

if "final_risk_level" in final.columns:

    distribution = (
        final["final_risk_level"]
        .astype(str)
        .str.upper()
        .value_counts()
    )

    for level in [
        "HIGH",
        "MEDIUM",
        "LOW",
    ]:

        print(
            f"{level:<8}: "
            f"{distribution.get(level, 0):,}"
        )


# ============================================================
# SAMPLE USER CROSS-CHECK
# ============================================================

print()
print("[10] SAMPLE USER CROSS-CHECK")
print("-" * 70)

sample_users = [
    "U0082",
    "U0064",
    "U0076",
    "U0066",
    "U0071",
]


for user_id in sample_users:

    feature_row = features[
        features["user_id"].astype(str)
        == user_id
    ]

    risk_row = risk[
        risk["user_id"].astype(str)
        == user_id
    ]

    ml_row = ml[
        ml["user_id"].astype(str)
        == user_id
    ]

    final_row = final[
        final["user_id"].astype(str)
        == user_id
    ]


    if (
        feature_row.empty
        or risk_row.empty
        or ml_row.empty
        or final_row.empty
    ):

        print(
            f"FAIL  {user_id} missing from "
            f"one or more datasets"
        )

        continue


    rule_score = float(
        risk_row.iloc[0]["risk_score"]
    )

    ml_probability = float(
        ml_row.iloc[0]["ml_suspicious_probability"]
    )

    final_score = float(
        final_row.iloc[0]["final_risk_score"]
    )

    final_level = (
        final_row.iloc[0]["final_risk_level"]
    )


    print(
        f"{user_id} | "
        f"Rule: {rule_score:.2f} | "
        f"ML: {ml_probability:.2f}% | "
        f"Final: {final_score:.2f} | "
        f"Level: {final_level}"
    )


# ============================================================
# FINAL STATUS
# ============================================================

print()
print("=" * 70)

if all_users_match:

    print(
        "PIPELINE CONSISTENCY VALIDATION — PASS"
    )

else:

    print(
        "PIPELINE CONSISTENCY VALIDATION — CHECK FAILURES"
    )

print("=" * 70)
print()