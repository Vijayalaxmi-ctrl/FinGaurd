import streamlit as st
import pandas as pd
import plotly.express as px

from analytics import (
    get_dashboard_stats,
    get_risk_distribution,
    get_transaction_type_distribution,
    get_city_distribution,
    get_fraud_alerts,
    get_top_suspicious_transactions,
    get_all_customers,
    get_customer_summary,
    get_all_transactions
)


# =========================================================
# PAGE CONFIGURATION
# =========================================================

st.set_page_config(
    page_title="FinGuard",
    page_icon="🛡️",
    layout="wide"
)


# =========================================================
# CUSTOM CSS
# =========================================================

st.markdown("""
<style>

.main {
    background-color: #f5f7fb;
}

.block-container {
    padding-top: 2rem;
}

.title {
    font-size: 42px;
    font-weight: 700;
}

.subtitle {
    font-size: 18px;
    color: #6b7280;
}

.metric-card {
    background-color: white;
    padding: 20px;
    border-radius: 12px;
    border: 1px solid #e5e7eb;
}

.alert-box {
    padding: 15px;
    border-radius: 10px;
    background-color: #fff3f3;
    border-left: 5px solid #dc2626;
}

</style>
""", unsafe_allow_html=True)


# =========================================================
# SIDEBAR
# =========================================================

st.sidebar.title("🛡️ FinGuard")

st.sidebar.write(
    "AI-Powered Financial Intelligence Platform"
)

st.sidebar.markdown("---")

page = st.sidebar.radio(
    "Navigation",
    [
        "🏠 Dashboard",
        "👤 Customer Analytics",
        "🚨 Fraud Detection",
        "💳 Transactions",
        "📊 Risk Analysis"
    ]
)

st.sidebar.markdown("---")

st.sidebar.info(
    """
    **FinGuard**

    Customer Analytics  
    Risk Assessment  
    AI Fraud Detection  
    Transaction Monitoring
    """
)


# =========================================================
# DASHBOARD
# =========================================================

if page == "🏠 Dashboard":

    st.markdown(
        '<div class="title">🛡️ FinGuard</div>',
        unsafe_allow_html=True
    )

    st.markdown(
        '<div class="subtitle">'
        'AI-Powered Customer Analytics, Risk Assessment '
        'and Fraud Detection Platform'
        '</div>',
        unsafe_allow_html=True
    )

    st.markdown("---")

    # Get statistics
    stats = get_dashboard_stats()

    # -----------------------------------------------------
    # KPI CARDS
    # -----------------------------------------------------

    col1, col2, col3, col4 = st.columns(4)

    with col1:
        st.metric(
            "👥 Customers",
            f"{stats['total_customers']:,}"
        )

    with col2:
        st.metric(
            "💳 Transactions",
            f"{stats['total_transactions']:,}"
        )

    with col3:
        st.metric(
            "⚠️ High Risk",
            f"{stats['high_risk_transactions']:,}"
        )

    with col4:
        st.metric(
            "🚨 Fraud Alerts",
            f"{stats['fraud_alerts']:,}"
        )

    st.markdown("")

    # -----------------------------------------------------
    # TRANSACTION VALUE
    # -----------------------------------------------------

    transaction_value = stats[
        "total_transaction_value"
    ]

    st.metric(
        "💰 Total Transaction Value",
        f"₹{transaction_value:,.2f}"
    )

    st.markdown("---")

    # -----------------------------------------------------
    # CHARTS
    # -----------------------------------------------------

    col1, col2 = st.columns(2)

    # Risk distribution
    with col1:

        st.subheader(
            "📊 Transaction Risk Distribution"
        )

        risk_df = get_risk_distribution()

        if not risk_df.empty:

            fig = px.pie(
                risk_df,
                names="risk_level",
                values="count",
                title="Risk Level Distribution",
                hole=0.4
            )

            st.plotly_chart(
                fig,
                use_container_width=True
            )

    # Transaction type
    with col2:

        st.subheader(
            "💳 Transaction Types"
        )

        type_df = get_transaction_type_distribution()

        if not type_df.empty:

            fig = px.bar(
                type_df,
                x="transaction_type",
                y="count",
                title="Transactions by Type"
            )

            st.plotly_chart(
                fig,
                use_container_width=True
            )

    # -----------------------------------------------------
    # CITY ANALYTICS
    # -----------------------------------------------------

    st.subheader(
        "🌍 Transaction Activity by City"
    )

    city_df = get_city_distribution()

    if not city_df.empty:

        fig = px.bar(
            city_df,
            x="location",
            y="transaction_count",
            title="Transaction Volume by Location"
        )

        st.plotly_chart(
            fig,
            use_container_width=True
        )

    # -----------------------------------------------------
    # TOP SUSPICIOUS TRANSACTIONS
    # -----------------------------------------------------

    st.subheader(
        "🚨 Top Suspicious Transactions"
    )

    suspicious_df = get_top_suspicious_transactions(10)

    if not suspicious_df.empty:

        display_df = suspicious_df[
            [
                "transaction_id",
                "customer_name",
                "amount",
                "transaction_type",
                "location",
                "fraud_probability",
                "risk_level"
            ]
        ].copy()

        display_df["amount"] = display_df[
            "amount"
        ].apply(
            lambda x: f"₹{x:,.2f}"
        )

        st.dataframe(
            display_df,
            use_container_width=True,
            hide_index=True
        )


