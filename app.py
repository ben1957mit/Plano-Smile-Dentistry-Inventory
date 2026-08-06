import pandas as pd
from datetime import datetime

INVENTORY_FILE = "inventory_master.csv"
RECEIVING_FILE = "inventory_receiving.csv"

# ---------------------------------------------------------
# Load or initialize data files
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

def save_inventory(df):
    df.to_csv(INVENTORY_FILE, index=False)

def save_receiving(df):
    df.to_csv(RECEIVING_FILE, index=False)


# ---------------------------------------------------------
# Add new inventory receipt
# ---------------------------------------------------------
def receive_inventory(sku, qty_received):
    inventory = load_inventory()
    receiving = load_receiving()

    # Validate SKU exists
    if sku not in inventory["sku"].values:
        print(f"SKU {sku} not found in master inventory.")
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

    # Update master inventory total
    idx = inventory[inventory["sku"] == sku].index[0]
    inventory.at[idx, "total_quantity"] += qty_received
    save_inventory(inventory)

    print(f"Received {qty_received} units for SKU {sku}. Inventory updated.")


# ---------------------------------------------------------
# Add new SKU to master inventory
# ---------------------------------------------------------
def add_new_sku(sku, item_name, category, min_level, max_level):
    inventory = load_inventory()

    if sku in inventory["sku"].values:
        print("SKU already exists.")
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

    print(f"New SKU {sku} added to inventory.")


# ---------------------------------------------------------
# Decrement inventory (usage)
# ---------------------------------------------------------
def use_inventory(sku, qty_used):
    inventory = load_inventory()

    if sku not in inventory["sku"].values:
        print("SKU not found.")
        return

    idx = inventory[inventory["sku"] == sku].index[0]
    current_qty = inventory.at[idx, "total_quantity"]

    if qty_used > current_qty:
        print("Not enough inventory to decrement.")
        return

    inventory.at[idx, "total_quantity"] = current_qty - qty_used
    save_inventory(inventory)

    print(f"Used {qty_used} units of SKU {sku}. New quantity: {current_qty - qty_used}")


# ---------------------------------------------------------
# View inventory
# ---------------------------------------------------------
def view_inventory():
    inventory = load_inventory()
    print(inventory—
