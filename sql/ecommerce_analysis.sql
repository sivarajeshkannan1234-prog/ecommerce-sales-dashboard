CREATE DATABASE ecommerce_db;
USE ecommerce_db;
CREATE TABLE ecommerce_sales (
    Order_ID VARCHAR(20),
    Customer_ID VARCHAR(20),
    Order_Date DATE,
    Product_Name VARCHAR(100),
    Category VARCHAR(50),
    Quantity INT,
    Unit_Price DECIMAL(10,2),
    Discount DECIMAL(5,2),
    Payment_Method VARCHAR(50),
    City VARCHAR(50),
    State VARCHAR(50),
    Customer_Age INT,
    Customer_Gender VARCHAR(20),
    Revenue DECIMAL(12,2),
    Month INT,
    Year INT
);

SHOW TABLES;

USE ecommerce_db;

SELECT
    COUNT(*) AS total_orders,
    COUNT(DISTINCT Customer_ID) AS total_customers,
    COUNT(DISTINCT Product_Name) AS total_products,
    ROUND(SUM(Revenue), 2) AS total_revenue,
    ROUND(AVG(Revenue), 2) AS average_order_value
FROM ecommerce_sales;


SELECT
    Category,
    COUNT(*) AS total_orders,
    ROUND(SUM(Revenue), 2) AS total_revenue,
    ROUND(AVG(Revenue), 2) AS average_order_value
FROM ecommerce_sales
GROUP BY Category
ORDER BY total_revenue DESC;


SELECT
    Product_Name,
    COUNT(*) AS total_orders,
    SUM(Quantity) AS total_quantity_sold,
    ROUND(SUM(Revenue), 2) AS total_revenue
FROM ecommerce_sales
GROUP BY Product_Name
ORDER BY total_revenue DESC
LIMIT 10;

SELECT
    Year,
    Month,
    ROUND(SUM(Revenue), 2) AS monthly_revenue
FROM ecommerce_sales
GROUP BY Year, Month
ORDER BY Year, Month;

SELECT
    Customer_ID,
    COUNT(*) AS total_orders,
    ROUND(SUM(Revenue), 2) AS total_revenue
FROM ecommerce_sales
GROUP BY Customer_ID
ORDER BY total_revenue DESC
LIMIT 10;

SELECT
    Payment_Method,
    COUNT(*) AS total_orders,
    ROUND(SUM(Revenue), 2) AS total_revenue,
    ROUND(AVG(Revenue), 2) AS average_order_value
FROM ecommerce_sales
GROUP BY Payment_Method
ORDER BY total_revenue DESC;

SELECT
    City,
    COUNT(*) AS total_orders,
    ROUND(SUM(Revenue), 2) AS total_revenue
FROM ecommerce_sales
GROUP BY City
ORDER BY total_revenue DESC
LIMIT 10;

SELECT
    Customer_ID,
    COUNT(*) AS total_orders,
    SUM(Quantity) AS total_quantity,
    ROUND(SUM(Revenue), 2) AS total_revenue,
    ROUND(AVG(Revenue), 2) AS average_order_value
FROM ecommerce_sales
GROUP BY Customer_ID
ORDER BY total_revenue DESC
LIMIT 10;

SELECT
    Customer_ID,
    COUNT(*) AS total_orders,
    ROUND(SUM(Revenue), 2) AS total_revenue
FROM ecommerce_sales
GROUP BY Customer_ID
ORDER BY total_orders DESC, total_revenue DESC
LIMIT 10;

SELECT
    Customer_Gender,
    COUNT(*) AS total_orders,
    ROUND(SUM(Revenue), 2) AS total_revenue,
    ROUND(AVG(Revenue), 2) AS average_order_value
FROM ecommerce_sales
GROUP BY Customer_Gender
ORDER BY total_revenue DESC;

SELECT
    CASE
        WHEN Customer_Age BETWEEN 18 AND 25 THEN '18-25'
        WHEN Customer_Age BETWEEN 26 AND 35 THEN '26-35'
        WHEN Customer_Age BETWEEN 36 AND 45 THEN '36-45'
        WHEN Customer_Age BETWEEN 46 AND 55 THEN '46-55'
        WHEN Customer_Age BETWEEN 56 AND 65 THEN '56-65'
    END AS age_group,
    COUNT(*) AS total_orders,
    ROUND(SUM(Revenue), 2) AS total_revenue,
    ROUND(AVG(Revenue), 2) AS average_order_value
FROM ecommerce_sales
GROUP BY age_group
ORDER BY total_revenue DESC;

SELECT
    Discount,
    COUNT(*) AS total_orders,
    ROUND(SUM(Revenue), 2) AS total_revenue,
    ROUND(AVG(Revenue), 2) AS average_order_value
FROM ecommerce_sales
GROUP BY Discount
ORDER BY Discount;

SELECT
    State,
    COUNT(*) AS total_orders,
    ROUND(SUM(Revenue), 2) AS total_revenue,
    ROUND(AVG(Revenue), 2) AS average_order_value
FROM ecommerce_sales
GROUP BY State
ORDER BY total_revenue DESC;


SELECT
    COUNT(*) AS total_rows,
    SUM(
        ABS(
            Revenue - (Quantity * Unit_Price * (1 - Discount))
        ) > 0.01
    ) AS revenue_mismatches
FROM ecommerce_sales;


UPDATE ecommerce_sales
SET Revenue = ROUND(
    Quantity * Unit_Price * (1 - Discount),
    2
)
WHERE ABS(
    Revenue - (Quantity * Unit_Price * (1 - Discount))
) > 0.01;