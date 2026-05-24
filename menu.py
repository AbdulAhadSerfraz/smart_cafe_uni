"""
Menu management module for Smart Cafe Ordering System.

This module handles all menu-related operations including
loading, saving, displaying, adding, updating, and deleting menu items.
"""

import os
from menu_item import MenuItem

# Base directory for data files (resolved relative to this script)
BASE_DIR = os.path.dirname(os.path.abspath(__file__))


class Menu:
    """
    Manages the cafe menu with CRUD operations.

    The menu is stored in a text file and loaded into memory
    as a list of MenuItem objects.

    Attributes:
        items (list): List of MenuItem objects
        file_path (str): Path to the menu data file
    """

    def __init__(self, file_path=None):
        if file_path is None:
            file_path = os.path.join(BASE_DIR, "data", "menu.txt")
        """
        Initialize the Menu and load items from file.

        Args:
            file_path (str): Path to the menu data file
        """
        self.items = []
        self.file_path = file_path
        self.load_from_file()

    # ==================== FILE OPERATIONS ====================

    def load_from_file(self):
        """
        Load menu items from the text file.

        Each line in the file should be in the format:
        item_id|name|price|category
        """
        self.items = []

        # Check if file exists
        if not os.path.exists(self.file_path):
            print(f"[INFO] Menu file not found. Creating new file at {self.file_path}")
            return

        try:
            with open(self.file_path, "r") as file:
                for line in file:
                    # Skip empty lines
                    if line.strip():
                        item = MenuItem.from_file_format(line)
                        if item:
                            self.items.append(item)

            print(f"[INFO] Loaded {len(self.items)} menu items from file.")

        except FileNotFoundError:
            print(f"[ERROR] Menu file not found at {self.file_path}")
        except PermissionError:
            print(f"[ERROR] Permission denied to read menu file.")
        except Exception as e:
            print(f"[ERROR] Could not load menu: {e}")

    def save_to_file(self):
        """
        Save all menu items to the text file.

        Overwrites the existing file with current menu data.
        """
        try:
            # Ensure the directory exists
            directory = os.path.dirname(self.file_path)
            if directory and not os.path.exists(directory):
                os.makedirs(directory)

            with open(self.file_path, "w") as file:
                for item in self.items:
                    file.write(item.to_file_format() + "\n")

            print(f"[SUCCESS] Saved {len(self.items)} menu items to file.")

        except PermissionError:
            print(f"[ERROR] Permission denied to write menu file.")
        except Exception as e:
            print(f"[ERROR] Could not save menu: {e}")

    # ==================== DISPLAY OPERATIONS ====================

    def display_menu(self):
        """
        Display all menu items grouped by category.
        """
        if not self.items:
            print("\n[INFO] The menu is currently empty.")
            return

        print("\n" + "=" * 60)
        print("              COMPLETE MENU")
        print("=" * 60)

        # Display items grouped by category
        for category in MenuItem.VALID_CATEGORIES:
            # Get items in this category
            category_items = [item for item in self.items if item.category == category]

            if category_items:
                print(f"\n--- {category} ---")
                print("-" * 60)
                print(f"{'ID':<6} {'Name':<25} {'Price':>10}")
                print("-" * 60)

                for item in category_items:
                    print(f"{item.item_id:<6} {item.name:<25} ${item.price:>7.2f}")

        print("=" * 60)

    def display_by_category(self, category):
        """
        Display menu items for a specific category.

        Args:
            category (str): Category to display
        """
        # Get items in this category
        category_items = [item for item in self.items if item.category == category]

        if not category_items:
            print(f"\n[INFO] No items found in '{category}' category.")
            return False

        print(f"\n--- {category} ---")
        print("-" * 50)
        print(f"{'ID':<6} {'Name':<25} {'Price':>10}")
        print("-" * 50)

        for item in category_items:
            print(f"{item.item_id:<6} {item.name:<25} ${item.price:>7.2f}")

        return True

    # ==================== CRUD OPERATIONS ====================

    def add_item(self, item_id, name, price, category):
        """
        Add a new item to the menu.

        Args:
            item_id (str): Unique ID for the item
            name (str): Name of the item
            price (float): Price of the item
            category (str): Category of the item

        Returns:
            bool: True if item was added successfully
        """
        # Check for duplicate ID
        if self.find_item_by_id(item_id):
            print(f"[ERROR] Item with ID '{item_id}' already exists.")
            return False

        # Validate category
        if not MenuItem.is_valid_category(category):
            print(f"[ERROR] Invalid category. Valid categories: {MenuItem.VALID_CATEGORIES}")
            return False

        # Validate price
        if price <= 0:
            print("[ERROR] Price must be greater than zero.")
            return False

        # Create and add the new item
        new_item = MenuItem(item_id, name, price, category)
        self.items.append(new_item)
        self.save_to_file()
        print(f"[SUCCESS] Item '{name}' added to menu.")
        return True

    def remove_item(self, item_id):
        """
        Remove an item from the menu by ID.

        Args:
            item_id (str): ID of the item to remove

        Returns:
            bool: True if item was removed successfully
        """
        item = self.find_item_by_id(item_id)

        if not item:
            print(f"[ERROR] Item with ID '{item_id}' not found.")
            return False

        self.items.remove(item)
        self.save_to_file()
        print(f"[SUCCESS] Item '{item.name}' removed from menu.")
        return True

    def update_item_price(self, item_id, new_price):
        """
        Update the price of an existing menu item.

        Args:
            item_id (str): ID of the item to update
            new_price (float): New price for the item

        Returns:
            bool: True if price was updated successfully
        """
        item = self.find_item_by_id(item_id)

        if not item:
            print(f"[ERROR] Item with ID '{item_id}' not found.")
            return False

        if new_price <= 0:
            print("[ERROR] Price must be greater than zero.")
            return False

        old_price = item.price
        item.price = new_price
        self.save_to_file()
        print(f"[SUCCESS] Price of '{item.name}' updated from ${old_price:.2f} to ${new_price:.2f}.")
        return True

    def update_item_name(self, item_id, new_name):
        """
        Update the name of an existing menu item.

        Args:
            item_id (str): ID of the item to update
            new_name (str): New name for the item

        Returns:
            bool: True if name was updated successfully
        """
        item = self.find_item_by_id(item_id)

        if not item:
            print(f"[ERROR] Item with ID '{item_id}' not found.")
            return False

        if not new_name.strip():
            print("[ERROR] Name cannot be empty.")
            return False

        old_name = item.name
        item.name = new_name
        self.save_to_file()
        print(f"[SUCCESS] Item name changed from '{old_name}' to '{new_name}'.")
        return True

    # ==================== SEARCH OPERATIONS ====================

    def find_item_by_id(self, item_id):
        """
        Find a menu item by its ID.

        Args:
            item_id (str): ID to search for

        Returns:
            MenuItem or None: The found item or None
        """
        for item in self.items:
            if item.item_id == item_id:
                return item
        return None

    def search_by_name(self, keyword):
        """
        Search for menu items by name (case-insensitive).

        Args:
            keyword (str): Search keyword

        Returns:
            list: List of matching MenuItem objects
        """
        keyword = keyword.lower()
        results = [item for item in self.items if keyword in item.name.lower()]
        return results

    def search_by_category(self, category):
        """
        Get all menu items in a specific category.

        Args:
            category (str): Category to filter by

        Returns:
            list: List of MenuItem objects in that category
        """
        return [item for item in self.items if item.category == category]

    def search_by_price_range(self, min_price, max_price):
        """
        Search for items within a price range.

        Args:
            min_price (float): Minimum price
            max_price (float): Maximum price

        Returns:
            list: List of matching MenuItem objects
        """
        results = [
            item for item in self.items
            if min_price <= item.price <= max_price
        ]
        return results

    def display_search_results(self, results):
        """
        Display search results in a formatted table.

        Args:
            results (list): List of MenuItem objects to display
        """
        if not results:
            print("\n[INFO] No items found matching your search.")
            return

        print("\n" + "-" * 50)
        print(f"Search Results: {len(results)} item(s) found")
        print("-" * 50)
        print(f"{'ID':<6} {'Name':<25} {'Price':>10} {'Category':>15}")
        print("-" * 50)

        for item in results:
            print(f"{item.item_id:<6} {item.name:<25} ${item.price:>7.2f} {item.category:>15}")

        print("-" * 50)

    # ==================== UTILITY ====================

    def get_item_count(self):
        """
        Get the total number of items in the menu.

        Returns:
            int: Number of items
        """
        return len(self.items)

    def get_all_items(self):
        """
        Get a copy of all menu items.

        Returns:
            list: Copy of the items list
        """
        return self.items.copy()
