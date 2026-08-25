from pathlib import Path
import pandas as pd


# ============================================================
# PROJECT PATHS
# ============================================================

# validate_data.py is inside:
# riskgraph-ai/src/
#
# Therefore:
# parent.parent = riskgraph-ai/

PROJECT_ROOT = Path(__file__).resolve().parent.parent
DATA_DIR = PROJECT_ROOT / "data"


USERS_FILE = DATA_DIR / "users.csv"
RISK_FILE = DATA_DIR / "user_risk_scores.csv"
TRANSACTIONS_FILE = DATA_DIR / "transactions.csv"


# ============================================================
# HELPERS
# ============================================================

def check_file(path: Path, label: str):
    if path.exists():
        print(f"PASS  {label}")
        print(f"      {path}")
        return True

    print(f"FAIL  {label}")
    print(f"      Missing: {path}")
    return False


def load_csv(path: Path, label: str):
    try:
        df = pd.read_csv(path)

        print(f"PASS  {label}")
        print(f"      Rows    : {len(df):,}")
        print(f"      Columns : {len(df.columns)}")

        return df

    except Exception as e:
        print(f"FAIL  {label}")
        print(f"      Error: {e}")
        return None


# ============================================================
# HEADER
# ============================================================

print()
print("=" * 70)
print("RISKGRAPH AI — DATA VALIDATION")
print("=" * 70)

print()
print("Project root:")
print(PROJECT_ROOT)

print()
print("Data directory:")
print(DATA_DIR)


# ============================================================
# 1. DATA FILES
# ============================================================

print()
print("[1] DATA FILES")
print("-" * 70)

print("Users file:")
print(USERS_FILE)

print("Risk file:")
print(RISK_FILE)

print("Transactions file:")
print(TRANSACTIONS_FILE)


# ============================================================
# 2. FILE EXISTENCE
# ============================================================

print()
print("[2] FILE EXISTENCE")
print("-" * 70)

users_exists = check_file(
    USERS_FILE,
    "users.csv found"
)

risk_exists = check_file(
    RISK_FILE,
    "user_risk_scores.csv found"
)

transactions_exists = check_file(
    TRANSACTIONS_FILE,
    "transactions.csv found"
)


if not (
    users_exists
    and risk_exists
    and transactions_exists
):
    print()
    print("Cannot continue because required files are missing.")
    print()
    raise SystemExit(1)


# ============================================================
# 3. LOAD DATA
# ============================================================

print()
print("[3] LOAD DATA")
print("-" * 70)

users = load_csv(
    USERS_FILE,
    "users.csv loaded"
)

risk_scores = load_csv(
    RISK_FILE,
    "user_risk_scores.csv loaded"
)

transactions = load_csv(
    TRANSACTIONS_FILE,
    "transactions.csv loaded"
)


if users is None or risk_scores is None or transactions is None:
    print()
    print("Validation stopped because one or more files could not be loaded.")
    print()
    raise SystemExit(1)


# ============================================================
# 4. BASIC VALIDATION
# ============================================================

print()
print("[4] BASIC VALIDATION")
print("-" * 70)


# ------------------------------------------------------------
# Users
# ------------------------------------------------------------

if "user_id" in users.columns:
    print("PASS  users.csv contains user_id")
else:
    print("FAIL  users.csv missing user_id")


# ------------------------------------------------------------
# Risk scores
# ------------------------------------------------------------

if "user_id" in risk_scores.columns:
    print("PASS  user_risk_scores.csv contains user_id")
else:
    print("FAIL  user_risk_scores.csv missing user_id")


# ------------------------------------------------------------
# Transactions
# ------------------------------------------------------------

required_transaction_columns = [
    "transaction_id",
    "user_id",
    "device_id",
    "merchant_id",
    "timestamp",
    "amount",
    "location",
]


for column in required_transaction_columns:

    if column in transactions.columns:
        print(
            f"PASS  transactions.csv contains '{column}'"
        )
    else:
        print(
            f"FAIL  transactions.csv missing '{column}'"
        )


# ============================================================
# 5. DUPLICATE CHECKS
# ============================================================

print()
print("[5] DUPLICATE CHECKS")
print("-" * 70)


if "user_id" in users.columns:

    duplicate_users = users["user_id"].duplicated().sum()

    if duplicate_users == 0:
        print("PASS  No duplicate user_id values")
    else:
        print(
            f"FAIL  Found {duplicate_users:,} duplicate user_id values"
        )


