import streamlit as st
import pandas as pd
import mysql.connector
import os

# =========================================================
# PAGE CONFIGURATION
# =========================================================

st.set_page_config(
    page_title="Bank Customer Profitability Analyzer",
    page_icon="🏦",
    layout="wide"
)

# =========================================================
# CURRENCY / NUMBER FORMATTING
# =========================================================

def format_indian_currency(value):
    value = float(value)

    if abs(value) >= 10000000:
        return f"₹{value / 10000000:.2f} Cr"
    elif abs(value) >= 100000:
        return f"₹{value / 100000:.2f} Lakh"
    elif abs(value) >= 1000:
        return f"₹{value / 1000:.1f}K"
    else:
        return f"₹{value:.0f}"


def format_percentage(value):
    return f"{float(value):.2f}%"


# =========================================================
# TITLE
# =========================================================

st.title("🏦 Bank Customer Profitability Analyzer")

st.write(
    "Interactive Business Analytics Dashboard for analyzing "
    "customer profitability, revenue, costs, loans and regions."
)

st.divider()


# =========================================================
# LOAD DATA
# =========================================================

df = None
data_source = ""


# ---------------------------------------------------------
# FIRST: TRY MYSQL
# ---------------------------------------------------------

try:

    mysql_password = ""

    # Get password from Streamlit Secrets if available
    try:
        mysql_password = st.secrets.get("MYSQL_PASSWORD", "")
    except Exception:
        mysql_password = ""

    # Also allow an environment variable
    if not mysql_password:
        mysql_password = os.environ.get("MYSQL_PASSWORD", "")

    if mysql_password:

        conn = mysql.connector.connect(
            host="localhost",
            user="root",
            password=mysql_password,
            database="bank_profitability"
        )

        df = pd.read_sql(
            "SELECT * FROM bank_customers",
            conn
        )

        conn.close()

        data_source = "MySQL"


except Exception:
    df = None


# ---------------------------------------------------------
# SECOND: IF MYSQL IS NOT AVAILABLE, USE CSV
# ---------------------------------------------------------

if df is None:

    try:

        csv_file = "bank_customer_profitability_clean.csv"

        df = pd.read_csv(csv_file)

        data_source = "CSV Dataset"

    except Exception as e:

        st.error("❌ Could not load project data.")

        st.write(
            "Make sure bank_customer_profitability_clean.csv "
            "is present in the project folder."
        )

        st.code(str(e))

        st.stop()


# =========================================================
# DATA SOURCE INFORMATION
# =========================================================

if data_source == "MySQL":

    st.success("✅ Connected to MySQL successfully!")

else:

    st.info(
        "📊 Dashboard is running using the project CSV dataset."
    )


# =========================================================
# SIDEBAR FILTERS
# =========================================================

st.sidebar.header("🔎 Customer Filters")

st.sidebar.write(
    "Use the filters below to analyze different customer groups."
)


# Customer Segment

segment_options = ["All"] + sorted(
    df["Customer_Segment"]
    .dropna()
    .unique()
    .tolist()
)

selected_segment = st.sidebar.selectbox(
    "Customer Segment",
    segment_options
)


# Region

region_options = ["All"] + sorted(
    df["Region"]
    .dropna()
    .unique()
    .tolist()
)

selected_region = st.sidebar.selectbox(
    "Region",
    region_options
)


# Loan Type

loan_options = ["All"] + sorted(
    df["Loan_Type"]
    .dropna()
    .unique()
    .tolist()
)

selected_loan = st.sidebar.selectbox(
    "Loan Type",
    loan_options
)


# Profitability Category

profitability_options = ["All"] + sorted(
    df["Profitability_Category"]
    .dropna()
    .unique()
    .tolist()
)

selected_profitability = st.sidebar.selectbox(
    "Profitability Category",
    profitability_options
)


# =========================================================
# APPLY FILTERS
# =========================================================

filtered_df = df.copy()


if selected_segment != "All":

    filtered_df = filtered_df[
        filtered_df["Customer_Segment"] == selected_segment
    ]


if selected_region != "All":

    filtered_df = filtered_df[
        filtered_df["Region"] == selected_region
    ]


if selected_loan != "All":

    filtered_df = filtered_df[
        filtered_df["Loan_Type"] == selected_loan
    ]


if selected_profitability != "All":

    filtered_df = filtered_df[
        filtered_df["Profitability_Category"]
        == selected_profitability
    ]


