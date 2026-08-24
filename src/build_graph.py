import pandas as pd
import networkx as nx


print("RiskGraph AI graph builder")


# ==================================================
# 1. LOAD DATA
# ==================================================

users_df = pd.read_csv("data/users.csv")
devices_df = pd.read_csv("data/devices.csv")
merchants_df = pd.read_csv("data/merchants.csv")
transactions_df = pd.read_csv("data/transactions.csv")

print(f"Loaded {len(transactions_df)} transactions")


# ==================================================
# 2. INITIALIZE GRAPH
# ==================================================

graph = nx.Graph()

print("Graph initialized")


# Add all user nodes
for user_id in users_df["user_id"]:
    graph.add_node(
        user_id,
        node_type="user"
    )


# Add all device nodes
for device_id in devices_df["device_id"]:
    graph.add_node(
        device_id,
        node_type="device"
    )


# Add all merchant nodes
for merchant_id in merchants_df["merchant_id"]:
    graph.add_node(
        merchant_id,
        node_type="merchant"
    )


print(f"Total nodes: {graph.number_of_nodes()}")
print("User nodes:", len(users_df))
print("Device nodes:", len(devices_df))
print("Merchant nodes:", len(merchants_df))


# ==================================================
# 3. BUILD USER-DEVICE-MERCHANT GRAPH
# ==================================================

for _, transaction in transactions_df.iterrows():

    user_id = transaction["user_id"]
    device_id = transaction["device_id"]
    merchant_id = transaction["merchant_id"]

    # User -> Device
    if graph.has_edge(user_id, device_id):

        graph[user_id][device_id]["transaction_count"] += 1

    else:

        graph.add_edge(
            user_id,
            device_id,
            relationship="uses",
            transaction_count=1
        )

    # User -> Merchant
    if graph.has_edge(user_id, merchant_id):

        graph[user_id][merchant_id]["transaction_count"] += 1

    else:

        graph.add_edge(
            user_id,
            merchant_id,
            relationship="pays",
            transaction_count=1
        )


print(f"Total nodes: {graph.number_of_nodes()}")
print(f"Total edges: {graph.number_of_edges()}")


# ==================================================
# 4. DEVICE SHARING ANALYSIS
# ==================================================

device_risk = []

for device_id in devices_df["device_id"]:

    connected_users = [
        neighbor
        for neighbor in graph.neighbors(device_id)
        if graph.nodes[neighbor]["node_type"] == "user"
    ]

    device_risk.append({
        "device_id": device_id,
        "connected_user_count": len(connected_users)
    })


device_risk_df = pd.DataFrame(device_risk)

print("\nTop devices by connected user count:")

print(
    device_risk_df
    .sort_values(
        "connected_user_count",
        ascending=False
    )
    .head(10)
)


# ==================================================
# 5. VALIDATE DEVICE RISK AGAINST LABELS
# ==================================================

device_validation = (
    transactions_df
    .groupby("device_id")
    .agg(
        total_transactions=("transaction_id", "count"),
        suspicious_transactions=("is_suspicious", "sum")
    )
    .reset_index()
)

device_risk_df = device_risk_df.merge(
    device_validation,
    on="device_id",
    how="left"
)

print("\nDevices with suspicious activity:")

print(
    device_risk_df[
        device_risk_df["suspicious_transactions"] > 0
    ]
    .sort_values(
        "suspicious_transactions",
        ascending=False
    )
    .head(15)
)


# ==================================================
# 6. TRANSACTION VELOCITY
# ==================================================

transactions_df["timestamp"] = pd.to_datetime(
    transactions_df["timestamp"]
)


user_velocity = (
    transactions_df
    .groupby("user_id")
    .agg(
        transaction_count=("transaction_id", "count"),
        first_transaction=("timestamp", "min"),
        last_transaction=("timestamp", "max")
    )
    .reset_index()
)


user_velocity["activity_duration_seconds"] = (
    user_velocity["last_transaction"]
    - user_velocity["first_transaction"]
).dt.total_seconds()


user_velocity["transactions_per_hour"] = 0.0


multi_transaction_users = (
    user_velocity["transaction_count"] > 1
)


user_velocity.loc[
    multi_transaction_users,
    "transactions_per_hour"
] = (
    user_velocity.loc[
        multi_transaction_users,
        "transaction_count"
    ]
    /
    (
        user_velocity.loc[
            multi_transaction_users,
            "activity_duration_seconds"
        ].clip(lower=1)
        / 3600
    )
)


print("\nTop users by transaction velocity:")

print(
    user_velocity
    .sort_values(
        "transactions_per_hour",
        ascending=False
    )
    .head(10)
)