if "user_id" in risk_scores.columns:

    duplicate_risk_users = (
        risk_scores["user_id"]
        .duplicated()
        .sum()
    )

    if duplicate_risk_users == 0:
        print("PASS  No duplicate user_id values in risk scores")
    else:
        print(
            f"FAIL  Found {duplicate_risk_users:,} duplicate risk-score user_id values"
        )


if "transaction_id" in transactions.columns:

    duplicate_transactions = (
        transactions["transaction_id"]
        .duplicated()
        .sum()
    )

    if duplicate_transactions == 0:
        print("PASS  No duplicate transaction_id values")
    else:
        print(
            f"FAIL  Found {duplicate_transactions:,} duplicate transaction_id values"
        )


# ============================================================
# 6. NULL CHECKS
# ============================================================

print()
print("[6] NULL CHECKS")
print("-" * 70)


def check_nulls(df, name):

    null_count = int(df.isnull().sum().sum())

    if null_count == 0:
        print(f"PASS  {name} contains no null values")
    else:
        print(
            f"WARN  {name} contains {null_count:,} null values"
        )


check_nulls(users, "users.csv")
check_nulls(risk_scores, "user_risk_scores.csv")
check_nulls(transactions, "transactions.csv")


# ============================================================
# 7. RISK LEVEL CHECK
# ============================================================

print()
print("[7] RISK LEVEL VALIDATION")
print("-" * 70)


if "final_risk_level" in risk_scores.columns:

    valid_levels = {
        "LOW",
        "MEDIUM",
        "HIGH",
    }

    actual_levels = set(
        risk_scores["final_risk_level"]
        .dropna()
        .astype(str)
        .str.upper()
        .unique()
    )

    invalid_levels = actual_levels - valid_levels

    if not invalid_levels:

        print(
            "PASS  Risk levels are LOW / MEDIUM / HIGH"
        )

    else:

        print(
            "FAIL  Invalid risk levels found:"
        )

        for level in sorted(invalid_levels):
            print(f"      {level}")


# ============================================================
# 8. TRANSACTION VALIDATION
# ============================================================

print()
print("[8] TRANSACTION VALIDATION")
print("-" * 70)


if "amount" in transactions.columns:

    negative_amounts = (
        transactions["amount"] < 0
    ).sum()

    if negative_amounts == 0:

        print(
            "PASS  No negative transaction amounts"
        )

    else:

        print(
            f"WARN  {negative_amounts:,} negative transaction amounts found"
        )


if "timestamp" in transactions.columns:

    parsed_timestamps = pd.to_datetime(
        transactions["timestamp"],
        errors="coerce"
    )

    invalid_timestamps = parsed_timestamps.isna().sum()

    if invalid_timestamps == 0:

        print(
            "PASS  All transaction timestamps are valid"
        )

    else:

        print(
            f"WARN  {invalid_timestamps:,} invalid timestamps found"
        )


# ============================================================
# 9. DATA SUMMARY
# ============================================================

print()
print("[9] DATA SUMMARY")
print("-" * 70)

print(
    f"Users                 : {len(users):,}"
)

print(
    f"Risk score records    : {len(risk_scores):,}"
)

print(
    f"Transactions          : {len(transactions):,}"
)


if "is_suspicious" in transactions.columns:

    suspicious = (
        transactions["is_suspicious"] == 1
    ).sum()

    rate = (
        suspicious / len(transactions) * 100
        if len(transactions) > 0
        else 0
    )

    print(
        f"Suspicious transactions: {suspicious:,}"
    )

    print(
        f"Suspicious rate       : {rate:.2f}%"
    )


if "final_risk_level" in risk_scores.columns:

    print()
    print("Risk distribution:")

    distribution = (
        risk_scores["final_risk_level"]
        .value_counts()
    )

    for level in ["HIGH", "MEDIUM", "LOW"]:

        print(
            f"  {level:<8}: {distribution.get(level, 0):,}"
        )


# ============================================================
# COMPLETE
# ============================================================

print()
print("=" * 70)
print("DATA VALIDATION COMPLETE")
print("=" * 70)

print()
print(
    "If there are FAIL messages above, fix those before moving "
    "to the next step."
)

print()