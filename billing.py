"""
Billing module for Smart Cafe Ordering System.

This module handles all billing operations including
generating invoices, applying discounts, and processing payments.
"""

from datetime import datetime


class Invoice:
    """
    Represents a bill/invoice for an order.

    The invoice calculates totals, applies discounts,
    and generates a printable receipt.

    Attributes:
        order (Order): The order being billed
        subtotal (float): Total before any discounts
        discount_percent (float): Discount percentage applied
        discount_amount (float): Amount saved from discount
        tax_percent (float): Tax percentage
        tax_amount (float): Tax amount
        grand_total (float): Final amount to pay
        payment_method (str): How the customer paid
        generated_at (datetime): When the invoice was created
    """

    # Default tax rate
    TAX_PERCENT = 8.0

    def __init__(self, order, discount_percent=0):
        """
        Generate an invoice for the given order.

        Args:
            order (Order): The order to bill
            discount_percent (float): Discount to apply (0-100)
        """
        self.order = order
        self.subtotal = order.get_total()
        self.discount_percent = min(discount_percent, 100)  # Cap at 100%
        self.discount_amount = self.subtotal * (self.discount_percent / 100)
        self.tax_percent = Invoice.TAX_PERCENT

        # Calculate taxable amount (after discount)
        taxable_amount = self.subtotal - self.discount_amount
        self.tax_amount = taxable_amount * (self.tax_percent / 100)
        self.grand_total = taxable_amount + self.tax_amount

        self.payment_method = "Not Paid"
        self.generated_at = datetime.now()

    def apply_payment(self, method):
        """
        Record the payment method used.

        Args:
            method (str): Payment method (Cash, Card, UPI, etc.)
        """
        self.payment_method = method

    def generate_receipt(self):
        """
        Generate and display a full receipt.

        Returns:
            str: The complete receipt text
        """
        receipt = []
        receipt.append("=" * 55)
        receipt.append("         SMART CAFE - OFFICIAL RECEIPT")
        receipt.append("=" * 55)
        receipt.append(f"  Order #: {self.order.order_id}")
        receipt.append(f"  Customer: {self.order.customer_name}")
        receipt.append(f"  Date: {self.generated_at.strftime('%Y-%m-%d %H:%M:%S')}")
        receipt.append("-" * 55)
        receipt.append(f"{'Item':<30} {'Qty':<5} {'Price':>8}")
        receipt.append("-" * 55)

        for item in self.order.items:
            line_price = item.menu_item.price * item.quantity
            receipt.append(f"{item.menu_item.name:<30} {item.quantity:<5} ${line_price:>6.2f}")

        receipt.append("-" * 55)
        receipt.append(f"{'Subtotal:':>45} ${self.subtotal:>6.2f}")

        if self.discount_percent > 0:
            receipt.append(f"{'Discount (' + str(self.discount_percent) + '%):':>45} -${self.discount_amount:>5.2f}")

        receipt.append(f"{'Tax (' + str(self.tax_percent) + '%):':>45} ${self.tax_amount:>6.2f}")
        receipt.append("=" * 55)
        receipt.append(f"{'GRAND TOTAL:':>35} ${self.grand_total:>7.2f}")
        receipt.append("=" * 55)
        receipt.append(f"  Payment: {self.payment_method}")
        receipt.append(f"  Status: PAID")
        receipt.append("=" * 55)
        receipt.append("       Thank you for visiting Smart Cafe!")
        receipt.append("           Have a great day!")
        receipt.append("=" * 55)

        return "\n".join(receipt)

    def display_invoice(self):
        """
        Display the invoice details.
        """
        print("\n" + "=" * 55)
        print("                 INVOICE")
        print("=" * 55)
        print(f"  Order #: {self.order.order_id}")
        print(f"  Customer: {self.order.customer_name}")
        print("-" * 55)
        print(f"  Subtotal:           ${self.subtotal:>7.2f}")

        if self.discount_percent > 0:
            print(f"  Discount ({self.discount_percent}%):    -${self.discount_amount:>7.2f}")

        print(f"  Tax ({self.tax_percent}%):            ${self.tax_amount:>7.2f}")
        print("=" * 55)
        print(f"  GRAND TOTAL:        ${self.grand_total:>7.2f}")
        print("=" * 55)
        print(f"  Payment: {self.payment_method}")
        print("=" * 55)
