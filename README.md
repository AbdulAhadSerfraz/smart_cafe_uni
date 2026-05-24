# Smart Cafe Ordering System

A console-based Cafe Management System built with Python for university Software Engineering lab exam.

## Features

- Customer ordering with interactive menu browsing
- Staff/Admin panel with login system
- Dynamic menu management (Add, Remove, Update, Search)
- Order management with status tracking
- Billing system with discounts and tax calculation
- Loyalty points program
- File-based data persistence
- Input validation and exception handling

## Project Structure

```
smart_cafe/
├── main.py           # Entry point
├── menu_item.py      # MenuItem class
├── menu.py           # Menu CRUD & search
├── order.py          # Order management
├── person.py         # Person > Customer / Staff (inheritance)
├── billing.py        # Invoice & receipt generation
├── auth.py           # Login system
├── utils.py          # Utility functions
├── data/
│   ├── menu.txt      # Menu data
│   ├── orders.txt    # Order history
│   └── users.txt     # User credentials
└── README.md
```

## How to Run

```bash
python smart_cafe/main.py
```

## Login Credentials

| Role   | Username | Password   |
|--------|----------|------------|
| Admin  | admin    | admin123   |
| Staff  | staff1   | staff123   |

## Screenshots

### 1. Welcome Screen (Main Menu)

![Welcome Screen](screenshots/welcome.png)

*Main menu with options: Customer Mode, Staff Mode, View Menu, Track Order, Exit*

---

### 2. Customer Ordering - Selecting Items

![Order Screen 1](screenshots/order1.png)

*Customer browsing menu by category and adding items to order*

---

### 3. Customer Ordering - Order Summary

![Order Screen 2](screenshots/order2.png)

*Order summary showing all items, quantities, and running total before payment*

---

### 4. Bill / Receipt

![Bill Receipt](screenshots/bill.png)

*Final receipt showing items, subtotal, discount, tax, and grand total*

---

### 5. Admin Panel

![Admin Panel](screenshots/admin1.png)

*Staff/Admin panel with Menu Management, Order Management, User Management options*

---

### 6. Menu Display

![Menu Display](screenshots/menu.png)

*Full menu displayed by category (Drinks, Fast Food, Desserts)*

## How to Capture Screenshots

1. Run the program: `python smart_cafe/main.py`
2. Take screenshots using:
   - **Windows:** `Win + Shift + S` (Snipping Tool)
   - **Mac:** `Cmd + Shift + 4`
   - **Linux:** Use GNOME Screenshot or `gnome-screenshot`
3. Save images as `screenshots/welcome.png`, `screenshots/order1.png`, etc.
4. Create the `screenshots/` folder inside `smart_cafe/`

## OOP Concepts Demonstrated

- **Classes & Objects** - MenuItem, Order, Customer, Staff, etc.
- **Inheritance** - Person > Customer, Person > Staff
- **Encapsulation** - Private attributes with getter/setter methods
- **Composition** - Order contains OrderItem objects; SmartCafe contains Menu, OrderManager, AuthSystem
- **Polymorphism** - get_role() overridden in Customer and Staff