# =========================================================
# CUSTOMER ANALYTICS
# =========================================================

elif page == "👤 Customer Analytics":

    st.title("👤 Customer Analytics")

    st.write(
        "Analyze customer financial behavior "
        "and transaction patterns."
    )

    st.markdown("---")

    customers = get_all_customers()

    customer_options = {
        f"{row['customer_id']} - {row['name']}":
        row["customer_id"]
        for _, row in customers.iterrows()
    }

    selected_customer = st.selectbox(
        "Select Customer",
        list(customer_options.keys())
    )

    customer_id = customer_options[
        selected_customer
    ]

    customer_df = get_customer_summary(
        customer_id
    )

    if not customer_df.empty:

        customer = customer_df.iloc[0]

        st.subheader(
            f"Customer Profile — {customer['name']}"
        )

        # -------------------------------------------------
        # CUSTOMER INFORMATION
        # -------------------------------------------------

        col1, col2, col3, col4 = st.columns(4)

        with col1:
            st.metric(
                "💰 Income",
                f"₹{customer['income']:,.0f}"
            )

        with col2:
            st.metric(
                "🏦 Balance",
                f"₹{customer['account_balance']:,.0f}"
            )

        with col3:
            st.metric(
                "⭐ Credit Score",
                int(customer['credit_score'])
            )

        with col4:
            st.metric(
                "📅 Account Age",
                f"{customer['account_age']} years"
            )

        st.markdown("---")

        # -------------------------------------------------
        # FINANCIAL INFORMATION
        # -------------------------------------------------

        col1, col2, col3 = st.columns(3)

        with col1:
            st.metric(
                "Total Transactions",
                int(customer[
                    "total_transactions"
                ])
            )

        with col2:
            st.metric(
                "Average Transaction",
                f"₹{customer['average_transaction_amount']:,.2f}"
            )

        with col3:
            st.metric(
                "Largest Transaction",
                f"₹{customer['largest_transaction']:,.2f}"
            )

        st.markdown("---")

        # -------------------------------------------------
        # RISK INFORMATION
        # -------------------------------------------------

        st.subheader("⚠️ Customer Risk Indicators")

        debt_ratio = customer["debt_ratio"]

        if customer["credit_score"] >= 750:
            credit_status = "Good"
        elif customer["credit_score"] >= 650:
            credit_status = "Moderate"
        else:
            credit_status = "Low"

        if debt_ratio <= 0.30:
            debt_status = "Low"
        elif debt_ratio <= 0.50:
            debt_status = "Moderate"
        else:
            debt_status = "High"

        col1, col2, col3 = st.columns(3)

        with col1:
            st.metric(
                "Credit Status",
                credit_status
            )

        with col2:
            st.metric(
                "Debt Ratio",
                f"{debt_ratio * 100:.1f}%"
            )

        with col3:
            st.metric(
                "Debt Risk",
                debt_status
            )

        # -------------------------------------------------
        # CUSTOMER SUMMARY TABLE
        # -------------------------------------------------

        st.markdown("---")

        st.subheader("Customer Details")

        details = pd.DataFrame({
            "Attribute": [
                "Customer ID",
                "Name",
                "Age",
                "Gender",
                "City",
                "Income",
                "Account Balance",
                "Credit Score",
                "Debt Ratio",
                "Account Age"
            ],

            "Value": [
                customer["customer_id"],
                customer["name"],
                customer["age"],
                customer["gender"],
                customer["city"],
                f"₹{customer['income']:,.2f}",
                f"₹{customer['account_balance']:,.2f}",
                customer["credit_score"],
                f"{customer['debt_ratio'] * 100:.1f}%",
                f"{customer['account_age']} years"
            ]
        })

        st.dataframe(
            details,
            use_container_width=True,
            hide_index=True
        )


