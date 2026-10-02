import pandas as pd
import mysql.connector

# 1. Read CSV
df = pd.read_csv("D:/ecommerce-sales-project/data/ecommerce_customer_sales_6000.csv")

# Handle missing values
df["Customer_Age"] = df["Customer_Age"].fillna(df["Customer_Age"].median())
df["Discount"] = df["Discount"].fillna(df["Discount"].median())
df["Payment_Method"] = df["Payment_Method"].fillna(df["Payment_Method"].mode()[0])

# 2. Convert Order_Date
df["Order_Date"] = pd.to_datetime(df["Order_Date"])

# 3. Connect to MySQL
conn = mysql.connector.connect(
    host="localhost",
    user="root",
    password="root",
    database="ecommerce_db"
)

cursor = conn.cursor()

# 4. Insert query
query = """
INSERT INTO ecommerce_sales
(
    Order_ID, Customer_ID, Order_Date, Product_Name, Category,
    Quantity, Unit_Price, Discount, Payment_Method, City,
    State, Customer_Age, Customer_Gender, Revenue, Month, Year
)
VALUES
(
    %s, %s, %s, %s, %s, %s, %s, %s,
    %s, %s, %s, %s, %s, %s, %s, %s
)
"""

# 5. Insert records
for _, row in df.iterrows():

    values = (
        row["Order_ID"],
        row["Customer_ID"],
        row["Order_Date"].date(),
        row["Product_Name"],
        row["Category"],
        int(row["Quantity"]),
        float(row["Unit_Price"]),
        float(row["Discount"]),
        row["Payment_Method"],
        row["City"],
        row["State"],
        int(row["Customer_Age"]),
        row["Customer_Gender"],
        float(row["Revenue"]),
        int(str(row["Month"]).split("-")[-1]),
        int(row["Year"])
    )

    cursor.execute(query, values)

# 6. Save changes
conn.commit()

print("Data inserted successfully!")
print("Total records:", len(df))

cursor.close()
conn.close()