import random
import pandas as pd


# --------------------------------------------------
# 1. BASIC CONFIGURATION
# --------------------------------------------------

SEED = 42
random.seed(SEED)

print("RiskGraph AI dataset generator")
print(f"Random seed: {SEED}")


# --------------------------------------------------
# 2. GENERATE USERS
# --------------------------------------------------

NUM_USERS = 1000

users = []

for i in range(1, NUM_USERS + 1):
    user_id = f"U{i:04d}"
    account_age_days = random.randint(1, 1000)

    users.append({
        "user_id": user_id,
        "account_age_days": account_age_days
    })

users_df = pd.DataFrame(users)

print(f"Generated {len(users_df)} users")
print(users_df.head())


# --------------------------------------------------
# 3. GENERATE DEVICES
# --------------------------------------------------

NUM_DEVICES = 500

device_types = ["mobile", "desktop", "tablet"]

devices = []

for i in range(1, NUM_DEVICES + 1):
    device_id = f"D{i:04d}"
    device_type = random.choice(device_types)

    devices.append({
        "device_id": device_id,
        "device_type": device_type
    })

devices_df = pd.DataFrame(devices)

print(f"Generated {len(devices_df)} devices")
print(devices_df.head())


# --------------------------------------------------
# 4. GENERATE MERCHANTS
# --------------------------------------------------

NUM_MERCHANTS = 100

merchant_categories = [
    "electronics",
    "fashion",
    "food",
    "travel",
    "gaming",
    "services"
]

merchants = []

for i in range(1, NUM_MERCHANTS + 1):
    merchant_id = f"M{i:03d}"
    category = random.choice(merchant_categories)

    merchants.append({
        "merchant_id": merchant_id,
        "category": category
    })

merchants_df = pd.DataFrame(merchants)

print(f"Generated {len(merchants_df)} merchants")
print(merchants_df.head())


# --------------------------------------------------
# 5. TRANSACTION CONFIGURATION
# --------------------------------------------------

NUM_TRANSACTIONS = 10000

locations = [
    "Bangalore",
    "Chennai",
    "Hyderabad",
    "Mumbai",
    "Delhi",
    "Pune"
]

transactions = []

user_ids = users_df["user_id"].tolist()
device_ids = devices_df["device_id"].tolist()
merchant_ids = merchants_df["merchant_id"].tolist()


# --------------------------------------------------
# 6. DEDICATED SUSPICIOUS ENTITIES
# --------------------------------------------------

# These entities are reserved for our controlled
# suspicious scenarios.

suspicious_users = user_ids[:150]
suspicious_devices = device_ids[:75]
suspicious_merchants = merchant_ids[:25]
normal_users = user_ids[150:]
normal_devices = device_ids[75:]
normal_merchants = merchant_ids[25:]


# --------------------------------------------------
# 7. GENERATE NORMAL TRANSACTIONS
# --------------------------------------------------

NUM_NORMAL_TRANSACTIONS = 8500

for i in range(1, NUM_NORMAL_TRANSACTIONS + 1):

    transaction_id = f"T{i:05d}"

    user_id = random.choice(normal_users)
    device_id = random.choice(normal_devices)
    merchant_id = random.choice(normal_merchants)

    timestamp = pd.Timestamp("2026-08-01") + pd.Timedelta(
        minutes=random.randint(0, 60 * 24 * 30)
    )

    amount = round(random.uniform(100, 10000), 2)

    location = random.choice(locations)

    transactions.append({
        "transaction_id": transaction_id,
        "user_id": user_id,
        "device_id": device_id,
        "merchant_id": merchant_id,
        "timestamp": timestamp,
        "amount": amount,
        "location": location,
        "is_suspicious": 0
    })

print(f"Generated {len(transactions)} normal transactions")


# --------------------------------------------------
# 8. SUSPICIOUS PATTERN 1
# SHARED DEVICE
# --------------------------------------------------

NUM_SHARED_DEVICE_GROUPS = 10
USERS_PER_GROUP = 5

suspicious_start_id = NUM_NORMAL_TRANSACTIONS + 1

for group in range(NUM_SHARED_DEVICE_GROUPS):

    group_users = random.sample(
        suspicious_users,
        USERS_PER_GROUP
    )

    shared_device = suspicious_devices[group]
    shared_merchant = suspicious_merchants[group]

    base_time = pd.Timestamp("2026-08-20") + pd.Timedelta(
        hours=random.randint(0, 24)
    )

    for user_id in group_users:

        timestamp = base_time + pd.Timedelta(
            minutes=random.randint(0, 30)
        )

        amount = round(random.uniform(500, 5000), 2)

        location = random.choice(locations)

        transaction_id = f"T{suspicious_start_id:05d}"
        suspicious_start_id += 1

        transactions.append({
            "transaction_id": transaction_id,
            "user_id": user_id,
            "device_id": shared_device,
            "merchant_id": shared_merchant,
            "timestamp": timestamp,
            "amount": amount,
            "location": location,
            "is_suspicious": 1
        })

print("Generated shared-device suspicious transactions")


