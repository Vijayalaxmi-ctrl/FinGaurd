import sqlite3
import os
import joblib
import pandas as pd

from sklearn.ensemble import IsolationForest

from database import get_connection


# =========================================================
# MODEL LOCATION
# =========================================================

MODEL_PATH = os.path.join(
    "ml",
    "isolation_forest.pkl"
)


# =========================================================
# LOAD TRANSACTION DATA
# =========================================================

def load_transaction_data():

    conn = get_connection()

    query = """
        SELECT
            transaction_id,
            customer_id,
            amount,
            transaction_frequency,
            transaction_hour
        FROM transactions
    """

    df = pd.read_sql_query(
        query,
        conn
    )

    conn.close()

    return df


# =========================================================
# TRAIN MODEL
# =========================================================

def train_model():

    print("Loading transaction data...")

    df = load_transaction_data()

    features = [
        "amount",
        "transaction_frequency",
        "transaction_hour"
    ]

    X = df[features]

    print("Training Isolation Forest...")

    model = IsolationForest(
        n_estimators=150,
        contamination=0.05,
        random_state=42
    )

    model.fit(X)

    # Create ML predictions
    predictions = model.predict(X)

    # Isolation Forest:
    # 1  = normal
    # -1 = anomaly

    df["anomaly_prediction"] = predictions

    # Get anomaly score
    df["anomaly_score"] = model.decision_function(X)

    # Convert prediction to fraud flag
    df["ml_fraud"] = (
        df["anomaly_prediction"] == -1
    ).astype(int)

    # -----------------------------------------------------
    # Convert anomaly score into 0-100 risk probability
    # -----------------------------------------------------

    min_score = df["anomaly_score"].min()
    max_score = df["anomaly_score"].max()

    df["fraud_probability"] = (
        (max_score - df["anomaly_score"])
        /
        (max_score - min_score)
        * 100
    )

    df["fraud_probability"] = (
        df["fraud_probability"]
        .clip(0, 100)
        .round(2)
    )

    # -----------------------------------------------------
    # Risk level
    # -----------------------------------------------------

    df["risk_level"] = df["fraud_probability"].apply(
        lambda x:
            "HIGH" if x >= 70
            else "MEDIUM" if x >= 40
            else "LOW"
    )

    # Save model
    os.makedirs("ml", exist_ok=True)

    joblib.dump(
        model,
        MODEL_PATH
    )

    print()
    print("======================================")
    print("Isolation Forest trained successfully!")
    print("======================================")

    print()
    print(f"Total transactions: {len(df)}")

    print(
        f"Potential anomalies detected: "
        f"{df['ml_fraud'].sum()}"
    )

    print(
        f"Model saved at: {MODEL_PATH}"
    )

    return df


# =========================================================
# UPDATE DATABASE
# =========================================================

def update_transaction_results(df):

    conn = get_connection()
    cursor = conn.cursor()

    for _, row in df.iterrows():

        cursor.execute("""
            UPDATE transactions
            SET
                anomaly_score = ?,
                fraud_probability = ?,
                risk_level = ?
            WHERE transaction_id = ?
        """, (
            float(row["anomaly_score"]),
            float(row["fraud_probability"]),
            row["risk_level"],
            int(row["transaction_id"])
        ))

    conn.commit()
    conn.close()

    print()
    print("Transaction risk results saved to database!")


# =========================================================
# CREATE FRAUD ALERTS
# =========================================================

def create_fraud_alerts(df):

    conn = get_connection()
    cursor = conn.cursor()

    # Clear old alerts
    cursor.execute("""
        DELETE FROM fraud_alerts
    """)

    suspicious = df[
        df["fraud_probability"] >= 70
    ]

    for _, row in suspicious.iterrows():

        message = (
            f"Suspicious transaction of "
            f"₹{row['amount']:,.2f} detected."
        )

        cursor.execute("""
            INSERT INTO fraud_alerts (
                transaction_id,
                customer_id,
                alert_type,
                risk_score,
                message,
                status
            )
            VALUES (?, ?, ?, ?, ?, ?)
        """, (
            int(row["transaction_id"]),
            int(row["customer_id"]),
            "ML_ANOMALY",
            float(row["fraud_probability"]),
            message,
            "OPEN"
        ))

    conn.commit()
    conn.close()

    print(
        f"{len(suspicious)} fraud alerts created!"
    )


# =========================================================
# MAIN
# =========================================================

if __name__ == "__main__":

    print()
    print("======================================")
    print("       FINGUARD FRAUD DETECTION")
    print("======================================")
    print()

    results = train_model()

    update_transaction_results(results)

    create_fraud_alerts(results)

    print()
    print("Fraud detection pipeline completed!")