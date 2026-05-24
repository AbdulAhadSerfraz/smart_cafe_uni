"""
MenuItem class for Smart Cafe Ordering System.

This module defines the MenuItem class which represents
a single item on the cafe menu.
"""


class MenuItem:
    """
    Represents a single menu item in the cafe.

    Attributes:
        item_id (str): Unique identifier for the item
        name (str): Name of the menu item
        price (float): Price of the item
        category (str): Category (Drinks, Fast Food, Desserts)
    """

    # Class-level variable to track all valid categories
    VALID_CATEGORIES = ["Drinks", "Fast Food", "Desserts"]

    def __init__(self, item_id, name, price, category):
        """
        Initialize a new MenuItem.

        Args:
            item_id (str): Unique ID for the item
            name (str): Name of the item
            price (float): Price of the item
            category (str): Category of the item
        """
        self.item_id = item_id
        self.name = name
        self.price = price
        self.category = category

    def __str__(self):
        """
        Return a readable string representation of the item.
        """
        return f"{self.item_id}. {self.name} (${self.price:.2f}) - [{self.category}]"

    def get_details(self):
        """
        Return a dictionary with all item details.
        """
        return {
            "item_id": self.item_id,
            "name": self.name,
            "price": self.price,
            "category": self.category
        }

    def to_file_format(self):
        """
        Convert item to a pipe-delimited string for file saving.

        Format: item_id|name|price|category
        """
        return f"{self.item_id}|{self.name}|{self.price}|{self.category}"

    @staticmethod
    def from_file_format(line):
        """
        Create a MenuItem from a pipe-delimited string.

        Args:
            line (str): Line read from menu file

        Returns:
            MenuItem: A new MenuItem object
        """
        parts = line.strip().split("|")
        if len(parts) == 4:
            item_id = parts[0]
            name = parts[1]
            price = float(parts[2])
            category = parts[3]
            return MenuItem(item_id, name, price, category)
        return None

    @staticmethod
    def is_valid_category(category):
        """
        Check if the given category is valid.

        Args:
            category (str): Category to check

        Returns:
            bool: True if category is valid
        """
        return category in MenuItem.VALID_CATEGORIES
