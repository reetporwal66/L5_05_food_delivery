
"""Manage food delivery orders, statuses, backups, and revenue."""

import json
from datetime import datetime
from itertools import count

# Global state
orders = {}
ORDER_IDS = count(1)
menu = {}
VALID_STATUSES = ["placed", "cooking", "out_for_delivery", "delivered"]


def create_order(customer, items, order_history=None):
    """Create a food delivery order and return its ID."""
    if order_history is None:
        order_history = []

    total = 0
    for item in items:
        total += menu.get(item, 99)

    order_id = next(ORDER_IDS)

    orders[order_id] = {
        "customer": customer,
        "items": items,
        "total": total,
        "status": "placed"
    }

    order_history.append(order_id)
    return order_history[-1]


def update_order_status(order_id, status):
    """Update an order only if its ID and status are valid."""
    if order_id not in orders:
        return False

    if status not in VALID_STATUSES:
        return False

    orders[order_id]["status"] = status
    return True


def read_menu_config(file="menu.json"):
    """Read menu configuration or use the default menu."""
    try:
        with open(file, "r", encoding="utf-8") as menu_file:
            loaded_menu = json.load(menu_file)
    except (FileNotFoundError, json.JSONDecodeError):
        loaded_menu = {
            "pizza": 250,
            "burger": 150,
            "fries": 90,
            "coke": 40
        }

    menu.clear()
    menu.update(loaded_menu)


def daily_revenue():
    """Calculate revenue from delivered orders."""
    revenue = 0

    for order in orders.values():
        if order["status"] == "delivered":
            revenue += order["total"]

    return revenue


def backup_orders(file="orders.json"):
    """Save all orders to a JSON backup file."""
    with open(file, "w", encoding="utf-8") as backup_file:
        json.dump(orders, backup_file)


def restore_orders(file="orders.json"):
    """Restore orders from a JSON backup file."""
    try:
        with open(file, "r", encoding="utf-8") as backup_file:
            restored_data = json.load(backup_file)

        restored_orders = {
            int(order_id): order
            for order_id, order in restored_data.items()
        }

    except FileNotFoundError:
        restored_orders = {}

    orders.clear()
    orders.update(restored_orders)


def print_queue():
    """Display all orders in the delivery queue."""
    print(f"Order queue at {datetime.now()}")

    for order_id, order in orders.items():
        print(
            order_id,
            order["customer"],
            order["status"],
            order["total"]
        )


def main():
    """Run the food delivery order management program."""
    read_menu_config()

    first_order = create_order("Asha", ["pizza", "coke"])
    second_order = create_order("Ravi", ["burger", "sushi"])
    third_order = create_order("", [])

    update_order_status(first_order, "delivered")
    update_order_status(second_order, "teleported")
    update_order_status(42, "delivered")
    update_order_status(third_order, "delivered")

    print("Revenue today:", daily_revenue())

    backup_orders()
    restore_orders()
    print_queue()


if __name__ == "__main__":
    main()
