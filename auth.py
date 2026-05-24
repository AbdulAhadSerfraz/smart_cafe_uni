"""
Authentication module for Smart Cafe Ordering System.

This module handles user login and registration for
staff/admin access to the cafe management features.
"""

import os

# Base directory for data files (resolved relative to this script)
BASE_DIR = os.path.dirname(os.path.abspath(__file__))


class User:
    """
    Represents a system user for authentication.

    Attributes:
        username (str): Login username
        password (str): Login password (stored as plain text for simplicity)
        role (str): User role (admin or staff)
        name (str): Display name of the user
    """

    def __init__(self, username, password, role="staff", name=""):
        """
        Initialize a User.

        Args:
            username (str): Login username
            password (str): Login password
            role (str): User role ('admin' or 'staff')
            name (str): Display name
        """
        self.username = username
        self.password = password
        self.role = role
        self.name = name if name else username

    def to_file_format(self):
        """
        Convert user to pipe-delimited string for file saving.

        Returns:
            str: username|password|role|name
        """
        return f"{self.username}|{self.password}|{self.role}|{self.name}"

    @staticmethod
    def from_file_format(line):
        """
        Create a User from a pipe-delimited string.

        Args:
            line (str): Line from users file

        Returns:
            User or None: A new User object or None
        """
        parts = line.strip().split("|")
        if len(parts) >= 3:
            username = parts[0]
            password = parts[1]
            role = parts[2]
            name = parts[3] if len(parts) > 3 else username
            return User(username, password, role, name)
        return None


class AuthSystem:
    """
    Manages user authentication for the system.

    Handles login, logout, and user registration.

    Attributes:
        users (list): List of User objects
        current_user (User): Currently logged-in user
        file_path (str): Path to the users data file
    """

    def __init__(self, file_path=None):
        if file_path is None:
            file_path = os.path.join(BASE_DIR, "data", "users.txt")
        """
        Initialize the AuthSystem.

        Args:
            file_path (str): Path to the users data file
        """
        self.users = []
        self.current_user = None
        self.file_path = file_path
        self.load_users()

    def load_users(self):
        """
        Load users from the data file.
        """
        self.users = []

        if not os.path.exists(self.file_path):
            # Create default admin user if file doesn't exist
            print("[INFO] No users file found. Creating default admin account.")
            default_admin = User("admin", "admin123", "admin", "Admin")
            self.users.append(default_admin)
            self.save_users()
            return

        try:
            with open(self.file_path, "r") as file:
                for line in file:
                    if line.strip():
                        user = User.from_file_format(line)
                        if user:
                            self.users.append(user)

        except Exception as e:
            print(f"[ERROR] Could not load users: {e}")

    def save_users(self):
        """
        Save all users to the data file.
        """
        try:
            directory = os.path.dirname(self.file_path)
            if directory and not os.path.exists(directory):
                os.makedirs(directory)

            with open(self.file_path, "w") as file:
                for user in self.users:
                    file.write(user.to_file_format() + "\n")

        except Exception as e:
            print(f"[ERROR] Could not save users: {e}")

    def login(self, username, password):
        """
        Attempt to log in a user.

        Args:
            username (str): Username to check
            password (str): Password to check

        Returns:
            bool: True if login was successful
        """
        # Check if already logged in
        if self.current_user:
            print(f"[INFO] Already logged in as '{self.current_user.username}'.")
            return False

        # Find the user
        for user in self.users:
            if user.username == username and user.password == password:
                self.current_user = user
                print(f"\n[SUCCESS] Welcome back, {user.name}!")
                print(f"[INFO] Logged in as '{user.role.upper()}'")
                return True

        print("[ERROR] Invalid username or password.")
        return False

    def logout(self):
        """
        Log out the current user.

        Returns:
            bool: True if logged out successfully
        """
        if self.current_user:
            print(f"[INFO] Goodbye, {self.current_user.name}!")
            self.current_user = None
            return True
        else:
            print("[INFO] No user is currently logged in.")
            return False

    def is_logged_in(self):
        """
        Check if a user is currently logged in.

        Returns:
            bool: True if someone is logged in
        """
        return self.current_user is not None

    def is_admin(self):
        """
        Check if the current user is an admin.

        Returns:
            bool: True if current user is admin
        """
        return self.current_user and self.current_user.role == "admin"

    def register_user(self, username, password, role="staff", name=""):
        """
        Register a new user (admin only).

        Args:
            username (str): New username
            password (str): New password
            role (str): User role ('admin' or 'staff')
            name (str): Display name

        Returns:
            bool: True if registration was successful
        """
        # Check if username already exists
        for user in self.users:
            if user.username == username:
                print(f"[ERROR] Username '{username}' already exists.")
                return False

        # Validate inputs
        if not username.strip():
            print("[ERROR] Username cannot be empty.")
            return False

        if not password.strip():
            print("[ERROR] Password cannot be empty.")
            return False

        if role not in ["admin", "staff"]:
            print("[ERROR] Role must be 'admin' or 'staff'.")
            return False

        # Create and add the new user
        display_name = name if name else username
        new_user = User(username, password, role, display_name)
        self.users.append(new_user)
        self.save_users()
        print(f"[SUCCESS] User '{username}' registered as {role}.")
        return True

    def get_current_user_name(self):
        """
        Get the name of the currently logged-in user.

        Returns:
            str: Current user's name or 'Not logged in'
        """
        if self.current_user:
            return self.current_user.name
        return "Not logged in"

    def get_current_user_role(self):
        """
        Get the role of the currently logged-in user.

        Returns:
            str: Current user's role or 'None'
        """
        if self.current_user:
            return self.current_user.role
        return "None"