# ==================================================
# 7. VALIDATE VELOCITY
# ==================================================

user_validation = (
    transactions_df
    .groupby("user_id")
    .agg(
        total_transactions=("transaction_id", "count"),
        suspicious_transactions=("is_suspicious", "sum")
    )
    .reset_index()
)


user_velocity_validation = user_velocity.merge(
    user_validation,
    on="user_id",
    how="left"
)


print("\nHigh-velocity users with suspicious activity:")

print(
    user_velocity_validation[
        user_velocity_validation["suspicious_transactions"] > 0
    ]
    .sort_values(
        "transactions_per_hour",
        ascending=False
    )
    .head(15)
)


# ==================================================
# 8. MERCHANT CONCENTRATION
# ==================================================

user_merchant_counts = (
    transactions_df
    .groupby("user_id")["merchant_id"]
    .nunique()
    .reset_index(
        name="unique_merchant_count"
    )
)


user_transaction_counts = (
    transactions_df
    .groupby("user_id")["transaction_id"]
    .count()
    .reset_index(
        name="transaction_count"
    )
)


merchant_concentration = user_merchant_counts.merge(
    user_transaction_counts,
    on="user_id"
)


merchant_concentration["merchant_concentration_ratio"] = (
    1
    -
    (
        merchant_concentration["unique_merchant_count"]
        /
        merchant_concentration["transaction_count"]
    )
)


print("\nTop users by merchant concentration:")

print(
    merchant_concentration
    .sort_values(
        "merchant_concentration_ratio",
        ascending=False
    )
    .head(10)
)


# ==================================================
# 9. ACCOUNT AGE
# ==================================================

user_account_age = users_df[
    [
        "user_id",
        "account_age_days"
    ]
].copy()


print("\nUsers with youngest account ages:")

print(
    user_account_age
    .sort_values(
        "account_age_days",
        ascending=True
    )
    .head(10)
)


# ==================================================
# 10. UNIQUE DEVICE COUNT
# ==================================================

user_device_counts = (
    transactions_df
    .groupby("user_id")["device_id"]
    .nunique()
    .reset_index(
        name="unique_device_count"
    )
)


# ==================================================
# 11. LONG-TERM SHARED DEVICE SIGNAL
# ==================================================

device_user_counts = (
    transactions_df
    .groupby("device_id")["user_id"]
    .nunique()
    .reset_index(
        name="device_user_count"
    )
)


transaction_device_risk = transactions_df[
    [
        "user_id",
        "device_id"
    ]
].drop_duplicates()


transaction_device_risk = transaction_device_risk.merge(
    device_user_counts,
    on="device_id",
    how="left"
)


user_shared_device_risk = (
    transaction_device_risk
    .groupby("user_id")["device_user_count"]
    .max()
    .reset_index(
        name="max_shared_device_users"
    )
)


# ==================================================
# 12. SHORT-WINDOW SHARED DEVICE SIGNAL
# ==================================================

print("\nCalculating short-window shared-device risk...")


device_window_risk = []


for device_id, device_transactions in transactions_df.groupby(
    "device_id"
):

    device_transactions = (
        device_transactions
        .sort_values("timestamp")
        .reset_index(drop=True)
    )

    timestamps = device_transactions[
        "timestamp"
    ].tolist()

    users = device_transactions[
        "user_id"
    ].tolist()


    for i in range(len(device_transactions)):

        window_start = timestamps[i]

        window_end = (
            window_start
            + pd.Timedelta(minutes=15)
        )

        window_users = set()


        for j in range(
            i,
            len(device_transactions)
        ):

            if timestamps[j] <= window_end:

                window_users.add(
                    users[j]
                )

            else:

                break


        device_window_risk.append({
            "device_id": device_id,
            "window_start": window_start,
            "window_user_count": len(window_users)
        })


device_window_risk_df = pd.DataFrame(
    device_window_risk
)


device_max_window = (
    device_window_risk_df
    .groupby("device_id")["window_user_count"]
    .max()
    .reset_index(
        name="max_users_on_device_in_window"
    )
)


# Attach device signal to users

user_device_window = transactions_df[
    [
        "user_id",
        "device_id"
    ]
].drop_duplicates()


user_device_window = user_device_window.merge(
    device_max_window,
    on="device_id",
    how="left"
)


user_short_window_risk = (
    user_device_window
    .groupby("user_id")[
        "max_users_on_device_in_window"
    ]
    .max()
    .reset_index(
        name="max_users_on_device_in_window"
    )
)


print(
    "\nTop users by short-window shared-device activity:"
)


print(
    user_short_window_risk
    .sort_values(
        "max_users_on_device_in_window",
        ascending=False
    )
    .head(15)
)


