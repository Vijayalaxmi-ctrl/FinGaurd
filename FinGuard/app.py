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

/* ================================
   GLOBAL
================================ */

.stApp {
    background: #0b0f17;
}

.block-container {
    padding-top: 1.5rem;
    padding-bottom: 2.5rem;
    max-width: 1450px;
}

/* ================================
   SIDEBAR
================================ */

section[data-testid="stSidebar"] {
    background: #111722;
    border-right: 1px solid #273244;
}

section[data-testid="stSidebar"] h1,
section[data-testid="stSidebar"] h2,
section[data-testid="stSidebar"] h3 {
    color: white;
}

.sidebar-brand {
    padding: 10px 5px 20px 5px;
}

.sidebar-brand-title {
    font-size: 25px;
    font-weight: 700;
    color: white;
}

.sidebar-brand-subtitle {
    font-size: 13px;
    color: #8b98aa;
    line-height: 1.5;
    margin-top: 5px;
}

.sidebar-status {
    margin-top: 25px;
    padding: 12px;
    border-radius: 10px;
    background: #162235;
    border: 1px solid #263b57;
}

.sidebar-status-title {
    color: #62a8ff;
    font-weight: 600;
    font-size: 13px;
}

.sidebar-status-text {
    color: #aab7c8;
    font-size: 12px;
    margin-top: 4px;
}

/* ================================
   HEADER
================================ */

.dashboard-title {
    font-size: 42px;
    font-weight: 800;
    color: #ffffff;
    letter-spacing: -1px;
}

.dashboard-subtitle {
    font-size: 15px;
    color: #8c99aa;
    margin-top: -5px;
}

.status-badge {
    display: inline-block;
    padding: 6px 13px;
    border-radius: 20px;
    background: #123522;
    color: #4ade80;
    font-size: 13px;
    font-weight: 600;
    border: 1px solid #1d633c;
}

/* ================================
   KPI CARDS
================================ */

.kpi-card {
    background: #121925;
    border: 1px solid #263244;
    border-radius: 14px;
    padding: 18px 20px;
    min-height: 125px;
    transition: 0.2s;
}

.kpi-card:hover {
    border-color: #3b82f6;
}

.kpi-label {
    color: #8d9aad;
    font-size: 13px;
    font-weight: 500;
}

.kpi-value {
    color: #ffffff;
    font-size: 30px;
    font-weight: 750;
    margin-top: 8px;
}

.kpi-description {
    color: #64748b;
    font-size: 11px;
    margin-top: 5px;
}

/* ================================
   INSIGHT BOX
================================ */

.insight-box {
    background: linear-gradient(
        135deg,
        #111d32,
        #101827
    );

    border: 1px solid #29466c;
    border-radius: 14px;
    padding: 20px 22px;
    margin: 20px 0;
}

.insight-title {
    font-size: 18px;
    font-weight: 700;
    color: white;
}

.insight-text {
    color: #9aa8bb;
    font-size: 13px;
    margin-top: 8px;
}

.insight-number {
    color: #60a5fa;
    font-weight: 700;
}

/* ================================
   TRANSACTION VALUE
================================ */

