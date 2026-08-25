import streamlit as st

from ui_utils import (
    setup_page,
    render_sidebar,
    render_header,
    render_footer,
    render_kpi_row,
    render_panel_header,
    style_levels,
    load_transactions,
)


setup_page("Transactions", "💳")
render_sidebar()

df = load_transactions()

render_header(
    "Transaction Explorer",
    "Search and filter transaction activity"
)

render_panel_header("Transaction Filters", icon="🔍")

with st.container(border=True):

    col1, col2, col3 = st.columns(3)

    with col1:
        status = st.selectbox(
            "Status",
            [
                "All",
                "Suspicious",
                "Normal"
            ]
        )

    with col2:
        locations = [
            "All"
        ] + sorted(
            df["location"]
            .dropna()
            .unique()
            .tolist()
        )

        location = st.selectbox(
            "Location",
            locations
        )

    with col3:
        search_user = st.text_input(
            "User ID",
            placeholder="Example: U0082"
        )

filtered = df.copy()

if status == "Suspicious":
    filtered = filtered[
        filtered["is_suspicious"] == 1
    ]

elif status == "Normal":
    filtered = filtered[
        filtered["is_suspicious"] == 0
    ]

if location != "All":
    filtered = filtered[
        filtered["location"] == location
    ]

if search_user.strip():
    filtered = filtered[
        filtered["user_id"]
        .astype(str)
        .str.upper()
        .str.contains(
            search_user.strip().upper(),
            na=False
        )
    ]

st.write("")

render_kpi_row(
    [
        {
            "label": "Matching Transactions",
            "value": f"{len(filtered):,}",
            "icon": "🔎",
            "variant": "blue",
        },
        {
            "label": "Suspicious",
            "value": f"{int((filtered['is_suspicious'] == 1).sum()):,}",
            "icon": "⚠️",
            "variant": "danger",
        },
        {
            "label": "Total Amount",
            "value": f"₹{filtered['amount'].sum():,.2f}",
            "icon": "💰",
            "variant": "success",
        },
    ]
)

st.write("")

render_panel_header("Transaction Results", icon="📋")

display_columns = [
    "transaction_id",
    "user_id",
    "device_id",
    "merchant_id",
    "timestamp",
    "amount",
    "location",
    "is_suspicious"
]

display = filtered[display_columns].copy()

display["status"] = display[
    "is_suspicious"
].map({
    1: "Suspicious",
    0: "Normal"
})

display = display.drop(
    columns=["is_suspicious"]
)

st.dataframe(
    style_levels(display, ["status"]),
    hide_index=True,
    width="stretch"
)

render_footer()