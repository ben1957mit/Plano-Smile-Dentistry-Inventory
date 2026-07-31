"""
Inventory Management System for Plano Smile Dentistry
Features:
- Up to 1000 SKUs
- Barcode-based lookup (works with keyboard-wedge barcode scanners or manual entry)
- Decrement inventory (e.g., when items are used)
- Min/Max levels per SKU
- Category filters:
  PPE, Restorative, Hygiene, Anesthetics, Disposable, Imaging,
  Instruments, Orthodontics, Endodontics, Other
"""

from dataclasses import dataclass, field
from typing import List, Dict, Optional

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


@dataclass
class InventoryItem:
    sku: str
    name: str
    barcode: str
    category: str
    quantity: int
    min_level: int
    max_level: int

    def is_below_min(self) -> bool:
        return self.quantity < self.min_level

    def is_above_max(self) -> bool:
        return self.quantity > self.max_level


@dataclass
class InventorySystem:
    office_name: str = "Plano Smile Dentistry"
    items: Dict[str, InventoryItem] = field(default_factory=dict)  # key: sku

    def add_item(
        self,
        sku: str,
        name: str,
        barcode: str,
        category: str,
        quantity: int,
        min_level: int,
        max_level: int,
    ) -> None:
        if len(self.items) >= 1000:
            print("Inventory limit reached (1000 SKUs). Cannot add more items.")
            return

        if category not in CATEGORIES:
            print(f"Invalid category. Must be one of: {', '.join(CATEGORIES)}")
            return

        if sku in self.items:
            print(f"SKU {sku} already exists. Use update_item to modify.")
            return

        self.items[sku] = InventoryItem(
            sku=sku,
            name=name,
            barcode=barcode,
            category=category,
            quantity=quantity,
            min_level=min_level,
            max_level=max_level,
        )
        print(f"Item {name} (SKU: {sku}) added to inventory.")

    def update_item(
        self,
        sku: str,
        name: Optional[str] = None,
        barcode: Optional[str] = None,
        category: Optional[str] = None,
        quantity: Optional[int] = None,
        min_level: Optional[int] = None,
        max_level: Optional[int] = None,
    ) -> None:
        item = self.items.get(sku)
        if not item:
            print(f"SKU {sku} not found.")
            return

        if name is not None:
            item.name = name
        if barcode is not None:
            item.barcode = barcode
        if category is not None:
            if category not in CATEGORIES:
                print(f"Invalid category. Must be one of: {', '.join(CATEGORIES)}")
                return
            item.category = category
        if quantity is not None:
            item.quantity = quantity
        if min_level is not None:
            item.min_level = min_level
        if max_level is not None:
            item.max_level = max_level

        print(f"Item {sku} updated.")

    def decrement_inventory(self, sku: str, amount: int = 1) -> None:
        item = self.items.get(sku)
        if not item:
            print(f"SKU {sku} not found.")
            return

        if amount <= 0:
            print("Decrement amount must be positive.")
            return

        if item.quantity < amount:
            print(
                f"Not enough quantity to decrement. Current: {item.quantity}, requested: {amount}"
            )
            return

        item.quantity -= amount
        print(
            f"Decremented {amount} from SKU {sku}. New quantity: {item.quantity}"
        )

        if item.is_below_min():
            print(
                f"WARNING: SKU {sku} is below minimum level ({item.quantity} < {item.min_level})."
            )

    def find_by_barcode(self, barcode: str) -> Optional[InventoryItem]:
        for item in self.items.values():
            if item.barcode == barcode:
                return item
        return None

    def find_by_sku(self, sku: str) -> Optional[InventoryItem]:
        return self.items.get(sku)

    def filter_by_category(self, category: str) -> List[InventoryItem]:
        if category not in CATEGORIES:
            print(f"Invalid category. Must be one of: {', '.join(CATEGORIES)}")
            return []
        return [item for item in self.items.values() if item.category == category]

    def list_low_stock(self) -> List[InventoryItem]:
        return [item for item in self.items.values() if item.is_below_min()]

    def list_overstock(self) -> List[InventoryItem]:
        return [item for item in self.items.values() if item.is_above_max()]

    def display_item(self, item: InventoryItem) -> None:
        print(
            f"SKU: {item.sku}\n"
            f"Name: {item.name}\n"
            f"Barcode: {item.barcode}\n"
            f"Category: {item.category}\n"
            f"Quantity: {item.quantity}\n"
            f"Min Level: {item.min_level}\n"
            f"Max Level: {item.max_level}\n"
            f"Below Min: {item.is_below_min()}\n"
            f"Above Max: {item.is_above_max()}\n"
        )

    def display_inventory_summary(self) -> None:
        print(f"Inventory Summary - {self.office_name}")
        print(f"Total SKUs: {len(self.items)}")
        for category in CATEGORIES:
            count = len(self.filter_by_category(category))
            print(f"{category}: {count} items")


