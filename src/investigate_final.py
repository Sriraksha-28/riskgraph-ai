import sys
import pandas as pd


FINAL_FILE = "data/final_risk_results.csv"
TRANSACTION_FILE = "data/transactions.csv"


def investigate_user(user_id):

    print("RiskGraph AI Final User Investigation")
    print("=" * 55)

    final_df = pd.read_csv(FINAL_FILE)
    transactions_df = pd.read_csv(TRANSACTION_FILE)

    user_data = final_df[
        final_df["user_id"] == user_id
    ]

    if user_data.empty:
        print(f"\nUser {user_id} not found.")
        return

    user = user_data.iloc[0]

    print(f"\nUser: {user_id}")
    print(f"Final Risk Score: {user['final_risk_score']:.2f}")
    print(f"Final Risk Level: {user['final_risk_level']}")

    print(f"\nRule-Based Risk Score: {user['risk_score']:.2f}")
    print(f"Rule-Based Risk Level: {user['risk_level']}")

    print(
        f"\nML Suspicious Probability: "
        f"{user['ml_suspicious_probability']:.2f}%"
    )

    print(
        f"ML Risk Level: "
        f"{user['ml_risk_level']}"
    )

    print("\nRisk Reasons:")

    for reason in str(
        user["risk_reasons"]
    ).split(";"):

        print(f"- {reason.strip()}")

    # --------------------------------------------------
    # User transactions
    # --------------------------------------------------

    user_transactions = transactions_df[
        transactions_df["user_id"] == user_id
    ].copy()

    suspicious = user_transactions[
        user_transactions["is_suspicious"] == 1
    ]

    print(
        f"\nTotal transactions: "
        f"{len(user_transactions)}"
    )

    print(
        f"Suspicious transactions: "
        f"{len(suspicious)}"
    )

    # --------------------------------------------------
    # Connected devices
    # --------------------------------------------------

    devices = sorted(
        user_transactions["device_id"]
        .dropna()
        .unique()
        .tolist()
    )

    print("\nConnected Devices:")

    if devices:
        for device in devices:
            print(f"- {device}")
    else:
        print("- None")

    # --------------------------------------------------
    # Connected merchants
    # --------------------------------------------------

    merchants = sorted(
        user_transactions["merchant_id"]
        .dropna()
        .unique()
        .tolist()
    )

    print("\nConnected Merchants:")

    if merchants:
        for merchant in merchants:
            print(f"- {merchant}")
    else:
        print("- None")

    # --------------------------------------------------
    # Shared device users
    # --------------------------------------------------

    print("\nOther Users Sharing Devices:")

    shared_users = []

    if devices:

        shared_transactions = transactions_df[
            transactions_df["device_id"].isin(devices)
            & (transactions_df["user_id"] != user_id)
        ]

        shared_users = sorted(
            shared_transactions["user_id"]
            .dropna()
            .unique()
            .tolist()
        )

    if shared_users:

        for other_user in shared_users:
            print(f"- {other_user}")

    else:
        print("- None")

    # --------------------------------------------------
    # Suspicious transactions
    # --------------------------------------------------

    if not suspicious.empty:

        print("\nSuspicious Transactions:")

        columns = [
            "transaction_id",
            "device_id",
            "merchant_id",
            "timestamp",
            "amount",
            "location"
        ]

        print(
            suspicious[columns]
            .to_string(index=False)
        )

    else:

        print("\nSuspicious Transactions:")
        print("- None")

    print("\nInvestigation complete.")


# --------------------------------------------------
# Command-line entry point
# --------------------------------------------------

if __name__ == "__main__":

    if len(sys.argv) != 2:

        print(
            "Usage: "
            "python src/investigate_final.py <user_id>"
        )

        print(
            "Example: "
            "python src/investigate_final.py U0082"
        )

        sys.exit(1)

    user_id = sys.argv[1].strip().upper()

    investigate_user(user_id)