# =========================================================
# FILTER STATUS
# =========================================================

st.info(
    f"Showing **{len(filtered_df):,}** customers "
    f"out of **{len(df):,}** total customers."
)


# =========================================================
# KPI CALCULATIONS
# =========================================================

total_customers = len(filtered_df)

total_revenue = filtered_df["Total_Revenue"].sum()

total_cost = filtered_df["Total_Cost"].sum()

total_profit = filtered_df["Customer_Profit"].sum()


if total_customers > 0:

    avg_profit = filtered_df["Customer_Profit"].mean()

    avg_margin = filtered_df["Profit_Margin"].mean()

else:

    avg_profit = 0

    avg_margin = 0


# =========================================================
# KPI DASHBOARD
# =========================================================

st.header("📊 Key Performance Indicators")

col1, col2, col3, col4, col5 = st.columns(5)


col1.metric(
    "👥 Customers",
    f"{total_customers:,}"
)


col2.metric(
    "💰 Revenue",
    format_indian_currency(total_revenue)
)


col3.metric(
    "💸 Cost",
    format_indian_currency(total_cost)
)


col4.metric(
    "📈 Profit",
    format_indian_currency(total_profit)
)


col5.metric(
    "💵 Avg Profit",
    format_indian_currency(avg_profit)
)


st.caption(
    f"Average Profit Margin: {format_percentage(avg_margin)}"
)


st.divider()


# =========================================================
# CUSTOMER SEGMENT ANALYSIS
# =========================================================

st.header("👥 Customer Segment Analysis")

segment = (
    filtered_df
    .groupby("Customer_Segment")
    .agg(
        Customers=("Customer_ID", "count"),
        Total_Revenue=("Total_Revenue", "sum"),
        Total_Cost=("Total_Cost", "sum"),
        Total_Profit=("Customer_Profit", "sum"),
        Avg_Profit=("Customer_Profit", "mean"),
        Avg_Margin=("Profit_Margin", "mean")
    )
    .reset_index()
)


if not segment.empty:

    segment_display = segment.copy()

    segment_display["Total_Revenue"] = (
        segment_display["Total_Revenue"]
        .apply(format_indian_currency)
    )

    segment_display["Total_Cost"] = (
        segment_display["Total_Cost"]
        .apply(format_indian_currency)
    )

    segment_display["Total_Profit"] = (
        segment_display["Total_Profit"]
        .apply(format_indian_currency)
    )

    segment_display["Avg_Profit"] = (
        segment_display["Avg_Profit"]
        .apply(format_indian_currency)
    )

    segment_display["Avg_Margin"] = (
        segment_display["Avg_Margin"]
        .apply(format_percentage)
    )

    st.dataframe(
        segment_display,
        use_container_width=True,
        hide_index=True
    )

    st.subheader("Average Profit by Customer Segment")

    st.bar_chart(
        segment.set_index("Customer_Segment")["Avg_Profit"]
    )


st.divider()


# =========================================================
# LOAN PROFITABILITY ANALYSIS
# =========================================================

st.header("🏦 Loan Profitability Analysis")

loan = (
    filtered_df
    .groupby("Loan_Type")
    .agg(
        Customers=("Customer_ID", "count"),
        Total_Revenue=("Total_Revenue", "sum"),
        Total_Cost=("Total_Cost", "sum"),
        Total_Profit=("Customer_Profit", "sum"),
        Avg_Profit=("Customer_Profit", "mean"),
        Avg_Margin=("Profit_Margin", "mean")
    )
    .reset_index()
)


if not loan.empty:

    loan_display = loan.copy()

    loan_display["Total_Revenue"] = (
        loan_display["Total_Revenue"]
        .apply(format_indian_currency)
    )

    loan_display["Total_Cost"] = (
        loan_display["Total_Cost"]
        .apply(format_indian_currency)
    )

    loan_display["Total_Profit"] = (
        loan_display["Total_Profit"]
        .apply(format_indian_currency)
    )

    loan_display["Avg_Profit"] = (
        loan_display["Avg_Profit"]
        .apply(format_indian_currency)
    )

    loan_display["Avg_Margin"] = (
        loan_display["Avg_Margin"]
        .apply(format_percentage)
    )

    st.dataframe(
        loan_display,
        use_container_width=True,
        hide_index=True
    )

    st.subheader("Average Profit by Loan Type")

    st.bar_chart(
        loan.set_index("Loan_Type")["Avg_Profit"]
    )