# =========================================================
# FRAUD DETECTION
# =========================================================

elif page == "🚨 Fraud Detection":

    st.title("🚨 AI Fraud Detection")

    st.write(
        "Machine-learning based anomaly detection "
        "for potentially suspicious transactions."
    )

    st.markdown("---")

    alerts = get_fraud_alerts()

    # -----------------------------------------------------
    # ALERT COUNT
    # -----------------------------------------------------

    col1, col2, col3 = st.columns(3)

    with col1:
        st.metric(
            "🚨 Open Alerts",
            len(alerts)
        )

    with col2:

        if not alerts.empty:
            average_score = alerts[
                "risk_score"
            ].mean()
        else:
            average_score = 0

        st.metric(
            "Average Risk Score",
            f"{average_score:.1f}"
        )

    with col3:

        if not alerts.empty:
            maximum_score = alerts[
                "risk_score"
            ].max()
        else:
            maximum_score = 0

        st.metric(
            "Highest Risk Score",
            f"{maximum_score:.1f}"
        )

    st.markdown("---")

    # -----------------------------------------------------
    # ALERT TABLE
    # -----------------------------------------------------

    st.subheader(
        "🚨 Suspicious Transaction Alerts"
    )

    if not alerts.empty:

        display_alerts = alerts[
            [
                "alert_id",
                "transaction_id",
                "customer_name",
                "amount",
                "location",
                "transaction_type",
                "risk_score",
                "status"
            ]
        ].copy()

        display_alerts["amount"] = (
            display_alerts["amount"]
            .apply(lambda x: f"₹{x:,.2f}")
        )

        display_alerts["risk_score"] = (
            display_alerts["risk_score"]
            .apply(lambda x: f"{x:.1f}%")
        )

        st.dataframe(
            display_alerts,
            use_container_width=True,
            hide_index=True
        )

    else:

        st.success(
            "No suspicious transactions detected."
        )

    # -----------------------------------------------------
    # TOP ALERT
    # -----------------------------------------------------

    if not alerts.empty:

        top_alert = alerts.iloc[0]

        st.markdown("---")

        st.subheader(
            "🔎 Highest Risk Alert"
        )

        st.error(
            f"""
            **Customer:** {top_alert['customer_name']}

            **Transaction:** #{top_alert['transaction_id']}

            **Amount:** ₹{top_alert['amount']:,.2f}

            **Location:** {top_alert['location']}

            **Risk Score:** {top_alert['risk_score']:.2f}%

            **Status:** {top_alert['status']}

            **Reason:** {top_alert['message']}
            """
        )


# =========================================================
# TRANSACTIONS
# =========================================================

