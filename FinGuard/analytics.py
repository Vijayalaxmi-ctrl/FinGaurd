import pandas as pd
from database import get_connection


# =========================================================
# CUSTOMER ANALYTICS
# =========================================================

def get_customer_summary(customer_id):

    conn = get_connection()

    query = """
        SELECT
            c.customer_id,
            c.name,
            c.age,
            c.gender,
            c.income,
            c.account_balance,
            c.credit_score,
            c.debt_ratio,
            c.account_age,
            c.city,

            COUNT(t.transaction_id) AS total_transactions,

            COALESCE(SUM(t.amount), 0)
                AS total_transaction_amount,

            COALESCE(AVG(t.amount), 0)
                AS average_transaction_amount,

            COALESCE(MAX(t.amount), 0)
                AS largest_transaction,

            COALESCE(
                SUM(
                    CASE
                        WHEN t.risk_level = 'HIGH'
                        THEN 1
                        ELSE 0
                    END
                ),
                0
            ) AS high_risk_transactions

        FROM customers c

        LEFT JOIN transactions t
            ON c.customer_id = t.customer_id

        WHERE c.customer_id = ?

        GROUP BY c.customer_id
    """

    df = pd.read_sql_query(
        query,
        conn,
        params=(customer_id,)
    )

    conn.close()

    return df


# =========================================================
# ALL CUSTOMERS
# =========================================================

def get_all_customers():

    conn = get_connection()

    query = """
        SELECT *
        FROM customers
        ORDER BY customer_id
    """

    df = pd.read_sql_query(
        query,
        conn
    )

    conn.close()

    return df


# =========================================================
# ALL TRANSACTIONS
# =========================================================

def get_all_transactions():

    conn = get_connection()

    query = """
        SELECT
            t.*,
            c.name AS customer_name
        FROM transactions t

        LEFT JOIN customers c
            ON t.customer_id = c.customer_id

        ORDER BY t.transaction_id DESC
    """

    df = pd.read_sql_query(
        query,
        conn
    )

    conn.close()

    return df


# =========================================================
# DASHBOARD STATISTICS
# =========================================================

def get_dashboard_stats():

    conn = get_connection()
    cursor = conn.cursor()

    total_customers = cursor.execute("""
        SELECT COUNT(*)
        FROM customers
    """).fetchone()[0]

    total_transactions = cursor.execute("""
        SELECT COUNT(*)
        FROM transactions
    """).fetchone()[0]

    high_risk_transactions = cursor.execute("""
        SELECT COUNT(*)
        FROM transactions
        WHERE risk_level = 'HIGH'
    """).fetchone()[0]

    fraud_alerts = cursor.execute("""
        SELECT COUNT(*)
        FROM fraud_alerts
        WHERE status = 'OPEN'
    """).fetchone()[0]

    total_transaction_value = cursor.execute("""
        SELECT COALESCE(SUM(amount), 0)
        FROM transactions
    """).fetchone()[0]

    conn.close()

    return {
        "total_customers": total_customers,
        "total_transactions": total_transactions,
        "high_risk_transactions": high_risk_transactions,
        "fraud_alerts": fraud_alerts,
        "total_transaction_value": total_transaction_value
    }


# =========================================================
# RISK DISTRIBUTION
# =========================================================

def get_risk_distribution():

    conn = get_connection()

    query = """
        SELECT
            risk_level,
            COUNT(*) AS count
        FROM transactions
        GROUP BY risk_level
    """

    df = pd.read_sql_query(
        query,
        conn
    )

    conn.close()

    return df


# =========================================================
# TRANSACTION TYPE DISTRIBUTION
# =========================================================

def get_transaction_type_distribution():

    conn = get_connection()

    query = """
        SELECT
            transaction_type,
            COUNT(*) AS count,
            SUM(amount) AS total_amount
        FROM transactions
        GROUP BY transaction_type
        ORDER BY count DESC
    """

    df = pd.read_sql_query(
        query,
        conn
    )

    conn.close()

    return df


# =========================================================
# CITY ANALYTICS
# =========================================================

def get_city_distribution():

    conn = get_connection()

    query = """
        SELECT
            location,
            COUNT(*) AS transaction_count,
            SUM(amount) AS total_amount
        FROM transactions
        GROUP BY location
        ORDER BY transaction_count DESC
    """

    df = pd.read_sql_query(
        query,
        conn
    )

    conn.close()

    return df


# =========================================================
# FRAUD ALERTS
# =========================================================

def get_fraud_alerts():

    conn = get_connection()

    query = """
        SELECT
            f.alert_id,
            f.transaction_id,
            f.customer_id,
            c.name AS customer_name,
            t.amount,
            t.location,
            t.transaction_type,
            f.alert_type,
            f.risk_score,
            f.message,
            f.status

        FROM fraud_alerts f

        LEFT JOIN customers c
            ON f.customer_id = c.customer_id

        LEFT JOIN transactions t
            ON f.transaction_id = t.transaction_id

        ORDER BY f.risk_score DESC
    """

    df = pd.read_sql_query(
        query,
        conn
    )

    conn.close()

    return df


# =========================================================
# TOP SUSPICIOUS TRANSACTIONS
# =========================================================

def get_top_suspicious_transactions(limit=10):

    conn = get_connection()

    query = """
        SELECT
            t.transaction_id,
            t.customer_id,
            c.name AS customer_name,
            t.amount,
            t.transaction_type,
            t.location,
            t.transaction_hour,
            t.transaction_frequency,
            t.fraud_probability,
            t.risk_level

        FROM transactions t

        LEFT JOIN customers c
            ON t.customer_id = c.customer_id

        ORDER BY t.fraud_probability DESC

        LIMIT ?
    """

    df = pd.read_sql_query(
        query,
        conn,
        params=(limit,)
    )

    conn.close()

    return df


# =========================================================
# TEST
# =========================================================

if __name__ == "__main__":

    print("Testing FinGuard Analytics...")
    print()

    stats = get_dashboard_stats()

    print("Dashboard Statistics:")
    print(stats)

    print()
    print("Customer 1:")
    print(get_customer_summary(1))

    print()
    print("Top Suspicious Transactions:")
    print(get_top_suspicious_transactions())

    print()
    print("Analytics module working successfully!")