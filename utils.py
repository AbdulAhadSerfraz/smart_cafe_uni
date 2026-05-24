"""
Utility functions for Smart Cafe Ordering System.

This module contains helper functions used across the project.
"""

import os


def clear_screen():
    """
    Clear the terminal screen.

    Works on both Windows and Unix-like systems.
    """
    # For Windows
    if os.name == "nt":
        os.system("cls")
    # For Mac and Linux
    else:
        os.system("clear")


def print_header(title):
    """
    Print a formatted header with a title.

    Args:
        title (str): Title to display in the header
    """
    print("=" * 60)
    print(f"{title:^60}")
    print("=" * 60)


def print_subheader(text):
    """
    Print a formatted sub-header line.

    Args:
        text (str): Text to display
    """
    print("-" * 60)
    print(f"  {text}")
    print("-" * 60)


def print_success(message):
    """
    Print a success message in green color.

    Args:
        message (str): Success message
    """
    print(f"[SUCCESS] {message}")


def print_error(message):
    """
    Print an error message in red color.

    Args:
        message (str): Error message
    """
    print(f"[ERROR] {message}")


def print_info(message):
    """
    Print an informational message.

    Args:
        message (str): Info message
    """
    print(f"[INFO] {message}")


def get_valid_input(prompt, input_type=str, allow_empty=False):
    """
    Get user input and validate it.

    Args:
        prompt (str): Prompt message for the user
        input_type (type): Expected type (str, float, int)
        allow_empty (bool): Whether empty input is allowed

    Returns:
        The validated input in the expected type
    """
    while True:
        try:
            user_input = input(prompt).strip()

            # Check for empty input
            if not user_input and not allow_empty:
                print_error("Input cannot be empty. Please try again.")
                continue

            # Convert to the desired type
            if input_type == float:
                return float(user_input)
            elif input_type == int:
                return int(user_input)
            else:
                return user_input

        except ValueError:
            print_error(f"Invalid input. Please enter a valid {input_type.__name__}.")


def get_yes_no(prompt):
    """
    Get a yes/no answer from the user.

    Args:
        prompt (str): Prompt message

    Returns:
        bool: True for yes, False for no
    """
    while True:
        answer = input(prompt + " (y/n): ").strip().lower()
        if answer in ["y", "yes"]:
            return True
        elif answer in ["n", "no"]:
            return False
        else:
            print_error("Please enter 'y' or 'n'.")


def press_enter_to_continue():
    """
    Wait for the user to press Enter before continuing.
    """
    input("\nPress Enter to continue...")
