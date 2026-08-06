import pandas as pd
from datetime import datetime

# ---------------------------------------------------------
# File paths
# ---------------------------------------------------------
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
# Add new SKU to master inventory
# ---------------------------------------------------------
def add_new_sku(sku, item_name, category, min_level=0, max_level=0):
    inventory = load_inventory()

    if sku in inventory["sku"].values:
        print(f"SKU {sku} already exists.")
        return

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

    print(f"New SKU {sku} added successfully.")


# ---------------------------------------------------------
# Receive inventory (adds quantity + logs receipt)
# ---------------------------------------------------------
def receive_inventory(sku, qty_received):
    inventory = load_inventory()
    receiving = load_receiving()

    if sku not in inventory["sku"].values:
        print(f"SKU {sku} not found in inventory.")
        return

    # Create receiving entry
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

    # Update inventory total
    idx = inventory[inventory["sku"] == sku].index[0]
    inventory.at[idx, "total_quantity"] += qty_received
    save_inventory(inventory)

    print(f"Received {qty_received} units for SKU {sku}. Inventory updated.")


# ---------------------------------------------------------
# Use inventory (subtract quantity + log usage)
# ---------------------------------------------------------
def use_inventory(sku, qty_used):
    inventory = load_inventory()
    usage = load_usage()

    if sku not in inventory["sku"].values:
        print(f"SKU {sku} not found.")
        return

    idx = inventory[inventory["sku"] == sku].index[0]
    current_qty = inventory.at[idx, "total_quantity"]

    if qty_used > current_qty:
        print("Not enough inventory to use that amount.")
        return

    # Log usage
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

    # Update inventory
    inventory.at[idx, "total_quantity"] = current_qty - qty_used
    save_inventory(inventory)

    print(f"Used {qty_used} units of SKU {sku}. New quantity: {current_qty - qty_used}")


# ---------------------------------------------------------
# View inventory
# ---------------------------------------------------------
def view_inventory():
    inventory = load_inventory()
    print(inventory)


# ---------------------------------------------------------
# View receiving log
# ---------------------------------------------------------
def view_receiving_log():
    receiving = load_receiving()
    print(receiving)


# ---------------------------------------------------------
# View usage log
# ---------------------------------------------------------
def view_usage_log():
    usage = load_usage()
    print(usage)


# ---------------------------------------------------------
# Example usage (remove or modify for Streamlit)
# ---------------------------------------------------------
if __name__ == "__main__":
    # Example actions:
    # add_new_sku("A100", "Gloves Small", "PPE", 50, 300)
    # receive_inventory("A100", 120)
    # use_inventory("A100", 20)
    view_inventory()

