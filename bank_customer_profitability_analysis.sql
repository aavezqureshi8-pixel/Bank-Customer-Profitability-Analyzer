USE bank_profitability;

ALTER TABLE bank_customers
MODIFY Customer_ID VARCHAR(10) NOT NULL;
SELECT COUNT(*) AS Total_Customers
FROM bank_customers;
SELECT
    COUNT(*) AS Total_Customers,
    ROUND(SUM(Total_Revenue), 2) AS Total_Revenue,
    ROUND(SUM(Total_Cost), 2) AS Total_Cost,
    ROUND(SUM(Customer_Profit), 2) AS Total_Profit,
    ROUND(AVG(Customer_Profit), 2) AS Avg_Profit_Per_Customer
FROM bank_customers;
SELECT
    Customer_Segment,
    COUNT(*) AS Customer_Count,
    ROUND(SUM(Customer_Profit), 2) AS Total_Profit,
    ROUND(AVG(Customer_Profit), 2) AS Avg_Profit_Per_Customer,
    ROUND(AVG(Profit_Margin), 2) AS Avg_Profit_Margin
FROM bank_customers
GROUP BY Customer_Segment
ORDER BY Avg_Profit_Per_Customer DESC;
SELECT
    Loan_Type,
    COUNT(*) AS Customer_Count,
    ROUND(SUM(Loan_Revenue), 2) AS Total_Loan_Revenue,
    ROUND(SUM(Customer_Profit), 2) AS Total_Profit,
    ROUND(AVG(Customer_Profit), 2) AS Avg_Profit_Per_Customer
FROM bank_customers
GROUP BY Loan_Type
ORDER BY Avg_Profit_Per_Customer DESC;
SELECT
    Account_Type,
    COUNT(*) AS Customer_Count,
    ROUND(SUM(Customer_Profit), 2) AS Total_Profit,
    ROUND(AVG(Customer_Profit), 2) AS Avg_Profit_Per_Customer,
    ROUND(AVG(Profit_Margin), 2) AS Avg_Profit_Margin
FROM bank_customers
GROUP BY Account_Type
ORDER BY Avg_Profit_Per_Customer DESC;
SELECT
    Credit_Card,
    COUNT(*) AS Customer_Count,
    ROUND(SUM(Customer_Profit), 2) AS Total_Profit,
    ROUND(AVG(Customer_Profit), 2) AS Avg_Profit_Per_Customer,
    ROUND(AVG(Profit_Margin), 2) AS Avg_Profit_Margin
FROM bank_customers
GROUP BY Credit_Card
ORDER BY Avg_Profit_Per_Customer DESC;
SELECT
    Region,
    COUNT(*) AS Customer_Count,
    ROUND(SUM(Customer_Profit), 2) AS Total_Profit,
    ROUND(AVG(Customer_Profit), 2) AS Avg_Profit_Per_Customer,
    ROUND(AVG(Profit_Margin), 2) AS Avg_Profit_Margin
FROM bank_customers
GROUP BY Region
ORDER BY Avg_Profit_Per_Customer DESC;
SELECT
    Profitability_Category,
    COUNT(*) AS Customer_Count,
    ROUND(SUM(Customer_Profit), 2) AS Total_Profit,
    ROUND(AVG(Customer_Profit), 2) AS Avg_Profit_Per_Customer
FROM bank_customers
GROUP BY Profitability_Category
ORDER BY Total_Profit DESC;
SELECT
    Customer_ID,
    Age,
    Customer_Segment,
    Account_Type,
    Loan_Type,
    Total_Revenue,
    Total_Cost,
    Customer_Profit,
    Profit_Margin
FROM bank_customers
ORDER BY Customer_Profit DESC
LIMIT 10;
SELECT
    Customer_ID,
    Age,
    Customer_Segment,
    Account_Type,
    Loan_Type,
    Total_Revenue,
    Total_Cost,
    Customer_Profit,
    Profit_Margin
FROM bank_customers
ORDER BY Customer_Profit ASC
LIMIT 10;
SELECT
    Occupation,
    COUNT(*) AS Customer_Count,
    ROUND(SUM(Customer_Profit), 2) AS Total_Profit,
    ROUND(AVG(Customer_Profit), 2) AS Avg_Profit_Per_Customer
FROM bank_customers
GROUP BY Occupation
ORDER BY Avg_Profit_Per_Customer DESC;