elif page == "💳 Transactions":

    st.title("💳 Transaction Monitoring")

    st.write(
        "Explore and filter financial transactions."
    )

    st.markdown("---")

    transactions = get_all_transactions()

    # -----------------------------------------------------
    # FILTERS
    # -----------------------------------------------------

    col1, col2, col3 = st.columns(3)

    with col1:

        risk_filter = st.selectbox(
            "Risk Level",
            [
                "ALL",
                "LOW",
                "MEDIUM",
                "HIGH"
            ]
        )

    with col2:

        type_filter = st.selectbox(
            "Transaction Type",
            [
                "ALL"
            ] +
            sorted(
                transactions[
                    "transaction_type"
                ].unique()
            )
        )

    with col3:

        location_filter = st.selectbox(
            "Location",
            [
                "ALL"
            ] +
            sorted(
                transactions[
                    "location"
                ].unique()
            )
        )

    filtered = transactions.copy()

    if risk_filter != "ALL":

        filtered = filtered[
            filtered["risk_level"]
            == risk_filter
        ]

    if type_filter != "ALL":

        filtered = filtered[
            filtered["transaction_type"]
            == type_filter
        ]

    if location_filter != "ALL":

        filtered = filtered[
            filtered["location"]
            == location_filter
        ]

    st.write(
        f"Showing **{len(filtered):,}** transactions"
    )

    display_transactions = filtered[
        [
            "transaction_id",
            "customer_name",
            "amount",
            "transaction_type",
            "location",
            "transaction_hour",
            "transaction_frequency",
            "fraud_probability",
            "risk_level"
        ]
    ].copy()

    display_transactions["amount"] = (
        display_transactions["amount"]
        .apply(lambda x: f"₹{x:,.2f}")
    )

    display_transactions["fraud_probability"] = (
        display_transactions[
            "fraud_probability"
        ]
        .apply(lambda x: f"{x:.1f}%")
    )

    st.dataframe(
        display_transactions,
        use_container_width=True,
        hide_index=True
    )


# =========================================================
# RISK ANALYSIS
# =========================================================

elif page == "📊 Risk Analysis":

    st.title("📊 Risk Analysis")

    st.write(
        "Analyze transaction risk and identify "
        "high-risk financial activity."
    )

    st.markdown("---")

    risk_df = get_risk_distribution()

    type_df = get_transaction_type_distribution()

    city_df = get_city_distribution()

    # -----------------------------------------------------
    # RISK CHART
    # -----------------------------------------------------

    st.subheader(
        "Transaction Risk Distribution"
    )

    if not risk_df.empty:

        fig = px.bar(
            risk_df,
            x="risk_level",
            y="count",
            title="Number of Transactions by Risk Level"
        )

        st.plotly_chart(
            fig,
            use_container_width=True
        )

    # -----------------------------------------------------
    # TRANSACTION TYPE
    # -----------------------------------------------------

    st.subheader(
        "Transaction Type Analysis"
    )

    if not type_df.empty:

        fig = px.bar(
            type_df,
            x="transaction_type",
            y="total_amount",
            title="Transaction Value by Type"
        )

        st.plotly_chart(
            fig,
            use_container_width=True
        )

    # -----------------------------------------------------
    # CITY
    # -----------------------------------------------------

    st.subheader(
        "Geographical Transaction Analysis"
    )

    if not city_df.empty:

        fig = px.bar(
            city_df,
            x="location",
            y="total_amount",
            title="Transaction Value by Location"
        )

        st.plotly_chart(
            fig,
            use_container_width=True
        )

    # -----------------------------------------------------
    # SUMMARY
    # -----------------------------------------------------

    st.subheader(
        "Risk Summary"
    )

    if not risk_df.empty:

        total = risk_df["count"].sum()

        for _, row in risk_df.iterrows():

            percentage = (
                row["count"] / total
            ) * 100

            st.write(
                f"**{row['risk_level']} Risk:** "
                f"{row['count']} transactions "
                f"({percentage:.2f}%)"
            )

            st.progress(
                float(percentage / 100)
            )