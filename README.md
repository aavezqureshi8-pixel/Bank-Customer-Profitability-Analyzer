# 🏦 Bank Customer Profitability Analyzer

## 📌 Project Overview

The Bank Customer Profitability Analyzer is a Business Analytics project designed to analyze customer revenue, costs, profitability, loan performance, customer segments and regional performance.

The project helps identify profitable customer groups and provides business insights that can support data-driven decision making.

> **Note:** The dataset used in this project is simulated/educational data and does not represent real bank customers.

---

## 🎯 Business Problem

Banks serve customers through different accounts, loans and financial products. However, customer revenue and servicing costs can vary significantly.

This project analyzes customer-level financial data to answer questions such as:

- Which customer segments are most profitable?
- Which loan types generate the highest profitability?
- Which regions have higher customer profitability?
- Which customers generate the highest profit?
- How does profitability vary across different customer groups?
- Which customers or segments may require further business analysis?

---

## 📊 Key Performance Indicators

The dashboard analyzes:

- Total Customers
- Total Revenue
- Total Cost
- Total Customer Profit
- Average Profit per Customer
- Average Profit Margin

---

## 🔍 Business Analysis

The project includes analysis of:

### Customer Segments
- Mass
- Affluent
- Premium

### Loan Types
- No Loan
- Auto Loan
- Education Loan
- Personal Loan
- Home Loan

### Account Types
- Savings
- Salary
- Current

### Other Analysis
- Credit Card usage
- Product count
- Region
- Age
- Income
- Occupation
- Profitability Category

---

## 🛠️ Technology Stack

- Python
- Pandas
- MySQL
- SQL
- Streamlit
- Excel
- GitHub

---

## 📈 Dashboard Features

The Streamlit dashboard provides:

- Interactive customer filters
- KPI cards
- Customer segment analysis
- Loan profitability analysis
- Regional profitability analysis
- Profitability category analysis
- Top 10 most profitable customers
- Filtered dataset download

---

## 🗄️ Database

The project uses MySQL for storing and analyzing customer data.

Database:

`bank_profitability`

Main table:

`bank_customers`

The SQL analysis includes queries for:

- Overall KPIs
- Customer segments
- Loan profitability
- Account types
- Credit cards
- Regions
- Profitability categories
- Top customers
- Bottom customers
- Occupations

---

## 📂 Project Files

```text
Bank-Customer-Profitability-Analyzer/
│
├── app.py
├── requirements.txt
├── bank_customer_profitability_analysis.sql
├── bank_customer_profitability_clean.csv
└── README.md
