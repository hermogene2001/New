import mysql.connector
import re

# Connect to MySQL database
conn = mysql.connector.connect(
    host="localhost",
    user="root",
    password="",
    database="milk_store"
)
cursor = conn.cursor()

# Create customers table if it doesn't exist
cursor.execute('''
CREATE TABLE IF NOT EXISTS customers (
    id INT AUTO_INCREMENT PRIMARY KEY,
    fname VARCHAR(50) NOT NULL,
    lname VARCHAR(50) NOT NULL,
    email VARCHAR(100) NOT NULL,
    phone VARCHAR(10) NOT NULL,
    pin VARCHAR(6) NOT NULL,
    road_nbr VARCHAR(20),
    UNIQUE (email),
    UNIQUE (phone)
);
''')

# Create orders table if it doesn't exist
cursor.execute('''
CREATE TABLE IF NOT EXISTS orders (
    id INT AUTO_INCREMENT PRIMARY KEY,
    customer_id INT,
    product_id INT,
    quantity INT,
    total_price DECIMAL(10, 2),
    FOREIGN KEY (customer_id) REFERENCES customers(id)
);
''')

def select_product():
    print("Select Product:")
    print("1. Yoghurt")
    print("2. Milk")
    print("3. Cheese")
    choice = input("Enter choice: ")
    product_id = int(choice)

    if product_id == 1:  # Yoghurt
        print("Select Size:")
        print("1. Small")
        print("2. Medium")
        print("3. Large")
        size_choice = input("Enter choice: ")
        if size_choice in ["1", "2", "3"]:
            return product_id, int(size_choice)
        else:
            print("Invalid size choice. Please try again.")
            return select_product()
    elif product_id == 2:  # Milk
        print("Select Size:")
        print("1. 250ml")
        print("2. 1L")
        print("3. 3L")
        print("4. 5L")
        size_choice = input("Enter choice: ")
        if size_choice in ["1", "2", "3", "4"]:
            return product_id, int(size_choice) + 3  # Adjust the size index for Milk
        else:
            print("Invalid size choice. Please try again.")
            return select_product()
    elif product_id == 3:  # Cheese
        print("Select Size:")
        print("1. Small")
        print("2. Medium")
        print("3. Large")
        size_choice = input("Enter choice: ")
        if size_choice in ["1", "2", "3"]:
            return product_id, int(size_choice)
        else:
            print("Invalid size choice. Please try again.")
            return select_product()
    else:
        print("Invalid product choice. Please try again.")
        return select_product()


def enter_quantity():
    while True:
        quantity = input("Enter Quantity: ")
        if quantity.isdigit():
            return int(quantity)
        else:
            print("Invalid quantity. Please enter a valid integer.")


def confirm_order(product, size, quantity, customer_id):
    product_key = {
        1: "Yoghurt",
        2: "Milk",
        3: "Cheese"
    }
    size_key = {
        1: "Small",
        2: "Medium",
        3: "Large",
        4: "250ml",
        5: "1L",
        6: "3L",
        7: "5L"
    }
    
    prices = {
        "Yoghurt": {
            "Small": 500,
            "Medium": 750,
            "Large": 1000
        },
        "Milk": {
            "250ml": 500,
            "1L": 1500,
            "3L": 3000,
            "5L": 8000
        },
        "Cheese": {
            "Small": 1000,
            "Medium": 1500,
            "Large": 2000
        }
    }

    total_price = prices[product_key[product]][size_key[size]] * quantity

    # Display order summary card
    print("\nOrder Summary:")
    print("=================================")
    print(f"Product       : {product_key[product]}")
    print(f"Size          : {size_key[size]}")
    print(f"Quantity      : {quantity}")
    print(f"Total Price   : {total_price}")
    print("=================================\n")
    
    while True:
        confirm = input("Confirm order?\n1. Confirm\n2. Cancel\n3. Modify Quantity: ")
        if confirm == "1":
            cursor.execute("INSERT INTO orders (customer_id, product_id, quantity, total_price) VALUES (%s, %s, %s, %s)", (customer_id, product, quantity, total_price))
            conn.commit()
            print("Order confirmed")
            break
        elif confirm == "2":
            print("Order cancelled")
            break
        elif confirm == "3":
            quantity = enter_quantity()
            total_price = prices[product_key[product]][size_key[size]] * quantity
            
            # Update and display the order summary card again
            print("\nUpdated Order Summary:")
            print("=================================")
            print(f"Product       : {product_key[product]}")
            print(f"Size          : {size_key[size]}")
            print(f"Quantity      : {quantity}")
            print(f"Total Price   : {total_price}")
            print("=================================\n")
        else:
            print("Invalid choice. Please enter 1, 2, or 3.")

def create_account():
    print("Create Account:")
    fname = input("Enter first name: ")
    lname = input("Enter last name: ")
    email = input("Enter email: ")
    roadnbr = input("Enter Road Number: ")
    while True:
        phone = input("Enter phone number (must start with 078 or 079): ")
        if re.match(r"^(078|079)\d{7}$", phone):
            break
        else:
            print("Invalid phone number. Please enter a number starting with 078 or 079.")
    pin = input("Enter PIN: ")
    
    cursor.execute("INSERT INTO customers (fname, lname, email, phone, pin,road_nbr) VALUES (%s, %s, %s, %s, %s, %s)", (fname, lname, email, phone, pin, roadnbr))
    conn.commit()
    print("Account created successfully!")

def login():
    print("Login:")
    phone = input("Enter phone number: ")
    pin = input("Enter PIN: ")
    
    cursor.execute("SELECT id FROM customers WHERE phone = %s AND pin = %s", (phone, pin))
    result = cursor.fetchone()
    if result:
        return result[0]  # Return customer ID
    else:
        print("Invalid phone number or PIN.")
        return None

def main():
    print("Welcome to MUKAMIRA Dairy Ltd")
    ussd_code = input("Enter USSD code: ")
    if ussd_code == "*456#":
        while True:
            print("1. Create Account")
            print("2. Login")
            print("3. Exit")
            choice = input("Enter choice: ")

            if choice == "1":
                create_account()
            elif choice == "2":
                customer_id = login()
                if customer_id:
                    while True:
                        print("1. Place an Order")
                        print("2. Logout")
                        choice = input("Enter choice: ")

                        if choice == "1":
                            product, size = select_product()
                            quantity = enter_quantity()
                            confirm_order(product, size, quantity, customer_id)
                        elif choice == "2":
                            print("Logged out.")
                            break
                        else:
                            print("Invalid choice. Please try again.")
            elif choice == "3":
                print("Thank you for using our service")
                break
            else:
                print("Invalid choice. Please try again.")
    else:
        print("Invalid USSD code.")

if __name__ == "__main__":
    main()

# Close connection
cursor.close()
conn.close()
