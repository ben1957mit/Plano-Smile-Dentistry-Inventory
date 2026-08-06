import streamlit as st
import pandas as pd
import uuid
from datetime import datetime

# -----------------------------
# CONFIG
# -----------------------------
st.set_page_config(page_title="Plano Smile Dentistry Inventory", layout="wide")

CATEGORIES = [
    "PPE", "Restorative", "Hygiene", "Anesthetics", "Disposable",
    "Imaging", "Instruments", "Orthodontics", "Endodontics", "Other"
]

INVENTORY_FILE = "inventory.csv"
RECEIVING_FILE = "receiving.csv"


# -----------------------------
# LOAD / SAVE DATA
# -----------------------------
def load_inventory():
    try:
        df = pd.read_csv(INVENTORY_FILE)

        # Auto-convert old CSVs (fixes KeyError)
        if "quantity" in df.columns and "total_quantity" not in df.columns:
            df["total_quantity"] = df["quantity"]
            df.drop(columns=["quantity"], inplace=True)

        required_cols = [
            "sku", "name", "barcode", "category",
            "total_quantity", "min_level", "max_level"
        ]
        for col in required_cols:
            if col not in df.columns:
                df[col] = 0

        return df

    except FileNotFoundError:
        return pd.DataFrame(columns=[
            "sku", "name", "barcode", "category",
            "total_quantity", "min_level", "max_level"
        ])


def save_inventory(df):
    df.to_csv(INVENTORY_FILE, index=False)


def load_receiving():
    try:
        return pd.read_csv(RECEIVING_FILE)
    except FileNotFoundError:
        return pd.DataFrame(columns=[
            "item_number", "sku", "date_received", "qty_received"
        ])


def save_receiving(df):
    df.to_csv(RECEIVING_FILE, index=False)


inventory = load_inventory()
receiving = load_receiving()


# -----------------------------
# HEADER
# -----------------------------
st.title("Plano Smile Dentistry — Inventory Management System")
st.subheader("Receiving log, barcode scanning, min/max alerts, duplicate removal, and full SKU tracking.")


# -----------------------------
# SIDEBAR NAVIGATION
# -----------------------------
page = st.sidebar.radio(
    "Navigation",
    [
        "Add New SKU",
        "Receive Inventory",
        "Lookup / Scan",
        "Use Inventory",
        "Category Filter",
        "Low Stock",
        "Overstock",
        "Inventory Table",
        "Receiving Log",
        "Remove Duplicates",
        "Summary Dashboard",
    ],
)


# -----------------------------
# ADD NEW SKU
# -----------------------------
if page == "Add New SKU":
    st.header("Add New SKU to Master Inventory")

    sku = st.text_input("SKU (auto-generate if left blank)")
    name = st.text_input("Item Name")
    barcode = st.text_input("Barcode (scan or type)")
    category = st.selectbox("Category", CATEGORIES)
    min_level = st.number_input("Minimum Level", min_value=0, step=1)
    max_level = st.number_input("Maximum Level", min_value=0, step=1)

    if st.button("Add SKU"):
        if sku.strip() == "":
            sku = str(uuid.uuid4())[:8]

        new_row = pd.DataFrame([{
            "sku": sku,
            "name": name,
            "barcode": barcode,
            "category": category,
            "total_quantity": 0,
            "min_level": min_level,
            "max_level": max_level,
        }])

        inventory = pd.concat([inventory, new_row], ignore_index=True)
        save_inventory(inventory)
        st.success(f"SKU '{sku}' added successfully.")


# -----------------------------
# RECEIVE INVENTORY
# -----------------------------
elif page == "Receive Inventory":
    st.header("Receive Inventory — Add Stock to Existing SKU")

    sku = st.text_input("Enter SKU")
    qty_received = st.number_input("Quantity Received", min_value=1, step=1)

    if st.button("Submit Receipt"):
        if sku not in inventory["sku"].values:
            st.error("SKU not found in master inventory.")
        else:
            item_number = len(receiving) + 1
            date_received = datetime.now().strftime("%Y-%m-%d")

            new_receipt = pd.DataFrame([{
                "item_number": item_number,
                "sku": sku,
                "date_received": date_received,
                "qty_received": qty_received
            }])

            receiving = pd.concat([receiving, new_receipt], ignore_index=True)
            save_receiving(receiving)

            idx = inventory[inventory["sku"] == sku].index[0]
            inventory.at[idx, "total_quantity"] += qty_received
            save_inventory(inventory)

            st.success(f"Received {qty_received} units for SKU {sku}. Inventory updated.")


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
# USE INVENTORY
# -----------------------------
elif page == "Use Inventory":
    st.header("Use Inventory — Decrement Stock")

    sku = st.text_input("Enter SKU")
    qty_used = st.number_input("Quantity Used", min_value=1, step=1)

    if st.button("Apply Usage"):
        if sku not in inventory["sku"].values:
            st.error("SKU not found.")
        else:
            idx = inventory[inventory["sku"] == sku].index[0]
            current_qty = inventory.at[idx, "total_quantity"]

            if qty_used > current_qty:
                st.error("Not enough inventory to decrement.")
            else:
                inventory.at[idx, "total_quantity"] = current_qty - qty_used
                save_inventory(inventory)
                st.success(f"New quantity: {current_qty - qty_used}")

                if inventory.at[idx, "total_quantity"] < inventory.at[idx, "min_level"]:
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
    low = inventory[inventory["total_quantity"] < inventory["min_level"]]
    st.dataframe(low)


# -----------------------------
# OVERSTOCK
# -----------------------------
elif page == "Overstock":
    st.header("Items Above Maximum Level")
    over = inventory[inventory["total_quantity"] > inventory["max_level"]]
    st.dataframe(over)


# -----------------------------
# INVENTORY TABLE
# -----------------------------
elif page == "Inventory Table":
    st.header("Full Inventory Table")
    st.dataframe(inventory)


# -----------------------------
# RECEIVING LOG
# ----------------