# --------------------------------------------------
# 9. SUSPICIOUS PATTERN 2
# HIGH TRANSACTION VELOCITY
# --------------------------------------------------

NUM_VELOCITY_GROUPS = 10
TRANSACTIONS_PER_VELOCITY_GROUP = 10

for group in range(NUM_VELOCITY_GROUPS):

    user_id = suspicious_users[50 + group]

    device_id = suspicious_devices[10 + group]

    merchant_id = suspicious_merchants[10 + group]


    base_time = pd.Timestamp("2026-08-21") + pd.Timedelta(
        hours=random.randint(0, 24)
    )

    for _ in range(TRANSACTIONS_PER_VELOCITY_GROUP):

        timestamp = base_time + pd.Timedelta(
            seconds=random.randint(0, 600)
        )

        amount = round(random.uniform(500, 5000), 2)

        location = random.choice(locations)

        transaction_id = f"T{suspicious_start_id:05d}"
        suspicious_start_id += 1

        transactions.append({
            "transaction_id": transaction_id,
            "user_id": user_id,
            "device_id": device_id,
            "merchant_id": merchant_id,
            "timestamp": timestamp,
            "amount": amount,
            "location": location,
            "is_suspicious": 1
        })

print("Generated high-velocity suspicious transactions")


# --------------------------------------------------
# 10. SUSPICIOUS PATTERN 3
# COORDINATED ABUSE
# --------------------------------------------------

NUM_COORDINATED_GROUPS = 5
USERS_PER_COORDINATED_GROUP = 6
TRANSACTIONS_PER_COORDINATED_USER = 5

for group in range(NUM_COORDINATED_GROUPS):

    start_index = 60 + (
        group * USERS_PER_COORDINATED_GROUP
    )

    group_users = suspicious_users[
        start_index:
        start_index + USERS_PER_COORDINATED_GROUP
    ]

    shared_device = suspicious_devices[20 + group]

    shared_merchant = suspicious_merchants[20 + group]

    base_time = pd.Timestamp("2026-08-22") + pd.Timedelta(
        hours=group
    )

    for user_id in group_users:

        for _ in range(TRANSACTIONS_PER_COORDINATED_USER):

            timestamp = base_time + pd.Timedelta(
                seconds=random.randint(0, 900)
            )

            amount = round(
                random.uniform(1000, 8000),
                2
            )

            location = random.choice(locations)

            transaction_id = f"T{suspicious_start_id:05d}"
            suspicious_start_id += 1

            transactions.append({
                "transaction_id": transaction_id,
                "user_id": user_id,
                "device_id": shared_device,
                "merchant_id": shared_merchant,
                "timestamp": timestamp,
                "amount": amount,
                "location": location,
                "is_suspicious": 1
            })

print("Generated coordinated-abuse suspicious transactions")


# --------------------------------------------------
# 11. CREATE DATAFRAME
# --------------------------------------------------
# --------------------------------------------------
# 11. GENERATE REMAINING NORMAL TRANSACTIONS
# --------------------------------------------------

NUM_REMAINING_NORMAL_TRANSACTIONS = (
    NUM_TRANSACTIONS - len(transactions)
)

for _ in range(NUM_REMAINING_NORMAL_TRANSACTIONS):

    transaction_id = f"T{suspicious_start_id:05d}"
    suspicious_start_id += 1

    user_id = random.choice(normal_users)
    device_id = random.choice(normal_devices)
    merchant_id = random.choice(normal_merchants)

    timestamp = pd.Timestamp("2026-08-23") + pd.Timedelta(
        minutes=random.randint(0, 60 * 24)
    )

    amount = round(random.uniform(100, 10000), 2)

    location = random.choice(locations)

    transactions.append({
        "transaction_id": transaction_id,
        "user_id": user_id,
        "device_id": device_id,
        "merchant_id": merchant_id,
        "timestamp": timestamp,
        "amount": amount,
        "location": location,
        "is_suspicious": 0
    })

print(
    f"Generated {NUM_REMAINING_NORMAL_TRANSACTIONS} "
    "additional normal transactions"
)

transactions_df = pd.DataFrame(transactions)
# --------------------------------------------------
# 12. SAVE DATASETS
# --------------------------------------------------

users_df.to_csv("data/users.csv", index=False)
devices_df.to_csv("data/devices.csv", index=False)
merchants_df.to_csv("data/merchants.csv", index=False)
transactions_df.to_csv("data/transactions.csv", index=False)

print("\nSaved datasets:")
print("data/users.csv")
print("data/devices.csv")
print("data/merchants.csv")
print("data/transactions.csv")

print(f"Total transactions: {len(transactions_df)}")


# --------------------------------------------------
# 12. VALIDATION
# --------------------------------------------------

print("\nSuspicious transactions:")

print(
    transactions_df[
        transactions_df["is_suspicious"] == 1
    ].head(10)
)


print("\nDevices used by suspicious transactions:")

print(
    transactions_df[
        transactions_df["is_suspicious"] == 1
    ]["device_id"].value_counts().head(10)
)


print("\nTransaction label counts:")

print(
    transactions_df["is_suspicious"].value_counts()
)