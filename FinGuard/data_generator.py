import sqlite3
import random
import os
from datetime import datetime

from database import get_connection, create_tables


# ---------------------------------------------------------
# SAMPLE DATA
# ---------------------------------------------------------

FIRST_NAMES = [
    "Rahul", "Priya", "Aarav", "Ananya", "Rohan",
    "Sneha", "Aditya", "Neha", "Vikram", "Pooja",
    "Karan", "Ishita", "Arjun", "Simran", "Varun",
    "Meera", "Nikhil", "Kavya", "Sahil", "Riya"
]

CITIES = [
    "Mumbai",
    "Pune",
    "Delhi",
    "Bangalore",
    "Hyderabad",
    "Chennai",
    "Kolkata",
    "Ahmedabad"
]

TRANSACTION_TYPES = [
    "UPI",
    "CARD",
    "BANK_TRANSFER",
    "ATM",
    "ONLINE"
]


# ---------------------------------------------------------
# GENERATE CUSTOMERS
# ---------------------------------------------------------

def generate_customers(number_of_customers=500):

    conn = get_connection()
    cursor = conn.cursor()

    # Remove old data
    cursor.execute("DELETE FROM fraud_alerts")
    cursor.execute("DELETE FROM transactions")
    cursor.execute("DELETE FROM customers")

    for customer_id in range(1, number_of_customers + 1):

        name = random.choice(FIRST_NAMES)

        age = random.randint(21, 65)

        gender = random.choice([
            "Male",
            "Female"
        ])

        # Monthly income
        income = random.randint(25000, 250000)

        # Account balance
        account_balance = random.randint(
            10000,
            income * 12
        )

        # Credit score
        credit_score = random.randint(550, 850)

        # Debt ratio
        debt_ratio = round(
            random.uniform(0.05, 0.70),
            2
        )

        # Account age in years
        account_age = random.randint(1, 15)

        city = random.choice(CITIES)

        cursor.execute("""
            INSERT INTO customers (
                customer_id,
                name,
                age,
                gender,
                income,
                account_balance,
                credit_score,
                debt_ratio,
                account_age,
                city
            )
            VALUES (?, ?, ?, ?, ?, ?, ?, ?, ?, ?)
        """, (
            customer_id,
            name,
            age,
            gender,
            income,
            account_balance,
            credit_score,
            debt_ratio,
            account_age,
            city
        ))

    conn.commit()
    conn.close()

    print(f"{number_of_customers} customers generated successfully!")


# ---------------------------------------------------------
# GENERATE TRANSACTIONS
# ---------------------------------------------------------

def generate_transactions(number_of_transactions=5000):

    conn = get_connection()
    cursor = conn.cursor()

    customers = cursor.execute("""
        SELECT
            customer_id,
            account_balance
        FROM customers
    """).fetchall()

    for transaction_id in range(
        1,
        number_of_transactions + 1
    ):

        customer_id, account_balance = random.choice(
            customers
        )

        # Most transactions are normal
        is_suspicious = random.random() < 0.05

        if is_suspicious:

            # Unusually large transaction
            amount = round(
                random.uniform(
                    100000,
                    500000
                ),
                2
            )

            transaction_frequency = random.randint(
                20,
                50
            )

            transaction_hour = random.choice([
                0, 1, 2, 3, 4, 23
            ])

        else:

            # Normal transaction
            amount = round(
                random.uniform(
                    100,
                    25000
                ),
                2
            )

            transaction_frequency = random.randint(
                1,
                15
            )

            transaction_hour = random.randint(
                6,
                22
            )

        transaction_type = random.choice(
            TRANSACTION_TYPES
        )

        location = random.choice(
            CITIES
        )

        cursor.execute("""
            INSERT INTO transactions (
                transaction_id,
                customer_id,
                amount,
                transaction_type,
                location,
                transaction_hour,
                transaction_frequency,
                is_fraud
            )
            VALUES (?, ?, ?, ?, ?, ?, ?, ?)
        """, (
            transaction_id,
            customer_id,
            amount,
            transaction_type,
            location,
            transaction_hour,
            transaction_frequency,
            int(is_suspicious)
        ))

    conn.commit()
    conn.close()

    print(
        f"{number_of_transactions} transactions "
        "generated successfully!"
    )


# ---------------------------------------------------------
# MAIN
# ---------------------------------------------------------

if __name__ == "__main__":

    print("Creating FinGuard database...")

    create_tables()

    print("Generating customer data...")

    generate_customers(500)

    print("Generating transaction data...")

    generate_transactions(5000)

    print()
    print("======================================")
    print("FinGuard dataset generated successfully!")
    print("Customers: 500")
    print("Transactions: 5000")
    print("======================================")