st.divider()


# =========================================================
# REGIONAL PROFITABILITY
# =========================================================

st.header("🌍 Regional Profitability")

region = (
    filtered_df
    .groupby("Region")
    .agg(
        Customers=("Customer_ID", "count"),
        Total_Revenue=("Total_Revenue", "sum"),
        Total_Profit=("Customer_Profit", "sum"),
        Avg_Profit=("Customer_Profit", "mean"),
        Avg_Margin=("Profit_Margin", "mean")
    )
    .reset_index()
)


if not region.empty:

    region_display = region.copy()

    region_display["Total_Revenue"] = (
        region_display["Total_Revenue"]
        .apply(format_indian_currency)
    )

    region_display["Total_Profit"] = (
        region_display["Total_Profit"]
        .apply(format_indian_currency)
    )

    region_display["Avg_Profit"] = (
        region_display["Avg_Profit"]
        .apply(format_indian_currency)
    )

    region_display["Avg_Margin"] = (
        region_display["Avg_Margin"]
        .apply(format_percentage)
    )

    st.dataframe(
        region_display,
        use_container_width=True,
        hide_index=True
    )

    st.subheader("Average Profit by Region")

    st.bar_chart(
        region.set_index("Region")["Avg_Profit"]
    )


st.divider()


# =========================================================
# PROFITABILITY CATEGORY
# =========================================================

st.header("📌 Profitability Category Analysis")

profitability = (
    filtered_df
    .groupby("Profitability_Category")
    .agg(
        Customers=("Customer_ID", "count"),
        Total_Profit=("Customer_Profit", "sum"),
        Avg_Profit=("Customer_Profit", "mean")
    )
    .reset_index()
)


if not profitability.empty:

    profitability_display = profitability.copy()

    profitability_display["Total_Profit"] = (
        profitability_display["Total_Profit"]
        .apply(format_indian_currency)
    )

    profitability_display["Avg_Profit"] = (
        profitability_display["Avg_Profit"]
        .apply(format_indian_currency)
    )

    st.dataframe(
        profitability_display,
        use_container_width=True,
        hide_index=True
    )

    st.subheader("Customers by Profitability Category")

    st.bar_chart(
        profitability.set_index(
            "Profitability_Category"
        )["Customers"]
    )


st.divider()


# =========================================================
# TOP 10 MOST PROFITABLE CUSTOMERS
# =========================================================

st.header("🏆 Top 10 Most Profitable Customers")

top_customers = (
    filtered_df
    .sort_values(
        "Customer_Profit",
        ascending=False
    )
    .head(10)
)


if not top_customers.empty:

    top_display = top_customers[
        [
            "Customer_ID",
            "Age",
            "Customer_Segment",
            "Account_Type",
            "Loan_Type",
            "Total_Revenue",
            "Total_Cost",
            "Customer_Profit",
            "Profit_Margin"
        ]
    ].copy()


    top_display["Total_Revenue"] = (
        top_display["Total_Revenue"]
        .apply(format_indian_currency)
    )


    top_display["Total_Cost"] = (
        top_display["Total_Cost"]
        .apply(format_indian_currency)
    )


    top_display["Customer_Profit"] = (
        top_display["Customer_Profit"]
        .apply(format_indian_currency)
    )


    top_display["Profit_Margin"] = (
        top_display["Profit_Margin"]
        .apply(format_percentage)
    )


    st.dataframe(
        top_display,
        use_container_width=True,
        hide_index=True
    )


st.divider()


# =========================================================
# DOWNLOAD FILTERED DATA
# =========================================================

st.header("📥 Download Analysis Data")

csv_data = filtered_df.to_csv(
    index=False
).encode("utf-8")


st.download_button(
    label="⬇️ Download Filtered Customer Data",
    data=csv_data,
    file_name="bank_customer_profitability_filtered.csv",
    mime="text/csv"
)


st.divider()


# =========================================================
# PROJECT INFORMATION
# =========================================================

st.header("ℹ️ About This Project")

st.write(
    """
    **Bank Customer Profitability Analyzer** is a Business Analytics
    project designed to analyze customer revenue, cost, profitability,
    loan performance, customer segments and regional performance.

    The dataset used in this project is simulated/educational data
    and does not represent real bank customers.
    """
)

st.write(
    "**Technology Stack:** Python • Pandas • MySQL • Streamlit • Excel • SQL"
)

st.success(
    "✅ Dashboard analysis completed successfully."
)
