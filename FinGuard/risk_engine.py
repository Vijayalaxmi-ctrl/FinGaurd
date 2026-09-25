import sqlite3
from database import get_connection


# =========================================================
# RISK SCORE CALCULATION
# =========================================================

def calculate_risk_score(
    credit_score,
    debt_ratio,
    account_age,
    income,
    fraud_count=0
):
    """
    Calculate a financial risk score from 0 to 100.

    Higher score = higher financial risk.
    """

    risk_score = 0

    # -----------------------------------------------------
    # 1. CREDIT SCORE
    # -----------------------------------------------------
    if credit_score < 600:
        risk_score += 30
    elif credit_score < 700:
        risk_score += 20
    elif credit_score < 750:
        risk_score += 10
    else:
        risk_score += 5

    # -----------------------------------------------------
    # 2. DEBT RATIO
    # -----------------------------------------------------
    if debt_ratio > 0.60:
        risk_score += 30
    elif debt_ratio > 0.40:
        risk_score += 20
    elif debt_ratio > 0.25:
        risk_score += 10
    else:
        risk_score += 5

    # -----------------------------------------------------
    # 3. ACCOUNT AGE
    # -----------------------------------------------------
    if account_age < 2:
        risk_score += 15
    elif account_age < 5:
        risk_score += 10
    else:
        risk_score += 5

    # -----------------------------------------------------
    # 4. INCOME
    # -----------------------------------------------------
    if income < 30000:
        risk_score += 15
    elif income < 60000:
        risk_score += 10
    else:
        risk_score += 5

    # -----------------------------------------------------
    # 5. PREVIOUS FRAUD
    # -----------------------------------------------------
    if fraud_count >= 3:
        risk_score += 20
    elif fraud_count >= 1:
        risk_score += 10

    # Make sure score stays between 0 and 100
    risk_score = min(risk_score, 100)

    return risk_score


# =========================================================
# RISK LEVEL
# =========================================================

def get_risk_level(risk_score):

    if risk_score <= 30:
        return "LOW"

    elif risk_score <= 60:
        return "MEDIUM"

    else:
        return "HIGH"


# =========================================================
# CALCULATE CUSTOMER RISK
# =========================================================

def calculate_customer_risk(customer_id):

    conn = get_connection()
    cursor = conn.cursor()

    # Get customer information
    customer = cursor.execute("""
        SELECT
            credit_score,
            debt_ratio,
            account_age,
            income
        FROM customers
        WHERE customer_id = ?
    """, (customer_id,)).fetchone()

    if customer is None:
        conn.close()
        return None

    credit_score, debt_ratio, account_age, income = customer

    # Count previous fraud alerts
    fraud_count = cursor.execute("""
        SELECT COUNT(*)
        FROM fraud_alerts
        WHERE customer_id = ?
    """, (customer_id,)).fetchone()[0]

    conn.close()

    # Calculate score
    score = calculate_risk_score(
        credit_score,
        debt_ratio,
        account_age,
        income,
        fraud_count
    )

    level = get_risk_level(score)

    return {
        "customer_id": customer_id,
        "risk_score": score,
        "risk_level": level
    }


# =========================================================
# UPDATE ALL CUSTOMER RISK SCORES
# =========================================================

def calculate_all_customer_risks():

    conn = get_connection()
    cursor = conn.cursor()

    customers = cursor.execute("""
        SELECT customer_id
        FROM customers
    """).fetchall()

    conn.close()

    results = []

    for (customer_id,) in customers:

        result = calculate_customer_risk(customer_id)

        if result:
            results.append(result)

    return results


# =========================================================
# TEST
# =========================================================

if __name__ == "__main__":

    print("Testing FinGuard Risk Engine...")
    print()

    result = calculate_customer_risk(1)

    print("Customer Risk Result:")
    print(result)

    print()
    print("Risk engine working successfully!")