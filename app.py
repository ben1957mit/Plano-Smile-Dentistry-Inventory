import streamlit as st
import pandas as pd
from datetime import datetime

INVENTORY_FILE = "inventory_master.csv"
RECEIVING_FILE = "inventory_receiving.csv"
USAGE_FILE = "inventory_usage.csv"

# ---------------------------------------------------------
# Load or initialize CSV files
# ---------------------------------------------------------
def load_inventory():
    try:
        return pd.read_csv(INVENTORY_FILE)
    except FileNotFoundError:
        return pd.DataFrame(columns=[
            "sku", "item_name", "category",
            "total_quantity", "min_level", "max_level"
        ])

def load_receiving():
    try:
        return pd.read_csv(RECEIVING_FILE)
    except FileNotFoundError:
        return pd.DataFrame(columns=[
            "item_number", "sku", "date_received", "qty_received"
        ])

def load_usage():
    try:
        return pd.read_csv(USAGE_FILE)
    except FileNotFoundError:
        return pd.DataFrame(columns=[
            "usage_id", "sku", "date_used", "qty_used"
        ])

def save_inventory(df):
    df.to_csv(INVENTORY_FILE, index=False)

def save_receiving(df):
    df.to_csv(RECEIVING_FILE, index=False)

def save_usage(df):
    df.to_csv(USAGE_FILE, index=False)

# ---------------------------------------------------------
# Add new SKU
# ---------------------------------------------------------
def add_new_sku(sku, item_name, category, min_level, max_level):
    inventory = load_inventory()
    if sku in inventory["sku"].values:
        return False, "SKU already exists."

    new_item = pd.DataFrame([{
        "sku": sku,
        "item_name": item_name,
        "category": category,
        "total_quantity": 0,
        "min_level": min_level,
        "max_level": max_level
    }])

    inventory = pd.concat([inventory, new_item], ignore_index=True)
    save_inventory(inventory)
    return True, f"New SKU {sku} added."

# ---------------------------------------------------------
# Receive inventory
# ---------------------------------------------------------
def receive_inventory(sku, qty_received):
    inventory = load_inventory()
    receiving = load_receiving()

    if sku not in inventory["sku"].values:
        return False, "SKU not found."

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

    return True, f"Received {qty_received} units for SKU {sku}."

# ---------------------------------------------------------
# Use inventory
# ---------------------------------------------------------
def use_inventory(sku, qty_used):
    inventory = load_inventory()
    usage = load_usage()

    if sku not in inventory["sku"].values:
        return False, "SKU not found."

    idx = inventory[inventory["sku"] == sku].index[0]
    current_qty = inventory.at[idx, "total_quantity"]

    if qty_used > current_qty:
        return False, "Not enough inventory."

    usage_id = len(usage) + 1
    date_used = datetime.now().strftime("%Y-%m-%d")

    new_usage = pd.DataFrame([{
        "usage_id": usage_id,
        "sku": sku,
        "date_used": date_used,
        "qty_used": qty_used
    }])

    usage = pd.concat([usage, new_usage], ignore_index=True)
    save_usage(usage)

    inventory.at[idx, "total_quantity"] = current_qty - qty_used
    save_inventory(inventory)

    return True, f"Used {qty_used} units of SKU {sku}."

# ---------------------------------------------------------
# STREAMLIT UI
# ---------------------------------------------------------
st.title("Plano Smile Dentistry — Inventory System")

menu = st.sidebar.selectbox(
    "Navigation",
    ["View Inventory", "Add New SKU", "Receive Inventory", "Use Inventory",
     "Receiving Log", "Usage Log", "Barcode Scan Mode"]
)

# ---------------------------------------------------------
# View Inventory
# ---------------------------------------------------------
if menu == "View Inventory":
    st.header("Current Inventory")
    st.dataframe(load_inventory())

# ---------------------------------------------------------
# Add New SKU
# ---------------------------------------------------------
elif menu == "Add New SKU":
    st.header("Add New SKU")

    sku = st.text_input("SKU (Barcode Number)")
    item_name = st.text_input("Item Name")
    category = st.text_input("Category")
    min_level = st.number_input("Min Level", min_value=0)
    max_level = st.number_input("Max Level", min_value=0)

    if st.button("Add SKU"):
        success, message = add_new_sku(sku, item_name, category, min_level, max_level)
        st.success(message) if success else st.error(message)

# ---------------------------------------------------------
# Receive Inventory
# ---------------------------------------------------------
elif menu == "Receive Inventory":
    st.header("Receive Inventory")

    barcode = st.text_input("Scan Barcode (SKU)")
    qty_received = st.number_input("Quantity Received", min_value=1)

    if st.button("Submit"):
        success, message = receive_inventory(barcode, qty_received)
        st.success(message) if success else st.error(message)

# ---------------------------------------------------------
# Use Inventory
# ---------------------------------------------------------
elif menu == "Use Inventory":
    st.header("Use Inventory")

    barcode = st.text_input("Scan Barcode (SKU)")
    qty_used = st.number_input("Quantity Used", min_value=1)

    if st.button("Submit"):
        success, message = use_inventory(barcode, qty_used)
        st.success(message) if success else st.error(message)

# ---------------------------------------------------------
# Receiving Log
# ---------------------------------------------------------
elif menu == "Receiving Log":
    st.header("Receiving Log")
    st.dataframe(load_receiving())

# ---------------------------------------------------------
# Usage Log
# ---------------------------------------------------------
elif menu == "Usage Log":
    st.header("Usage Log")
    st.dataframe(load_usage())

# ---------------------------------------------------------
# Barcode Scan Mode
# ---------------------------------------------------------
elif menu == "Barcode Scan Mode":
    st.header("Live Barcode Scanning Mode")

    st.write("Use your USB barcode scanner — it acts like a keyboard.")

    scanned = st.text_input("Scan Barcode Here")

    if scanned:
        inventory = load_inventory()
        if scanned in inventory["sku"].values:
            item = inventory[inventory["sku"] == scanned].iloc[0]
            st.success(f"Item Found: {item['item_name']} ({item['category']})")
            st.write(f"Current Qty: {item['total_quantity']}")
        else:
            st.error("Barcode not found in inventory.")
