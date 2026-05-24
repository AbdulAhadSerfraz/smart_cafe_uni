"""
Order management module for Smart Cafe Ordering System.

This module handles creating orders, adding items to orders,
and saving/loading order history from files.
"""

import os
from datetime import datetime
from menu_item import MenuItem

# Base directory for data files (resolved relative to this script)
BASE_DIR = os.path.dirname(os.path.abspath(__file__))


class OrderItem:
    """
    Represents a single item in an order with quantity.

    Attributes:
        menu_item (MenuItem): The menu item ordered
        quantity (int): Quantity ordered
    """

    def __init__(self, menu_item, quantity=1):
        """
        Initialize an order item.

        Args:
            menu_item (MenuItem): The menu item being ordered
            quantity (int): Quantity of the item
        """
        self.menu_item = menu_item
        self.quantity = quantity

    def get_subtotal(self):
        """
        Calculate subtotal for this order item.

        Returns:
            float: Price * Quantity
        """
        return self.menu_item.price * self.quantity

    def __str__(self):
        """
        Return a readable string for this order item.
        """
        return f"{self.menu_item.name} x{self.quantity} = ${self.get_subtotal():.2f}"


class Order:
    """
    Represents a customer order.

    Each order has a unique ID, a list of OrderItems,
    a timestamp, and a status.

    Attributes:
        order_id (str): Unique order identifier
        items (list): List of OrderItem objects
        customer_name (str): Name of the customer
        order_time (datetime): When the order was placed
        status (str): Current order status
    """

    # Class variable to track all valid statuses
    VALID_STATUSES = ["Pending", "Preparing", "Ready", "Completed", "Cancelled"]

    def __init__(self, order_id, customer_name="Guest"):
        """
        Initialize a new Order.

        Args:
            order_id (str): Unique order ID
            customer_name (str): Name of the customer
        """
        self.order_id = order_id
        self.items = []  # List of OrderItem objects
        self.customer_name = customer_name
        self.order_time = datetime.now()
        self.status = "Pending"

    def add_item(self, menu_item, quantity=1):
        """
        Add a menu item to the order.

        Args:
            menu_item (MenuItem): The item to add
            quantity (int): Quantity to add (default: 1)

        Returns:
            bool: True if item was added
        """
        if quantity <= 0:
            print("[ERROR] Quantity must be at least 1.")
            return False

        # Check if item already exists in order, then increase quantity
        for order_item in self.items:
            if order_item.menu_item.item_id == menu_item.item_id:
                order_item.quantity += quantity
                print(f"[INFO] Increased '{menu_item.name}' quantity to {order_item.quantity}.")
                return True

        # Otherwise add new item
        new_item = OrderItem(menu_item, quantity)
        self.items.append(new_item)
        print(f"[SUCCESS] Added '{menu_item.name}' x{quantity} to order.")
        return True

    def remove_item(self, menu_item_id):
        """
        Remove an item from the order by menu item ID.

        Args:
            menu_item_id (str): The menu item ID to remove

        Returns:
            bool: True if item was removed
        """
        for order_item in self.items:
            if order_item.menu_item.item_id == menu_item_id:
                self.items.remove(order_item)
                print(f"[SUCCESS] Removed '{order_item.menu_item.name}' from order.")
                return True

        print(f"[ERROR] Item with ID '{menu_item_id}' not found in order.")
        return False

    def update_item_quantity(self, menu_item_id, new_quantity):
        """
        Update the quantity of a specific item in the order.

        Args:
            menu_item_id (str): The menu item ID
            new_quantity (int): New quantity

        Returns:
            bool: True if quantity was updated
        """
        if new_quantity <= 0:
            print("[ERROR] Quantity must be at least 1.")
            return False

        for order_item in self.items:
            if order_item.menu_item.item_id == menu_item_id:
                order_item.quantity = new_quantity
                print(f"[SUCCESS] Updated '{order_item.menu_item.name}' quantity to {new_quantity}.")
                return True

        print(f"[ERROR] Item with ID '{menu_item_id}' not found in order.")
        return False

    def get_total(self):
        """
        Calculate the total price of the order.

        Returns:
            float: Total price of all items combined
        """
        total = sum(item.get_subtotal() for item in self.items)
        return total

    def get_item_count(self):
        """
        Get the total number of items (sum of quantities).

        Returns:
            int: Total quantity of all items
        """
        return sum(item.quantity for item in self.items)

    def update_status(self, new_status):
        """
        Update the status of the order.

        Args:
            new_status (str): New status value

        Returns:
            bool: True if status was updated
        """
        if new_status not in Order.VALID_STATUSES:
            print(f"[ERROR] Invalid status. Valid statuses: {Order.VALID_STATUSES}")
            return False

        old_status = self.status
        self.status = new_status
        print(f"[SUCCESS] Order #{self.order_id} status changed from '{old_status}' to '{new_status}'.")
        return True

    def display_order(self):
        """
        Display the order details in a formatted way.
        """
        print("\n" + "=" * 50)
        print(f"ORDER #{self.order_id}")
        print("=" * 50)
        print(f"Customer: {self.customer_name}")
        print(f"Time: {self.order_time.strftime('%Y-%m-%d %H:%M:%S')}")
        print(f"Status: {self.status}")
        print("-" * 50)

        if not self.items:
            print("  (No items in this order)")
        else:
            print(f"{'#':<3} {'Item':<25} {'Qty':<5} {'Price':>8}")
            print("-" * 50)
            for i, item in enumerate(self.items, 1):
                line_price = item.menu_item.price * item.quantity
                print(f"{i:<3} {item.menu_item.name:<25} {item.quantity:<5} ${line_price:>6.2f}")

        print("-" * 50)
        print(f"{'TOTAL':>40} ${self.get_total():>6.2f}")
        print("=" * 50)

    def to_file_format(self):
        """
        Convert the order to a string for file saving.

        Format:
        First line: ORDER|order_id|customer_name|timestamp|status
        Following lines: ITEM|item_id|name|price|category|quantity
        Separator: END_ORDER
        """
        lines = []

        # Order header line
        timestamp_str = self.order_time.strftime("%Y-%m-%d %H:%M:%S")
        header = f"ORDER|{self.order_id}|{self.customer_name}|{timestamp_str}|{self.status}"
        lines.append(header)

        # Order items
        for item in self.items:
            mi = item.menu_item
            item_line = f"ITEM|{mi.item_id}|{mi.name}|{mi.price}|{mi.category}|{item.quantity}"
            lines.append(item_line)

        # End marker
        lines.append("END_ORDER")

        return "\n".join(lines)

    @staticmethod
    def from_file_format(lines, start_index):
        """
        Create an Order from file format lines.

        Args:
            lines (list): List of strings from the file
            start_index (int): Index where the order starts

        Returns:
            tuple: (Order object, next_index_to_read)
        """
        header = lines[start_index].strip().split("|")
        order_id = header[1]
        customer_name = header[2]
        timestamp_str = header[3]
        status = header[4]

        # Create the order
        order = Order(order_id, customer_name)
        order.status = status

        # Parse timestamp
        try:
            order.order_time = datetime.strptime(timestamp_str, "%Y-%m-%d %H:%M:%S")
        except ValueError:
            order.order_time = datetime.now()

        # Parse items
        index = start_index + 1
        while index < len(lines):
            line = lines[index].strip()

            if line == "END_ORDER":
                break

            if line.startswith("ITEM|"):
                parts = line.split("|")
                item_id = parts[1]
                name = parts[2]
                price = float(parts[3])
                category = parts[4]
                quantity = int(parts[5])

                menu_item = MenuItem(item_id, name, price, category)
                order_item = OrderItem(menu_item, quantity)
                order.items.append(order_item)

            index += 1

        return order, index + 1


