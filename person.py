"""
Person, Customer, and Staff classes for Smart Cafe Ordering System.

This module demonstrates inheritance and encapsulation.
The Person class is the base class, with Customer and Staff
as derived classes.
"""


class Person:
    """
    Base class representing a person in the system.

    This class uses encapsulation with name and contact_info
    attributes. It serves as the parent for Customer and Staff.

    Attributes:
        name (str): Person's name
        contact_info (str): Person's contact information
    """

    def __init__(self, name, contact_info=""):
        """
        Initialize a Person.

        Args:
            name (str): Person's name
            contact_info (str): Contact info (phone, email, etc.)
        """
        self.name = name
        self.contact_info = contact_info

    def introduce(self):
        """
        Introduce the person with their basic info.

        Returns:
            str: Introduction string
        """
        return f"Hello! My name is {self.name}."

    def get_role(self):
        """
        Get the role of this person.

        Returns:
            str: Role description
        """
        return "Person"

    def __str__(self):
        """
        Return string representation.
        """
        return f"{self.name} ({self.get_role()})"


class Customer(Person):
    """
    Represents a cafe customer.

    Inherits from Person and adds customer-specific
    attributes like loyalty points and order history.

    Attributes:
        loyalty_points (int): Points earned from orders
        orders_count (int): Number of orders placed
    """

    # Discount thresholds for loyalty points
    LOYALTY_DISCOUNT_THRESHOLD = 100  # Points needed for discount
    LOYALTY_DISCOUNT_PERCENT = 10     # Discount percentage

    def __init__(self, name, contact_info="", customer_id=""):
        """
        Initialize a Customer.

        Args:
            name (str): Customer's name
            contact_info (str): Contact information
            customer_id (str): Unique customer ID
        """
        # Call parent constructor
        super().__init__(name, contact_info)

        self.customer_id = customer_id
        self.loyalty_points = 0
        self.orders_count = 0

    def get_role(self):
        """
        Override parent method to return 'Customer'.
        """
        return "Customer"

    def add_loyalty_points(self, amount_spent):
        """
        Add loyalty points based on amount spent.

        1 point for every $1 spent.

        Args:
            amount_spent (float): Amount the customer spent
        """
        points_earned = int(amount_spent)
        self.loyalty_points += points_earned
        print(f"[INFO] {self.name} earned {points_earned} loyalty points!")
        print(f"[INFO] Total loyalty points: {self.loyalty_points}")

    def has_discount_eligible(self):
        """
        Check if customer is eligible for a loyalty discount.

        Returns:
            bool: True if eligible for discount
        """
        return self.loyalty_points >= Customer.LOYALTY_DISCOUNT_THRESHOLD

    def apply_loyalty_discount(self):
        """
        Apply the loyalty discount if eligible.

        Deducts the threshold points from the customer's balance.

        Returns:
            float: Discount percentage (0 if not eligible)
        """
        if self.has_discount_eligible():
            self.loyalty_points -= Customer.LOYALTY_DISCOUNT_THRESHOLD
            print(f"[SUCCESS] Loyalty discount of {Customer.LOYALTY_DISCOUNT_PERCENT}% applied!")
            print(f"[INFO] Remaining loyalty points: {self.loyalty_points}")
            return Customer.LOYALTY_DISCOUNT_PERCENT
        else:
            points_needed = Customer.LOYALTY_DISCOUNT_THRESHOLD - self.loyalty_points
            print(f"[INFO] Need {points_needed} more points for a discount.")
            return 0

    def place_order(self):
        """
        Record that the customer placed an order.
        """
        self.orders_count += 1

    def customer_summary(self):
        """
        Get a summary of the customer's activity.

        Returns:
            str: Summary text
        """
        return (
            f"Customer: {self.name}\n"
            f"  ID: {self.customer_id}\n"
            f"  Contact: {self.contact_info}\n"
            f"  Orders: {self.orders_count}\n"
            f"  Loyalty Points: {self.loyalty_points}"
        )


class Staff(Person):
    """
    Represents a staff member or admin.

    Inherits from Person and adds staff-specific
    attributes like employee ID, position, and salary.

    Attributes:
        employee_id (str): Unique employee identifier
        position (str): Job position (e.g., Admin, Cashier, Chef)
        salary (float): Employee salary
    """

    def __init__(self, name, contact_info="", employee_id="", position="Staff", salary=0):
        """
        Initialize a Staff member.

        Args:
            name (str): Staff member's name
            contact_info (str): Contact information
            employee_id (str): Unique employee ID
            position (str): Job position
            salary (float): Salary amount
        """
        # Call parent constructor
        super().__init__(name, contact_info)

        self.employee_id = employee_id
        self.position = position
        self.salary = salary

    def get_role(self):
        """
        Override parent method to return the staff's position.
        """
        return f"Staff ({self.position})"

    def update_position(self, new_position):
        """
        Update the staff member's position.

        Args:
            new_position (str): New position title
        """
        old_position = self.position
        self.position = new_position
        print(f"[SUCCESS] {self.name}'s position changed from '{old_position}' to '{new_position}'.")

    def update_salary(self, new_salary):
        """
        Update the staff member's salary.

        Args:
            new_salary (float): New salary amount
        """
        if new_salary <= 0:
            print("[ERROR] Salary must be positive.")
            return

        old_salary = self.salary
        self.salary = new_salary
        print(f"[SUCCESS] {self.name}'s salary changed from ${old_salary:.2f} to ${new_salary:.2f}.")

    def staff_summary(self):
        """
        Get a summary of the staff member.

        Returns:
            str: Summary text
        """
        return (
            f"Staff: {self.name}\n"
            f"  Employee ID: {self.employee_id}\n"
            f"  Position: {self.position}\n"
            f"  Contact: {self.contact_info}\n"
            f"  Salary: ${self.salary:.2f}"
        )
