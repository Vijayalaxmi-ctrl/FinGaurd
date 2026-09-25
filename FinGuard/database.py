import sqlite3
import os

# Database location
BASE_DIR = os.path.dirname(os.path.abspath(__file__))

DB_PATH = os.path.join(
    BASE_DIR,
    "data",
    "finguard.db"
)


def get_connection():
    """Create and return a database connection."""

    # Create data folder if it doesn't exist
    os.makedirs("data", exist_ok=True)

    return sqlite3.connect(DB_PATH)


def create_tables():
    """Create all required database tables."""

    conn = get_connection()
    cursor = conn.cursor()

    # -----------------------------
    # CUSTOMER TABLE
    # -----------------------------
    cursor.execute("""
        CREATE TABLE IF NOT EXISTS customers (
            customer_id INTEGER PRIMARY KEY,
            name TEXT NOT NULL,
            age INTEGER,
            gender TEXT,
            income REAL,
            account_balance REAL,
            credit_score INTEGER,
            debt_ratio REAL,
            account_age INTEGER,
            city TEXT
        )
    """)

    # -----------------------------
    # TRANSACTION TABLE
    # -----------------------------
    cursor.execute("""
        CREATE TABLE IF NOT EXISTS transactions (
            transaction_id INTEGER PRIMARY KEY,
            customer_id INTEGER,
            amount REAL,
            transaction_type TEXT,
            location TEXT,
            transaction_hour INTEGER,
            transaction_frequency INTEGER,
            is_fraud INTEGER DEFAULT 0,
            anomaly_score REAL DEFAULT 0,
            fraud_probability REAL DEFAULT 0,
            risk_level TEXT DEFAULT 'LOW',

            FOREIGN KEY(customer_id)
            REFERENCES customers(customer_id)
        )
    """)

    # -----------------------------
    # FRAUD ALERT TABLE
    # -----------------------------
    cursor.execute("""
        CREATE TABLE IF NOT EXISTS fraud_alerts (
            alert_id INTEGER PRIMARY KEY AUTOINCREMENT,
            transaction_id INTEGER,
            customer_id INTEGER,
            alert_type TEXT,
            risk_score REAL,
            message TEXT,
            status TEXT DEFAULT 'OPEN',

            FOREIGN KEY(transaction_id)
            REFERENCES transactions(transaction_id),

            FOREIGN KEY(customer_id)
            REFERENCES customers(customer_id)
        )
    """)

    conn.commit()
    conn.close()

    print("Database tables created successfully!")


if __name__ == "__main__":
    create_tables()