class OrderManager:
    """
    Manages all orders for the cafe.

    Handles creating new orders, saving order history,
    and loading orders from files.

    Attributes:
        orders (list): List of all Order objects
        file_path (str): Path to the orders data file
        next_order_id (int): Counter for generating order IDs
    """

    def __init__(self, file_path=None):
        if file_path is None:
            file_path = os.path.join(BASE_DIR, "data", "orders.txt")
        """
        Initialize the OrderManager.

        Args:
            file_path (str): Path to the orders data file
        """
        self.orders = []
        self.file_path = file_path
        self.next_order_id = 1
        self.load_from_file()

    def _generate_order_id(self):
        """
        Generate a new unique order ID.

        Returns:
            str: New order ID in format ORD-001
        """
        order_id = f"ORD-{self.next_order_id:03d}"
        self.next_order_id += 1
        return order_id

    def create_order(self, customer_name="Guest"):
        """
        Create a new empty order.

        Args:
            customer_name (str): Name of the customer

        Returns:
            Order: The newly created order
        """
        order_id = self._generate_order_id()
        new_order = Order(order_id, customer_name)
        self.orders.append(new_order)
        self.save_to_file()
        print(f"[SUCCESS] New order created: #{order_id}")
        return new_order

    def find_order_by_id(self, order_id):
        """
        Find an order by its ID.

        Args:
            order_id (str): Order ID to search for

        Returns:
            Order or None: The found order or None
        """
        for order in self.orders:
            if order.order_id == order_id:
                return order
        return None

    def get_orders_by_status(self, status):
        """
        Get all orders with a specific status.

        Args:
            status (str): Status to filter by

        Returns:
            list: List of matching Order objects
        """
        return [order for order in self.orders if order.status == status]

    def get_orders_by_customer(self, customer_name):
        """
        Get all orders by a specific customer.

        Args:
            customer_name (str): Customer name to search

        Returns:
            list: List of matching Order objects
        """
        return [
            order for order in self.orders
            if order.customer_name.lower() == customer_name.lower()
        ]

    def display_all_orders(self):
        """
        Display a summary of all orders.
        """
        if not self.orders:
            print("\n[INFO] No orders found.")
            return

        print("\n" + "=" * 70)
        print("                    ALL ORDERS")
        print("=" * 70)
        print(f"{'Order ID':<10} {'Customer':<15} {'Items':>6} {'Total':>8} {'Status':<12} {'Date':<20}")
        print("-" * 70)

        for order in self.orders:
            total = order.get_total()
            item_count = order.get_item_count()
            date_str = order.order_time.strftime("%Y-%m-%d %H:%M")
            print(f"{order.order_id:<10} {order.customer_name:<15} {item_count:>6} ${total:>5.2f} {order.status:<12} {date_str:<20}")

        print("=" * 70)

    def cancel_order(self, order_id):
        """
        Cancel an order by setting its status to Cancelled.

        Args:
            order_id (str): ID of the order to cancel

        Returns:
            bool: True if cancelled successfully
        """
        order = self.find_order_by_id(order_id)
        if not order:
            print(f"[ERROR] Order #{order_id} not found.")
            return False

        order.update_status("Cancelled")
        self.save_to_file()
        return True

    # ==================== FILE OPERATIONS ====================

    def save_to_file(self):
        """
        Save all orders to the text file.
        """
        try:
            # Ensure directory exists
            directory = os.path.dirname(self.file_path)
            if directory and not os.path.exists(directory):
                os.makedirs(directory)

            with open(self.file_path, "w") as file:
                for order in self.orders:
                    file.write(order.to_file_format() + "\n")

        except PermissionError:
            print("[ERROR] Permission denied to write orders file.")
        except Exception as e:
            print(f"[ERROR] Could not save orders: {e}")

    def load_from_file(self):
        """
        Load orders from the text file.
        """
        self.orders = []

        if not os.path.exists(self.file_path):
            return

        try:
            with open(self.file_path, "r") as file:
                lines = file.readlines()

            index = 0
            while index < len(lines):
                line = lines[index].strip()

                if line.startswith("ORDER|"):
                    order, index = Order.from_file_format(lines, index)
                    self.orders.append(order)
                else:
                    index += 1

            # Update next_order_id based on existing orders
            if self.orders:
                max_num = 0
                for order in self.orders:
                    try:
                        num = int(order.order_id.split("-")[1])
                        if num > max_num:
                            max_num = num
                    except (IndexError, ValueError):
                        pass
                self.next_order_id = max_num + 1

        except FileNotFoundError:
            pass
        except Exception as e:
            print(f"[ERROR] Could not load orders: {e}")