# ==================================================
# 13. BUILD UNIFIED USER FEATURES
# ==================================================

user_features = (
    user_account_age

    .merge(
        user_velocity[
            [
                "user_id",
                "transaction_count",
                "transactions_per_hour"
            ]
        ],
        on="user_id",
        how="left"
    )

    .merge(
        merchant_concentration[
            [
                "user_id",
                "unique_merchant_count",
                "merchant_concentration_ratio"
            ]
        ],
        on="user_id",
        how="left"
    )

    .merge(
        user_device_counts,
        on="user_id",
        how="left"
    )

    .merge(
        user_shared_device_risk,
        on="user_id",
        how="left"
    )

    .merge(
        user_short_window_risk,
        on="user_id",
        how="left"
    )
)


# ==================================================
# 14. FILL MISSING ACTIVITY FEATURES
# ==================================================

activity_columns = [
    "transaction_count",
    "transactions_per_hour",
    "unique_merchant_count",
    "merchant_concentration_ratio",
    "unique_device_count",
    "max_shared_device_users",
    "max_users_on_device_in_window"
]


user_features[activity_columns] = (
    user_features[activity_columns]
    .fillna(0)
)


print("\nUnified user risk features:")

print(
    user_features.head(10)
)


print(
    f"Total user feature rows: {len(user_features)}"
)


# ==================================================
# 15. ADD GROUND-TRUTH LABELS
# ==================================================

user_labels = (
    transactions_df
    .groupby("user_id")["is_suspicious"]
    .max()
    .reset_index(
        name="is_suspicious"
    )
)


user_features = user_features.merge(
    user_labels,
    on="user_id",
    how="left"
)


user_features["is_suspicious"] = (
    user_features["is_suspicious"]
    .fillna(0)
)


# ==================================================
# 16. SHOW SUSPICIOUS USERS
# ==================================================

print("\nSuspicious users by combined features:")


print(
    user_features[
        user_features["is_suspicious"] == 1
    ]
    .sort_values(
        [
            "transactions_per_hour",
            "merchant_concentration_ratio"
        ],
        ascending=False
    )
    .head(20)
)


# ==================================================
# 17. RISK-SCORE THRESHOLD ANALYSIS
# ==================================================

print("\nRisk-score threshold analysis:")


print(
    "Velocity >= 60:",
    (
        user_features[
            "transactions_per_hour"
        ] >= 60
    ).sum()
)


print(
    "Velocity 30-59:",
    (
        (
            user_features[
                "transactions_per_hour"
            ] >= 30
        )
        &
        (
            user_features[
                "transactions_per_hour"
            ] < 60
        )
    ).sum()
)


print(
    "Long-term shared device >= 6 users:",
    (
        user_features[
            "max_shared_device_users"
        ] >= 6
    ).sum()
)


print(
    "Long-term shared device 3-5 users:",
    (
        (
            user_features[
                "max_shared_device_users"
            ] >= 3
        )
        &
        (
            user_features[
                "max_shared_device_users"
            ] < 6
        )
    ).sum()
)


print(
    "Short-window shared device >= 6 users:",
    (
        user_features[
            "max_users_on_device_in_window"
        ] >= 6
    ).sum()
)


print(
    "Short-window shared device 3-5 users:",
    (
        (
            user_features[
                "max_users_on_device_in_window"
            ] >= 3
        )
        &
        (
            user_features[
                "max_users_on_device_in_window"
            ] < 6
        )
    ).sum()
)


print(
    "Merchant concentration >= 0.80:",
    (
        user_features[
            "merchant_concentration_ratio"
        ] >= 0.80
    ).sum()
)


print(
    "Merchant concentration 0.60-0.79:",
    (
        (
            user_features[
                "merchant_concentration_ratio"
            ] >= 0.60
        )
        &
        (
            user_features[
                "merchant_concentration_ratio"
            ] < 0.80
        )
    ).sum()
)


print(
    "Account age <= 7 days:",
    (
        user_features[
            "account_age_days"
        ] <= 7
    ).sum()
)


print(
    "Account age 8-30 days:",
    (
        (
            user_features[
                "account_age_days"
            ] > 7
        )
        &
        (
            user_features[
                "account_age_days"
            ] <= 30
        )
    ).sum()
)


# ==================================================
# 18. FINAL FEATURE SUMMARY
# ==================================================

print("\nFinal user feature columns:")
print(user_features.columns.tolist())

user_features.to_csv("data/user_features.csv", index=False)
print("Saved user features to: data/user_features.csv")

print("\nRiskGraph AI graph feature engineering complete.")