.value-card {
    background: linear-gradient(135deg, #121d2d, #101722);
    border: 1px solid #29466c;
    border-radius: 14px;
    padding: 18px 22px;
    margin-top: 4px;
}

.value-label {
    color: #8d9aad;
    font-size: 13px;
    font-weight: 600;
}

.value-number {
    color: #ffffff;
    font-size: 32px;
    font-weight: 800;
    margin-top: 6px;
}

.value-description {
    color: #64748b;
    font-size: 11px;
    margin-top: 5px;
}

/* ================================
   SECTION HEADINGS
================================ */

.section-title {
    color: white;
    font-size: 20px;
    font-weight: 700;
    margin-top: 15px;
    margin-bottom: 10px;
}

/* ================================
   TABLE
================================ */

[data-testid="stDataFrame"] {
    border-radius: 12px;
    overflow: hidden;
}

/* ================================
   DIVIDER
================================ */

hr {
    border-color: #273244 !important;
}

/* ================================
   METRIC
================================ */

[data-testid="stMetric"] {
    background: #121925;
    border: 1px solid #263244;
    padding: 15px;
    border-radius: 12px;
}

/* ================================
   MODERN SIDEBAR NAVIGATION
================================ */

.nav-title {
    color: #8b98ad;
    font-size: 0.72rem;
    font-weight: 700;
    letter-spacing: 1.5px;
    margin: 8px 0 10px 2px;
}

header[data-testid="stHeader"] {
    background: #0b0f17 !important;
    border-bottom: 1px solid #1b2535 !important;
}

section[data-testid="stSidebar"] .st-key-nav_dashboard button,
section[data-testid="stSidebar"] .st-key-nav_customers button,
section[data-testid="stSidebar"] .st-key-nav_fraud button,
section[data-testid="stSidebar"] .st-key-nav_investigation button,
section[data-testid="stSidebar"] .st-key-nav_transactions button,
section[data-testid="stSidebar"] .st-key-nav_risk button {
    width: 100% !important;
    min-height: 42px !important;
    height: 42px !important;
    padding: 0 12px !important;
    margin: 2px 0 !important;
    border-radius: 9px !important;
    box-sizing: border-box !important;
    text-align: left !important;
    box-shadow: none !important;
    transition: background 0.15s ease,
                color 0.15s ease,
                border-color 0.15s ease !important;
}

/* Keep icon and label left-aligned */
section[data-testid="stSidebar"] .st-key-nav_dashboard button > div,
section[data-testid="stSidebar"] .st-key-nav_customers button > div,
section[data-testid="stSidebar"] .st-key-nav_fraud button > div,
section[data-testid="stSidebar"] .st-key-nav_investigation button > div,
section[data-testid="stSidebar"] .st-key-nav_transactions button > div,
section[data-testid="stSidebar"] .st-key-nav_risk button > div {
    width: 100% !important;
    justify-content: flex-start !important;
    align-items: center !important;
    text-align: left !important;
}

section[data-testid="stSidebar"] .st-key-nav_dashboard button p,
section[data-testid="stSidebar"] .st-key-nav_customers button p,
section[data-testid="stSidebar"] .st-key-nav_fraud button p,
section[data-testid="stSidebar"] .st-key-nav_investigation button p,
section[data-testid="stSidebar"] .st-key-nav_transactions button p,
section[data-testid="stSidebar"] .st-key-nav_risk button p {
    width: 100% !important;
    margin: 0 !important;
    text-align: left !important;
}

/* Inactive items */
section[data-testid="stSidebar"] .st-key-nav_dashboard button[kind="secondary"],
section[data-testid="stSidebar"] .st-key-nav_customers button[kind="secondary"],
section[data-testid="stSidebar"] .st-key-nav_fraud button[kind="secondary"],
section[data-testid="stSidebar"] .st-key-nav_investigation button[kind="secondary"],
section[data-testid="stSidebar"] .st-key-nav_transactions button[kind="secondary"],
section[data-testid="stSidebar"] .st-key-nav_risk button[kind="secondary"] {
    background: transparent !important;
    border: 1px solid transparent !important;
    color: #aeb8c8 !important;
}

/* Hover without movement */
section[data-testid="stSidebar"] .st-key-nav_dashboard button[kind="secondary"]:hover,
section[data-testid="stSidebar"] .st-key-nav_customers button[kind="secondary"]:hover,
section[data-testid="stSidebar"] .st-key-nav_fraud button[kind="secondary"]:hover,
section[data-testid="stSidebar"] .st-key-nav_investigation button[kind="secondary"]:hover,
section[data-testid="stSidebar"] .st-key-nav_transactions button[kind="secondary"]:hover,
section[data-testid="stSidebar"] .st-key-nav_risk button[kind="secondary"]:hover {
    background: rgba(59, 130, 246, 0.08) !important;
    border-color: rgba(76, 163, 255, 0.10) !important;
    color: #ffffff !important;
    transform: none !important;
}

/* Active item */
section[data-testid="stSidebar"] .st-key-nav_dashboard button[kind="primary"],
section[data-testid="stSidebar"] .st-key-nav_customers button[kind="primary"],
section[data-testid="stSidebar"] .st-key-nav_fraud button[kind="primary"],
section[data-testid="stSidebar"] .st-key-nav_investigation button[kind="primary"],
section[data-testid="stSidebar"] .st-key-nav_transactions button[kind="primary"],
section[data-testid="stSidebar"] .st-key-nav_risk button[kind="primary"] {
    background: rgba(59, 130, 246, 0.14) !important;
    border: 1px solid rgba(76, 163, 255, 0.20) !important;
    border-left: 3px solid #3b9cff !important;
    color: #ffffff !important;
    font-weight: 650 !important;
}

section[data-testid="stSidebar"] button:focus,
section[data-testid="stSidebar"] button:focus-visible {
    outline: none !important;
    box-shadow: none !important;
}

.block-container {
    padding-top: 2.6rem !important;
    padding-bottom: 3rem !important;
}

</style>
""", unsafe_allow_html=True)


# =========================================================
# SIDEBAR
# =========================================================

st.sidebar.markdown("""
<div class="sidebar-brand">

<div class="sidebar-brand-title">
🛡️ FinGuard
</div>

<div class="sidebar-brand-subtitle">
AI-Powered Financial Intelligence
Platform
</div>

</div>
""", unsafe_allow_html=True)

st.sidebar.markdown("---")

# ============================================================
# MODERN SIDEBAR NAVIGATION
# ============================================================

if "page" not in st.session_state:
    st.session_state.page = "🏠 Dashboard"

nav_items = [
    ("🏠 Dashboard", "dashboard"),
    ("👤 Customer Analytics", "customers"),
    ("🚨 Fraud Detection", "fraud"),
    ("🔎 Investigation Center", "investigation"),
    ("💳 Transactions", "transactions"),
    ("📊 Risk Analysis", "risk"),
]

st.sidebar.markdown(
    '<div class="nav-title">NAVIGATION</div>',
    unsafe_allow_html=True
)

for label, key_name in nav_items:

    button_type = (
        "primary"
        if st.session_state.page == label
        else "secondary"
    )

    if st.sidebar.button(
        label,
        key=f"nav_{key_name}",
        type=button_type,
        width="stretch"
    ):
        st.session_state.page = label
        st.rerun()

page = st.session_state.page
st.sidebar.markdown("""
<div class="sidebar-status">

<div class="sidebar-status-title">
● SYSTEM ACTIVE
</div>

<div class="sidebar-status-text">
Database connected<br>
ML model loaded<br>
Fraud monitoring enabled
</div>

</div>
""", unsafe_allow_html=True)


# =========================================================
# DASHBOARD
# =========================================================

if page == "🏠 Dashboard":

    col_title, col_status = st.columns(
        [5, 1]
    )

    with col_title:

        st.markdown(
            '<div class="dashboard-title">'
            '🛡️ FinGuard'
            '</div>',
            unsafe_allow_html=True
        )

        st.markdown(
            '<div class="dashboard-subtitle">'
            'AI-Powered Customer Analytics · '
            'Risk Assessment · Fraud Detection'
            '</div>',
            unsafe_allow_html=True
        )

    with col_status:

        st.markdown(
            '<br><div class="status-badge">'
            '● SYSTEM ACTIVE'
            '</div>',
            unsafe_allow_html=True
        )

    st.markdown("---")

    stats = get_dashboard_stats()

    # -----------------------------------------------------
    # KPI CARDS
    # -----------------------------------------------------

    col1, col2, col3, col4 = st.columns(4)

    with col1:
        st.markdown(f"""
        <div class="kpi-card">
            <div class="kpi-label">👥 TOTAL CUSTOMERS</div>
            <div class="kpi-value">{stats['total_customers']:,}</div>
            <div class="kpi-description">Registered customers</div>
        </div>
        """, unsafe_allow_html=True)

    with col2:
        st.markdown(f"""
        <div class="kpi-card">
            <div class="kpi-label">💳 TRANSACTIONS</div>
            <div class="kpi-value">{stats['total_transactions']:,}</div>
            <div class="kpi-description">Transactions analyzed</div>
        </div>
        """, unsafe_allow_html=True)

    with col3:
        st.markdown(f"""
        <div class="kpi-card">
            <div class="kpi-label">⚠️ HIGH RISK</div>
            <div class="kpi-value">{stats['high_risk_transactions']:,}</div>
            <div class="kpi-description">Require investigation</div>
        </div>
        """, unsafe_allow_html=True)

    with col4:
        st.markdown(f"""
        <div class="kpi-card">
            <div class="kpi-label">🚨 FRAUD ALERTS</div>
            <div class="kpi-value">{stats['fraud_alerts']:,}</div>
            <div class="kpi-description">Alerts generated by system</div>
        </div>
        """, unsafe_allow_html=True)

    # -----------------------------------------------------
    # AI RISK INSIGHTS
    # -----------------------------------------------------

    total_transactions = stats["total_transactions"]
    high_risk = stats["high_risk_transactions"]
    fraud_alerts = stats["fraud_alerts"]
    transaction_value = stats["total_transaction_value"]

    risk_percentage = (
        (high_risk / total_transactions) * 100
        if total_transactions else 0
    )

    st.markdown(f"""
    <div class="insight-box">
        <div class="insight-title">🧠 AI Risk Insights</div>
        <div class="insight-text">
            FinGuard analyzed
            <span class="insight-number">{total_transactions:,}</span>
            transactions across
            <span class="insight-number">{stats['total_customers']:,}</span>
            customers.
            <br><br>
            <span class="insight-number">{risk_percentage:.2f}%</span>
            of transactions are currently classified as high-risk,
            resulting in
            <span class="insight-number">{fraud_alerts:,}</span>
            fraud alerts for further investigation.
        </div>
    </div>
    """, unsafe_allow_html=True)

    # -----------------------------------------------------
    # TRANSACTION VALUE
    # -----------------------------------------------------

    st.markdown(f"""
    <div class="value-card">
        <div class="value-label">💰 TOTAL TRANSACTION VALUE</div>
        <div class="value-number">₹{transaction_value:,.0f}</div>
        <div class="value-description">
            Total monetary value processed by the platform
        </div>
    </div>
    """, unsafe_allow_html=True)

    st.markdown("<br>", unsafe_allow_html=True)

    # -----------------------------------------------------
    # CHARTS
    # -----------------------------------------------------

    col1, col2 = st.columns(2)

    with col1:
        st.markdown(
            '<div class="section-title">📊 Transaction Risk Distribution</div>',
            unsafe_allow_html=True
        )

        risk_df = get_risk_distribution()

        if not risk_df.empty:
            fig = px.pie(
                risk_df,
                names="risk_level",
                values="count",
                title="Risk Level Distribution",
                hole=0.55
            )

            fig.update_layout(
                template="plotly_dark",
                paper_bgcolor="rgba(0,0,0,0)",
                plot_bgcolor="rgba(0,0,0,0)",
                margin=dict(l=10, r=10, t=55, b=10),
                legend_title_text="Risk Level"
            )

            st.plotly_chart(
                fig,
                width="stretch"
            )

    with col2:
        st.markdown(
            '<div class="section-title">💳 Transaction Types</div>',
            unsafe_allow_html=True
        )

        type_df = get_transaction_type_distribution()

        if not type_df.empty:
            fig = px.bar(
                type_df,
                x="transaction_type",
                y="count",
                title="Transactions by Type"
            )

            fig.update_layout(
                template="plotly_dark",
                paper_bgcolor="rgba(0,0,0,0)",
                plot_bgcolor="rgba(0,0,0,0)",
                margin=dict(l=10, r=10, t=55, b=10)
            )

            st.plotly_chart(
                fig,
                width="stretch"
            )

    # -----------------------------------------------------
    # CITY ANALYTICS
    # -----------------------------------------------------

    st.markdown(
        '<div class="section-title">🌍 Transaction Activity by City</div>',
        unsafe_allow_html=True
    )

    city_df = get_city_distribution()

    if not city_df.empty:
        fig = px.bar(
            city_df,
            x="location",
            y="transaction_count",
            title="Transaction Volume by Location"
        )

        fig.update_layout(
            template="plotly_dark",
            paper_bgcolor="rgba(0,0,0,0)",
            plot_bgcolor="rgba(0,0,0,0)",
            margin=dict(l=10, r=10, t=55, b=10)
        )

        st.plotly_chart(
            fig,
            width="stretch"
        )

    # -----------------------------------------------------
    # TOP SUSPICIOUS TRANSACTIONS
    # -----------------------------------------------------

    st.markdown(
        '<div class="section-title">🚨 Top Suspicious Transactions</div>',
        unsafe_allow_html=True
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

        display_df["amount"] = display_df["amount"].apply(
            lambda x: f"₹{x:,.2f}"
        )

        display_df["fraud_probability"] = display_df[
            "fraud_probability"
        ].apply(lambda x: f"{x:.1f}%")

        st.dataframe(
            display_df,
            width="stretch",
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
        str(customer["customer_id"]),
        str(customer["name"]),
        str(customer["age"]),
        str(customer["gender"]),
        str(customer["city"]),
        f"₹{customer['income']:,.2f}",
        f"₹{customer['account_balance']:,.2f}",
        str(customer["credit_score"]),
        f"{customer['debt_ratio'] * 100:.1f}%",
        f"{customer['account_age']} years"
    ]
})

        st.dataframe(
            details,
            width="stretch",
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
            width="stretch",
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
        width="stretch",
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
            width="stretch"
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
            width="stretch"
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
            width="stretch"
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

    # =========================================================
# INVESTIGATION CENTER
# =========================================================

elif page == "🔎 Investigation Center":

    st.title("🔎 Investigation Center")

    st.write(
        "Investigate suspicious transactions using risk scores, "
        "transaction behaviour and customer financial indicators."
    )

    st.markdown("---")

    # -----------------------------------------------------
    # LOAD DATA
    # -----------------------------------------------------

    alerts = get_fraud_alerts()
    transactions = get_all_transactions()

    if alerts.empty:

        st.success(
            "No suspicious transactions are currently available for investigation."
        )

    else:

        # -------------------------------------------------
        # ALERT SELECTION
        # -------------------------------------------------

        st.subheader("🚨 Select Transaction to Investigate")

        alert_options = {
            f"#{row['transaction_id']} — "
            f"{row['customer_name']} — "
            f"Risk: {row['risk_score']:.1f}%":
            row["transaction_id"]
            for _, row in alerts.iterrows()
        }

        selected_alert = st.selectbox(
            "Choose a suspicious transaction",
            list(alert_options.keys())
        )

        selected_transaction_id = alert_options[
            selected_alert
        ]

        # -------------------------------------------------
        # GET SELECTED ALERT
        # -------------------------------------------------

        selected_alert_df = alerts[
            alerts["transaction_id"]
            == selected_transaction_id
        ]

        alert = selected_alert_df.iloc[0]

        # -------------------------------------------------
        # GET TRANSACTION DETAILS
        # -------------------------------------------------

        transaction_matches = transactions[
            transactions["transaction_id"]
            == selected_transaction_id
        ]

        if not transaction_matches.empty:

            transaction = transaction_matches.iloc[0]

        else:

            transaction = None

        # -------------------------------------------------
        # RISK OVERVIEW
        # -------------------------------------------------

        st.subheader("📊 Risk Overview")

        col1, col2, col3, col4 = st.columns(4)

        with col1:

            st.metric(
                "Risk Score",
                f"{float(alert['risk_score']):.1f}%"
            )

        with col2:

            risk_score = float(alert["risk_score"])

            if risk_score >= 75:
                risk_level = "HIGH"
            elif risk_score >= 40:
                risk_level = "MEDIUM"
            else:
                risk_level = "LOW"

            st.metric(
                "Risk Level",
                risk_level
            )

        with col3:

            st.metric(
                "Transaction",
                f"#{selected_transaction_id}"
            )

        with col4:

            st.metric(
                "Status",
                alert["status"]
            )

        st.markdown("---")

        # -------------------------------------------------
        # TRANSACTION INFORMATION
        # -------------------------------------------------

        st.subheader("💳 Transaction Details")

        col1, col2 = st.columns(2)

        with col1:

            st.markdown(
                f"""
                **Transaction ID:** #{selected_transaction_id}

                **Customer:** {alert['customer_name']}

                **Amount:** ₹{float(alert['amount']):,.2f}

                **Transaction Type:** {alert['transaction_type']}
                """
            )

        with col2:

            st.markdown(
                f"""
                **Location:** {alert['location']}

                **Alert Status:** {alert['status']}

                **Risk Score:** {float(alert['risk_score']):.2f}%

                **Alert Reason:** {alert['message']}
                """
            )

        # -------------------------------------------------
        # BEHAVIOUR ANALYSIS
        # -------------------------------------------------

        st.markdown("---")

        st.subheader("🧠 Transaction Behaviour Analysis")

        if transaction is not None:

            behaviour_points = []

            amount = float(transaction["amount"])

            # High transaction amount
            if amount >= 100000:

                behaviour_points.append(
                    "🔴 Transaction amount is very high."
                )

            elif amount >= 50000:

                behaviour_points.append(
                    "🟠 Transaction amount is relatively high."
                )

            else:

                behaviour_points.append(
                    "🟢 Transaction amount is within the generated normal range."
                )

            # Transaction hour
            if "transaction_hour" in transaction.index:

                hour = int(transaction["transaction_hour"])

                if hour < 6 or hour >= 23:

                    behaviour_points.append(
                        f"🔴 Transaction occurred at {hour:02d}:00, "
                        "which falls within the unusual night-time window."
                    )

                else:

                    behaviour_points.append(
                        f"🟢 Transaction occurred at {hour:02d}:00."
                    )

            # Transaction frequency
            if "transaction_frequency" in transaction.index:

                frequency = int(
                    transaction["transaction_frequency"]
                )

                if frequency >= 20:

                    behaviour_points.append(
                        f"🔴 High transaction frequency detected: "
                        f"{frequency}."
                    )

                elif frequency >= 10:

                    behaviour_points.append(
                        f"🟠 Moderate transaction frequency: "
                        f"{frequency}."
                    )

                else:

                    behaviour_points.append(
                        f"🟢 Transaction frequency: {frequency}."
                    )

            for point in behaviour_points:

                st.write(point)

        else:

            st.info(
                "Detailed transaction behaviour data is not available "
                "for this alert."
            )

        # -------------------------------------------------
        # AI RISK EXPLANATION
        # -------------------------------------------------

        st.markdown("---")

        st.subheader("🤖 AI Risk Explanation")

        risk_score = float(alert["risk_score"])

        if risk_score >= 75:

            explanation_title = "🔴 HIGH RISK TRANSACTION"

        elif risk_score >= 40:

            explanation_title = "🟠 MEDIUM RISK TRANSACTION"

        else:

            explanation_title = "🟢 LOW RISK TRANSACTION"

        st.markdown(
            f"""
            <div style="
                background:#111d32;
                border:1px solid #29466c;
                border-radius:14px;
                padding:20px;
                margin-top:10px;
            ">

            <h3 style="color:white;">
            {explanation_title}
            </h3>

            <p style="color:#9aa8bb;">
            FinGuard assigned a risk score of
            <strong style="color:#60a5fa;">
            {risk_score:.1f}%
            </strong>
            to this transaction.
            </p>

            <p style="color:#9aa8bb;">
            The investigation should consider the transaction
            characteristics, customer behaviour and the alert reason
            generated by the risk engine.
            </p>

            </div>
            """,
            unsafe_allow_html=True
        )

        # -------------------------------------------------
        # ALERT REASON
        # -------------------------------------------------

        st.markdown("---")

        st.subheader("⚠️ Why Was This Transaction Flagged?")

        st.warning(
            alert["message"]
        )

        # -------------------------------------------------
        # INVESTIGATION ACTION
        # -------------------------------------------------

        st.markdown("---")

        st.subheader("📋 Investigation Decision")

        decision = st.radio(
            "Select investigation status",
            [
                "Needs Investigation",
                "Under Review",
                "False Positive",
                "Confirmed Suspicious"
            ],
            horizontal=True
        )

        if st.button(
            "💾 Save Investigation Decision",
            width="stretch"
        ):

            st.success(
                f"Investigation status set to: **{decision}**"
            )