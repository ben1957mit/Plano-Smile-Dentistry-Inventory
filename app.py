import streamlit as st
import pandas as pd
import uuid

# -----------------------------
# CONFIG
# -----------------------------
st.set_page_config(page_title="Plano Smile Dentistry Inventory", layout="wide")

CATEGORIES = [
    "PPE",
    "Restorative",
    "Hygiene",
    "Anesthetics",
    "Disposable",
    "Imaging",
    "Instruments",
    "Orthodontics",
    "Endodontics",
    "Other",
]

DATA_FILE = "inventory.csv"


# -----------------------------
# LOAD / SAVE DATA
# -----------------------------
def load_inventory():
    try:
        return pd.read_csv(DATA_FILE)
    except FileNotFoundError:
        return pd.DataFrame(
            columns=[
                "sku",
                "name",
                "barcode",
                "category",
                "quantity",
                "min_level",
                "max_level",
            ]
        )


def save_inventory(df):
    df.to_csv(DATA_FILE, index=False)


inventory = load_inventory()


# -----------------------------
# HEADER
# -----------------------------
st.title("Plano Smile Dentistry — Inventory Management System")
st.subheader("Barcode scanning, min/max alerts, category filters, and 1000 SKU capacity.")


# -----------------------------
# SIDEBAR NAVIGATION
# -----------------------------
page = st.sidebar.radio(
    "Navigation",
    [
        "Add Item",
        "Lookup / Scan",
        "Decrement Inventory",
        "Category Filter",
        "Low Stock",
        "Overstock",
        "Inventory Table",
        "Summary Dashboard",
    ],
)


# -----------------------------
# ADD ITEM
# -----------------------------
if page == "Add Item":
    st.header("Add New Inventory Item")

    sku = st.text_input("SKU (auto-generate if left blank)")
    name = st.text_input("Item Name")
    barcode = st.text_input("Barcode (scan or type)")
    category = st.selectbox("Category", CATEGORIES)
    quantity = st.number_input("Quantity", min_value=0, step=1)
    min_level = st.number_input("Minimum Level", min_value=0, step=1)
    max_level = st.number_input("Maximum Level", min_value=0, step=1)

    if st.button("Add Item"):
        if len(inventory) >= 1000:
            st.error("Inventory limit reached (1000 SKUs).")
        else:
            if sku.strip() == "":
                sku = str(uuid.uuid4())[:8]

            new_row = pd.DataFrame(
                [
                    {
                        "sku": sku,
                        "name": name,
                        "barcode": barcode,
                        "category": category,
                        "quantity": quantity,
                        "min_level": min_level,
                        "max_level": max_level,
                    }
                ]
            )

            inventory = pd.concat([inventory, new_row], ignore_index=True)
            save_inventory(inventory)
            st.success(f"Item '{name}' added successfully.")


# -----------------------------
# LOOKUP / SCAN
# -----------------------------
elif page == "Lookup / Scan":
    st.header("Lookup Item by Barcode or SKU")

    lookup_value = st.text_input("Scan barcode or enter SKU")

    if st.button("Search"):
        result = inventory[
            (inventory["barcode"] == lookup_value)
            | (inventory["sku"] == lookup_value)
        ]

        if result.empty:
            st.error("No item found.")
        else:
            st.success("Item found:")
            st.dataframe(result)


# -----------------------------
# DECREMENT INVENTORY
# -----------------------------
elif page == "Decrement Inventory":
    st.header("Decrement Inventory")

    sku = st.text_input("Enter SKU")
    amount = st.number_input("Amount to decrement", min_value=1, step=1)

    if st.button("Apply Decrement"):
        if sku not in inventory["sku"].values:
            st.error("SKU not found.")
        else:
            idx = inventory[inventory["sku"] == sku].index[0]
            current_qty = inventory.at[idx, "quantity"]

            if current_qty < amount:
                st.error(f"Not enough quantity. Current: {current_qty}")
            else:
                inventory.at[idx, "quantity"] = current_qty - amount
                save_inventory(inventory)
                st.success(f"New quantity: {current_qty - amount}")

                if inventory.at[idx, "quantity"] < inventory.at[idx, "min_level"]:
                    st.warning("⚠ Item is now below minimum level!")


# -----------------------------
# CATEGORY FILTER
# -----------------------------
elif page == "Category Filter":
    st.header("Filter by Category")

    category = st.selectbox("Select Category", CATEGORIES)
    filtered = inventory[inventory["category"] == category]

    st.write(f"Items in category: **{category}**")
    st.dataframe(filtered)


# -----------------------------
# LOW STOCK
# -----------------------------
elif page == "Low Stock":
    st.header("Items Below Minimum Level")

    low = inventory[inventory["quantity"] < inventory["min_level"]]
    st.dataframe(low)


# -----------------------------
# OVERSTOCK
# -----------------------------
elif page == "Overstock":
    st.header("Items Above Maximum Level")

    over = inventory[inventory["quantity"] > inventory["max_level"]]
    st.dataframe(over)


# -----------------------------
# FULL INVENTORY TABLE
# -----------------------------
elif page == "Inventory Table":
    st.header("Full Inventory Table")
    st.dataframe(inventory)


# -----------------------------
# SUMMARY DASHBOARD
# -----------------------------
elif page == "Summary Dashboard":
    st.header("Inventory Summary Dashboard")

    total_skus = len(inventory)
    low_stock = len(inventory[inventory["quantity"] < inventory["min_level"]])
    overstock = len(inventory[inventory["quantity"] > inventory["max_level"]])

    st.metric("Total SKUs", total_skus)
    st.metric("Low Stock Items", low_stock)
    st.metric("Overstock Items", overstock)

    st.subheader("Category Breakdown")
    category_counts = inventory["category"].value_counts()
    st.bar_chart(category_counts)