def main():
    inv = InventorySystem()

    while True:
        print("\n--- Plano Smile Dentistry Inventory ---")
        print("1. Add Item")
        print("2. Update Item")
        print("3. Decrement Inventory (by SKU)")
        print("4. Lookup by Barcode (scan or type)")
        print("5. Lookup by SKU")
        print("6. Filter by Category")
        print("7. List Low Stock")
        print("8. List Overstock")
        print("9. Inventory Summary")
        print("0. Exit")

        choice = input("Select an option: ").strip()

        if choice == "1":
            sku = input("SKU: ").strip()
            name = input("Name: ").strip()
            barcode = input("Barcode (scan or type): ").strip()
            print(f"Categories: {', '.join(CATEGORIES)}")
            category = input("Category: ").strip()
            quantity = int(input("Quantity: ").strip())
            min_level = int(input("Min Level: ").strip())
            max_level = int(input("Max Level: ").strip())
            inv.add_item(sku, name, barcode, category, quantity, min_level, max_level)

        elif choice == "2":
            sku = input("SKU to update: ").strip()
            print("Leave fields blank to keep current value.")
            name = input("New Name (optional): ").strip()
            barcode = input("New Barcode (optional): ").strip()
            category = input("New Category (optional): ").strip()
            quantity = input("New Quantity (optional): ").strip()
            min_level = input("New Min Level (optional): ").strip()
            max_level = input("New Max Level (optional): ").strip()

            inv.update_item(
                sku,
                name=name or None,
                barcode=barcode or None,
                category=category or None,
                quantity=int(quantity) if quantity else None,
                min_level=int(min_level) if min_level else None,
                max_level=int(max_level) if max_level else None,
            )

        elif choice == "3":
            sku = input("SKU to decrement: ").strip()
            amount_str = input("Amount to decrement (default 1): ").strip()
            amount = int(amount_str) if amount_str else 1
            inv.decrement_inventory(sku, amount)

        elif choice == "4":
            barcode = input("Scan or enter barcode: ").strip()
            item = inv.find_by_barcode(barcode)
            if item:
                inv.display_item(item)
            else:
                print("No item found with that barcode.")

        elif choice == "5":
            sku = input("Enter SKU: ").strip()
            item = inv.find_by_sku(sku)
            if item:
                inv.display_item(item)
            else:
                print("SKU not found.")

        elif choice == "6":
            print(f"Categories: {', '.join(CATEGORIES)}")
            category = input("Category to filter: ").strip()
            items = inv.filter_by_category(category)
            if not items:
                print("No items found for that category.")
            else:
                for item in items:
                    inv.display_item(item)

        elif choice == "7":
            low_stock_items = inv.list_low_stock()
            if not low_stock_items:
                print("No items below minimum level.")
            else:
                print("Items below minimum level:")
                for item in low_stock_items:
                    inv.display_item(item)

        elif choice == "8":
            overstock_items = inv.list_overstock()
            if not overstock_items:
                print("No items above maximum level.")
            else:
                print("Items above maximum level:")
                for item in overstock_items:
                    inv.display_item(item)

        elif choice == "9":
            inv.display_inventory_summary()

        elif choice == "0":
            print("Exiting Plano Smile Dentistry Inventory System.")
            break

        else:
            print("Invalid option. Please try again.")


if __name__ == "__main__":
    main()
