import pandas as pd
import streamlit as st

from ui_utils import (
    setup_page,
    render_sidebar,
    render_header,
    render_footer,
    render_kpi_row,
    render_panel_header,
    load_transactions
)


setup_page("Graph Analysis", "🕸️")
render_sidebar()

transactions = load_transactions()

render_header(
    "Graph Analysis",
    "Explore relationships between users, devices and merchants"
)

st.info(
    "RiskGraph AI models relationships between users, "
    "devices and merchants to identify suspicious patterns."
)

st.write("")

render_kpi_row(
    [
        {
            "label": "Unique Devices",
            "value": f"{transactions['device_id'].nunique():,}",
            "icon": "📱",
            "variant": "blue",
        },
        {
            "label": "Unique Merchants",
            "value": f"{transactions['merchant_id'].nunique():,}",
            "icon": "🏪",
            "variant": "blue",
        },
        {
            "label": "Unique Users",
            "value": f"{transactions['user_id'].nunique():,}",
            "icon": "👥",
            "variant": "success",
        },
    ]
)

st.write("")

render_panel_header(
    "Device Sharing Analysis",
    "Devices used by the highest number of distinct users",
    icon="📱",
)

device_users = (
    transactions
    .groupby("device_id")["user_id"]
    .nunique()
    .reset_index(
        name="unique_users"
    )
    .sort_values(
        "unique_users",
        ascending=False
    )
)

st.bar_chart(
    device_users.head(15).set_index(
        "device_id"
    )
)

render_panel_header("Most Shared Devices", icon="📋")

st.dataframe(
    device_users.head(20),
    hide_index=True,
    width="stretch"
)

st.divider()

render_panel_header(
    "Merchant Concentration",
    "Merchants with the highest number of distinct users",
    icon="🏪",
)

merchant_users = (
    transactions
    .groupby("merchant_id")["user_id"]
    .nunique()
    .reset_index(
        name="unique_users"
    )
    .sort_values(
        "unique_users",
        ascending=False
    )
)

st.bar_chart(
    merchant_users.head(15).set_index(
        "merchant_id"
    )
)

render_panel_header("Merchant Connections", icon="📋")

st.dataframe(
    merchant_users.head(20),
    hide_index=True,
    width="stretch"
)

st.divider()

render_panel_header(
    "Shared Device Network",
    "Inspect all users connected through a single device",
    icon="🕸️",
)

with st.container(border=True):

    selected_device = st.selectbox(
        "Select Device",
        sorted(
            transactions["device_id"]
            .dropna()
            .unique()
            .tolist()
        )
    )

    device_data = transactions[
        transactions["device_id"] == selected_device
    ]

    connected_users = sorted(
        device_data["user_id"]
        .dropna()
        .unique()
        .tolist()
    )

    col1, col2 = st.columns(2)

    with col1:
        st.metric("Device", selected_device)

    with col2:
        st.metric("Connected Users", len(connected_users))

    st.write("")

    st.caption("Connected user IDs")
    st.write(", ".join(connected_users))

render_footer()