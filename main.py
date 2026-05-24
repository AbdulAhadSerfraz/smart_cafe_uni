"""
Main entry point for Smart Cafe Ordering System.

This is the main program that ties all modules together.
It provides a menu-driven interface for both customers and staff.

Usage:
    python main.py
"""

# Import all modules
from menu_item import MenuItem
from menu import Menu
from order import Order, OrderManager
from person import Person, Customer, Staff
from billing import Invoice
from auth import AuthSystem
from utils import (
    clear_screen,
    print_header,
    print_subheader,
    print_success,
    print_error,
    print_info,
    get_valid_input,
    get_yes_no,
    press_enter_to_continue,
)


class SmartCafe:
    """
    Main application class for the Smart Cafe Ordering System.

    This class ties together the Menu, OrderManager, and AuthSystem
    and provides all user-facing menus and workflows.

    Attributes:
        menu (Menu): The cafe menu manager
        order_manager (OrderManager): Manages all orders
        auth (AuthSystem): Handles user authentication
        current_customer (Customer): Currently active customer
    """

    def __init__(self):
        """
        Initialize the cafe system.
        """
        self.menu = Menu()
        self.order_manager = OrderManager()
        self.auth = AuthSystem()
        self.current_customer = None

    # ==================== MAIN PROGRAM LOOP ====================

    def run(self):
        """
        Start the Smart Cafe application.

        This is the main loop that displays the menu and handles
        user choices until they choose to exit.
        """
        while True:
            clear_screen()
            print_header("WELCOME TO SMART CAFE")
            print("\n1. Customer Mode (Place an Order)")
            print("2. Staff/Admin Mode (Manage System)")
            print("3. View Menu")
            print("4. Track Order Status")
            print("5. Exit")

            choice = input("\nEnter your choice (1-5): ").strip()

            if choice == "1":
                self.customer_mode()
            elif choice == "2":
                self.staff_mode()
            elif choice == "3":
                self.view_menu_only()
            elif choice == "4":
                self.track_order_status()
            elif choice == "5":
                print_header("THANK YOU FOR USING SMART CAFE!")
                print("\nGoodbye! Have a great day!")
                break
            else:
                print_error("Invalid choice. Please enter 1-5.")
                press_enter_to_continue()

    # ==================== CUSTOMER MODE ====================

    def customer_mode(self):
        """
        Customer ordering workflow.

        Handles the complete process from customer registration
        or identification to placing an order and payment.
        """
        clear_screen()
        print_header("CUSTOMER MODE")

        # Step 1: Get customer information
        print("\n--- Customer Information ---")
        name = get_valid_input("Enter your name: ", str)

        # Check if returning customer
        contact = get_valid_input("Enter your phone/email (optional): ", str, allow_empty=True)
        customer_id = f"CUST-{len(self.order_manager.orders) + 1:03d}"

        # Create customer object
        self.current_customer = Customer(name, contact, customer_id)

        # Check if returning customer (if we had a database we'd look them up)
        # For simplicity, check if this name has ordered before
        previous_orders = self.order_manager.get_orders_by_customer(name)
        if previous_orders:
            print(f"\n[INFO] Welcome back, {name}! You've placed {len(previous_orders)} previous orders.")
        else:
            print(f"\n[INFO] Welcome, {name}! This is your first order.")

        press_enter_to_continue()

        # Step 2: Create a new order
        order = self.order_manager.create_order(name)
        self.current_customer.place_order()

        # Step 3: Add items to the order
        self.add_items_to_order(order)

        # Step 4: Process billing
        self.process_payment(order)

        # Step 5: Finalize
        press_enter_to_continue()

    def add_items_to_order(self, order):
        """
        Let the customer add items to their order.

        Args:
            order (Order): The order to add items to
        """
        while True:
            clear_screen()
            print_header("ADD ITEMS TO ORDER")
            print(f"Order: #{order.order_id} | Customer: {order.customer_name}")
            print(f"Current Total: ${order.get_total():.2f}")

            print("\n--- CATEGORIES ---")
            print("1. Drinks")
            print("2. Fast Food")
            print("3. Desserts")
            print("4. Show Full Menu")
            print("5. Done Ordering")

            choice = input("\nChoose a category to browse (1-5): ").strip()

            if choice == "5":
                if order.items:
                    break
                else:
                    print_error("Your order is empty! Please add at least one item.")
                    press_enter_to_continue()
                    continue

            if choice == "4":
                self.menu.display_menu()
            elif choice in ["1", "2", "3"]:
                category_map = {"1": "Drinks", "2": "Fast Food", "3": "Desserts"}
                category = category_map[choice]

                # Display items in this category
                has_items = self.menu.display_by_category(category)
                if not has_items:
                    press_enter_to_continue()
                    continue

                # Let user select an item
                item_id = get_valid_input("\nEnter Item ID to add (or 0 to go back): ", str)

                if item_id == "0":
                    continue

                menu_item = self.menu.find_item_by_id(item_id)
                if not menu_item:
                    print_error(f"Item with ID '{item_id}' not found.")
                    press_enter_to_continue()
                    continue

                # Get quantity
                quantity = get_valid_input(f"Enter quantity for '{menu_item.name}': ", int)
                if quantity <= 0:
                    print_error("Quantity must be at least 1.")
                    press_enter_to_continue()
                    continue

                # Add to order
                order.add_item(menu_item, quantity)
                press_enter_to_continue()
            else:
                print_error("Invalid choice.")
                press_enter_to_continue()

    def process_payment(self, order):
        """
        Handle payment processing for an order.

        Args:
            order (Order): The order to process payment for
        """
        clear_screen()
        print_header("PAYMENT")

        # Display order summary
        order.display_order()

        print("\n--- DISCOUNT OPTIONS ---")

        # Check if customer has loyalty discount
        discount = 0
        if self.current_customer and self.current_customer.has_discount_eligible():
            print(f"[INFO] You have {self.current_customer.loyalty_points} loyalty points!")
            use_discount = get_yes_no(f"Apply {Customer.LOYALTY_DISCOUNT_PERCENT}% loyalty discount?")
            if use_discount:
                discount = self.current_customer.apply_loyalty_discount()

        # Other discount
        if discount == 0:
            print("\n[INFO] No loyalty discount available.")
            special_discount = get_valid_input("Enter special discount % (0 if none): ", float)
            if 0 < special_discount <= 100:
                discount = special_discount

        # Generate invoice
        invoice = Invoice(order, discount)

        # Select payment method
        print("\n--- PAYMENT METHOD ---")
        print("1. Cash")
        print("2. Card")
        print("3. UPI")
        method_choice = get_valid_input("Choose payment method (1-3): ", str)

        method_map = {"1": "Cash", "2": "Card", "3": "UPI"}
        payment_method = method_map.get(method_choice, "Cash")

        invoice.apply_payment(payment_method)

        # Display receipt
        clear_screen()
        receipt = invoice.generate_receipt()
        print(receipt)

        # Add loyalty points
        if self.current_customer:
            self.current_customer.add_loyalty_points(invoice.grand_total)

        # Update order status
        order.update_status("Completed")
        self.order_manager.save_to_file()

        print_success("Payment processed successfully!")

    # ==================== STAFF / ADMIN MODE ====================

    def staff_mode(self):
        """
        Staff/Admin management mode.

        Requires login. Provides access to:
        - Menu management (CRUD)
        - Order management
        - User management (admin only)
        """
        # Require login
        if not self.auth.is_logged_in():
            if not self.handle_login():
                return

        while True:
            clear_screen()
            print_header("STAFF / ADMIN PANEL")
            print(f"Logged in as: {self.auth.get_current_user_name()} ({self.auth.get_current_user_role().upper()})")
            print("=" * 60)

            print("\n1. Menu Management")
            print("2. View All Orders")
            print("3. Update Order Status")
            print("4. Search Orders")
            print("5. Cancel Order")

            # Admin-only options
            if self.auth.is_admin():
                print("\n--- ADMIN OPTIONS ---")
                print("6. User Management")
                print("7. Add Staff User")

            print("\n8. Logout")
            print("9. Back to Main Menu")

            choice = input("\nEnter your choice: ").strip()

            if choice == "1":
                self.menu_management()
            elif choice == "2":
                self.order_manager.display_all_orders()
                press_enter_to_continue()
            elif choice == "3":
                self.update_order_status()
            elif choice == "4":
                self.search_orders()
            elif choice == "5":
                self.cancel_order_flow()
            elif choice == "6" and self.auth.is_admin():
                self.user_management()
            elif choice == "7" and self.auth.is_admin():
                self.register_new_user()
            elif choice == "8":
                self.auth.logout()
                return
            elif choice == "9":
                return
            else:
                print_error("Invalid choice.")
                press_enter_to_continue()

    def handle_login(self):
        """
        Handle user login flow.

        Returns:
            bool: True if login was successful
        """
        clear_screen()
        print_header("STAFF LOGIN")

        print("\n--- Login Required ---")
        username = get_valid_input("Username: ", str)
        password = get_valid_input("Password: ", str)

        success = self.auth.login(username, password)
        press_enter_to_continue()
        return success

    # ==================== MENU MANAGEMENT ====================

    def menu_management(self):
        """
        Menu management interface for staff.
        """
        while True:
            clear_screen()
            print_header("MENU MANAGEMENT")
            print(f"Total items: {self.menu.get_item_count()}")
            print("=" * 60)

            print("\n1. View Full Menu")
            print("2. Add New Item")
            print("3. Remove Item")
            print("4. Update Item Price")
            print("5. Update Item Name")
            print("6. Search Items")
            print("7. Back")

            choice = input("\nEnter your choice: ").strip()

            if choice == "1":
                self.menu.display_menu()
                press_enter_to_continue()
            elif choice == "2":
                self.add_menu_item()
            elif choice == "3":
                self.remove_menu_item()
            elif choice == "4":
                self.update_item_price()
            elif choice == "5":
                self.update_item_name()
            elif choice == "6":
                self.search_menu_items()
            elif choice == "7":
                break
            else:
                print_error("Invalid choice.")
                press_enter_to_continue()

    def add_menu_item(self):
        """
        Add a new item to the menu.
        """
        clear_screen()
        print_header("ADD NEW MENU ITEM")

        item_id = get_valid_input("Enter Item ID (e.g., D001, F001, S001): ", str)
        name = get_valid_input("Enter Item Name: ", str)
        price = get_valid_input("Enter Price ($): ", float)

        # Show categories
        print("\nCategories:")
        for i, cat in enumerate(MenuItem.VALID_CATEGORIES, 1):
            print(f"{i}. {cat}")

        cat_choice = get_valid_input("Choose category (1-3): ", str)
        cat_map = {"1": "Drinks", "2": "Fast Food", "3": "Desserts"}
        category = cat_map.get(cat_choice)

        if not category:
            print_error("Invalid category choice.")
            press_enter_to_continue()
            return

        self.menu.add_item(item_id, name, price, category)
        press_enter_to_continue()

    def remove_menu_item(self):
        """
        Remove an item from the menu.
        """
        clear_screen()
        print_header("REMOVE MENU ITEM")
        self.menu.display_menu()

        item_id = get_valid_input("\nEnter Item ID to remove: ", str)
        self.menu.remove_item(item_id)
        press_enter_to_continue()

    def update_item_price(self):
        """
        Update the price of a menu item.
        """
        clear_screen()
        print_header("UPDATE ITEM PRICE")
        self.menu.display_menu()

        item_id = get_valid_input("\nEnter Item ID to update: ", str)
        new_price = get_valid_input("Enter new price ($): ", float)

        self.menu.update_item_price(item_id, new_price)
        press_enter_to_continue()

    def update_item_name(self):
        """
        Update the name of a menu item.
        """
        clear_screen()
        print_header("UPDATE ITEM NAME")
        self.menu.display_menu()

        item_id = get_valid_input("\nEnter Item ID to update: ", str)
        new_name = get_valid_input("Enter new name: ", str)

        self.menu.update_item_name(item_id, new_name)
        press_enter_to_continue()

    # ==================== SEARCH ====================

    def search_menu_items(self):
        """
        Search menu items by keyword, category, or price range.
        """
        clear_screen()
        print_header("SEARCH MENU")

        print("\nSearch by:")
        print("1. Name Keyword")
        print("2. Category")
        print("3. Price Range")
        print("4. Back")

        choice = input("\nEnter your choice: ").strip()

        if choice == "1":
            keyword = get_valid_input("Enter keyword to search: ", str)
            results = self.menu.search_by_name(keyword)
            self.menu.display_search_results(results)

        elif choice == "2":
            print("\nCategories:")
            for i, cat in enumerate(MenuItem.VALID_CATEGORIES, 1):
                print(f"{i}. {cat}")
            cat_choice = get_valid_input("Choose category (1-3): ", str)
            cat_map = {"1": "Drinks", "2": "Fast Food", "3": "Desserts"}
            category = cat_map.get(cat_choice)
            if category:
                results = self.menu.search_by_category(category)
                self.menu.display_search_results(results)
            else:
                print_error("Invalid category.")

        elif choice == "3":
            min_p = get_valid_input("Enter minimum price: ", float)
            max_p = get_valid_input("Enter maximum price: ", float)
            if min_p <= max_p:
                results = self.menu.search_by_price_range(min_p, max_p)
                self.menu.display_search_results(results)
            else:
                print_error("Min price must be <= max price.")

        else:
            return

        press_enter_to_continue()

    # ==================== ORDER MANAGEMENT ====================

    def update_order_status(self):
        """
        Update the status of an existing order.
        """
        clear_screen()
        print_header("UPDATE ORDER STATUS")

        # Show pending/preparing orders first
        pending = self.order_manager.get_orders_by_status("Pending")
        preparing = self.order_manager.get_orders_by_status("Preparing")

        if pending:
            print("\n--- Pending Orders ---")
            for o in pending:
                print(f"  {o.order_id} - {o.customer_name} (${o.get_total():.2f})")

        if preparing:
            print("\n--- Preparing Orders ---")
            for o in preparing:
                print(f"  {o.order_id} - {o.customer_name} (${o.get_total():.2f})")

        if not pending and not preparing:
            print("\n[INFO] No pending orders.")
            press_enter_to_continue()
            return

        order_id = get_valid_input("\nEnter Order ID to update: ", str)
        order = self.order_manager.find_order_by_id(order_id)

        if not order:
            print_error(f"Order #{order_id} not found.")
            press_enter_to_continue()
            return

        print(f"\nCurrent status: {order.status}")
        print("\nNew status options:")
        for i, status in enumerate(Order.VALID_STATUSES, 1):
            print(f"{i}. {status}")

        status_choice = get_valid_input("Choose new status (1-5): ", str)
        try:
            index = int(status_choice) - 1
            if 0 <= index < len(Order.VALID_STATUSES):
                order.update_status(Order.VALID_STATUSES[index])
                self.order_manager.save_to_file()
            else:
                print_error("Invalid status choice.")
        except ValueError:
            print_error("Invalid input.")

        press_enter_to_continue()

    def search_orders(self):
        """
        Search for orders by customer name or status.
        """
        clear_screen()
        print_header("SEARCH ORDERS")

        print("\nSearch by:")
        print("1. Customer Name")
        print("2. Order Status")
        print("3. View All Orders")

        choice = input("\nEnter your choice: ").strip()

        if choice == "1":
            name = get_valid_input("Enter customer name: ", str)
            results = self.order_manager.get_orders_by_customer(name)
            if results:
                print(f"\n[INFO] Found {len(results)} order(s) for '{name}':")
                for o in results:
                    o.display_order()
            else:
                print(f"[INFO] No orders found for '{name}'.")

        elif choice == "2":
            print("\nStatuses:")
            for i, status in enumerate(Order.VALID_STATUSES, 1):
                print(f"{i}. {status}")
            s_choice = get_valid_input("Choose status (1-5): ", str)
            try:
                index = int(s_choice) - 1
                if 0 <= index < len(Order.VALID_STATUSES):
                    results = self.order_manager.get_orders_by_status(Order.VALID_STATUSES[index])
                    if results:
                        print(f"\n[INFO] Found {len(results)} order(s) with status '{Order.VALID_STATUSES[index]}':")
                        for o in results:
                            o.display_order()
                    else:
                        print(f"[INFO] No orders with status '{Order.VALID_STATUSES[index]}'.")
                else:
                    print_error("Invalid choice.")
            except ValueError:
                print_error("Invalid input.")

        elif choice == "3":
            self.order_manager.display_all_orders()

        press_enter_to_continue()

    def cancel_order_flow(self):
        """
        Cancel an existing order.
        """
        clear_screen()
        print_header("CANCEL ORDER")
        self.order_manager.display_all_orders()

        order_id = get_valid_input("\nEnter Order ID to cancel: ", str)
        confirm = get_yes_no(f"Are you sure you want to cancel order #{order_id}?")
        if confirm:
            self.order_manager.cancel_order(order_id)

        press_enter_to_continue()

    # ==================== USER MANAGEMENT ====================

    def user_management(self):
        """
        View list of registered users.
        """
        clear_screen()
        print_header("USER MANAGEMENT")

        print("\n--- Registered Users ---")
        print(f"{'Username':<15} {'Role':<10} {'Name':<20}")
        print("-" * 45)
        for user in self.auth.users:
            print(f"{user.username:<15} {user.role:<10} {user.name:<20}")

        press_enter_to_continue()

    def register_new_user(self):
        """
        Register a new staff user (admin only).
        """
        clear_screen()
        print_header("REGISTER NEW USER")

        username = get_valid_input("Enter username: ", str)
        password = get_valid_input("Enter password: ", str)
        name = get_valid_input("Enter display name: ", str)

        print("\nRoles:")
        print("1. Admin")
        print("2. Staff")
        role_choice = get_valid_input("Choose role (1-2): ", str)
        role = "admin" if role_choice == "1" else "staff"

        self.auth.register_user(username, password, role, name)
        press_enter_to_continue()

    # ==================== PUBLIC VIEWING ====================

    def view_menu_only(self):
        """
        Display the menu for public viewing without any order flow.
        """
        clear_screen()
        print_header("SMART CAFE - MENU")
        self.menu.display_menu()
        press_enter_to_continue()

    def track_order_status(self):
        """
        Allow a customer to track their order status.
        """
        clear_screen()
        print_header("TRACK ORDER")

        order_id = get_valid_input("Enter your Order ID (e.g., ORD-001): ", str)
        order = self.order_manager.find_order_by_id(order_id)

        if order:
            order.display_order()
        else:
            print_error(f"Order #{order_id} not found.")

        press_enter_to_continue()


# ==================== PROGRAM ENTRY POINT ====================

if __name__ == "__main__":
    """
    Program starts here.

    Creates a SmartCafe instance and runs it.
    """
    cafe = SmartCafe()
    cafe.run()
