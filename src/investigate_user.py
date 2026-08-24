import sys
import pandas as pd


RISK_FILE = "data/user_risk_explanations.csv"
TRANSACTION_FILE = "data/transactions.csv"


def investigate_user(user_id):
    print("RiskGraph AI user investigation")
    print("=" * 50)

    # Load data
    risk_df = pd.read_csv(RISK_FILE)
    transactions_df = pd.read_csv(TRANSACTION_FILE)

    # Find user
    user_risk = risk_df[
        risk_df["user_id"] == user_id
    ]

    if user_risk.empty:
        print(f"User {user_id} not found.")
        return

    user_risk = user_risk.iloc[0]

    print(f"\nUser: {user_id}")
    print(f"Risk Score: {user_risk['risk_score']:.2f}")
    print(f"Risk Level: {user_risk['risk_level']}")

    print("\nRisk Reasons:")
    for reason in str(user_risk["risk_reasons"]).split(";"):
        print(f"- {reason.strip()}")

    # User transactions
    user_transactions = transactions_df[
        transactions_df["user_id"] == user_id
    ].copy()

    print(
        f"\nTotal transactions: "
        f"{len(user_transactions)}"
    )

    suspicious = user_transactions[
        user_transactions["is_suspicious"] == 1
    ]

    print(
        "\nNote: Risk level is the model's user-level assessment."
    )

    print(
        "Suspicious transactions are based on the dataset's "
        "'is_suspicious' label."
    )

    print(
        f"Suspicious transactions: "
        f"{len(suspicious)}"
    )

    

    # Connected devices
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

    # Connected merchants
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

    # Other users sharing the same devices
    print("\nOther Users Sharing Devices:")

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
    else:
        print("- None")

    # Suspicious transactions for this user
    if not suspicious.empty:
        print("\nSuspicious Transactions:")

        print(
            suspicious[
                [
                    "transaction_id",
                    "device_id",
                    "merchant_id",
                    "timestamp",
                    "amount",
                    "location"
                ]
            ].to_string(index=False)
        )

    print("\nInvestigation complete.")


# --------------------------------------------------
# Command-line entry point
# --------------------------------------------------

if __name__ == "__main__":

    if len(sys.argv) != 2:
        print(
            "Usage: python src/investigate_user.py <user_id>"
        )
        print(
            "Example: python src/investigate_user.py U0082"
        )
        sys.exit(1)

    user_id = sys.argv[1].strip().upper()

    investigate_user(user_id)