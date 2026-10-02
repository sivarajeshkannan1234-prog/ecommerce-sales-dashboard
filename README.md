# E-Commerce Sales Data Analytics Project

## 📊 Project Overview

This project analyzes an e-commerce sales dataset containing **6,000 customer orders**. It demonstrates a complete beginner-to-intermediate data analytics workflow using **Python, MySQL, SQL, and Power BI**.

The project covers:

- Data loading and basic preprocessing with Python
- Missing-value handling
- Date conversion
- MySQL database creation and data insertion
- SQL-based business analysis
- Revenue and sales validation
- Customer, product, category, payment, city, and state analysis
- Power BI dashboard visualization

## 🛠️ Technologies Used

| Technology | Purpose |
|---|---|
| Python | Data loading and preprocessing |
| Pandas | Data manipulation |
| MySQL | Database storage and SQL analysis |
| SQL | Business queries and validation |
| Power BI | Interactive dashboard |
| Jupyter Notebook | Python analysis and experimentation |
| Git & GitHub | Version control and project sharing |

## 📁 Project Structure

```text
ecommerce-sales-project/
│
├── data/
│   └── ecommerce_customer_sales_6000.csv
│
├── python/
│   ├── load_data.py
│   └── python_coding.ipynb
│
├── sql/
│   └── ecommerce_analysis.sql
│
├── power bi/
│   └── dashboard.pbix
│
├── .gitignore
├── requirements.txt
└── README.md
```

## 📌 Dataset

The dataset contains e-commerce order information such as:

- Order ID
- Customer ID
- Order Date
- Product Name
- Category
- Quantity
- Unit Price
- Discount
- Payment Method
- City
- State
- Customer Age
- Customer Gender
- Revenue
- Month
- Year

## 🔍 Key Business Questions

The SQL analysis answers questions such as:

1. What is the total revenue?
2. How many orders and customers are there?
3. Which product categories generate the most revenue?
4. Which products have the highest sales?
5. How does revenue change month by month?
6. Which customers generate the highest revenue?
7. Which payment methods are most commonly used?
8. Which cities and states generate the most revenue?
9. How does revenue vary by gender and age group?
10. Are there any revenue calculation mismatches?

## 🚀 How to Run the Project

### 1. Install Python

Install Python 3.x and verify:

```bash
python --version
```

### 2. Create a virtual environment

Open PowerShell inside the project folder:

```powershell
python -m venv .venv
```

Activate it:

```powershell
.\.venv\Scripts\Activate.ps1
```

If PowerShell blocks activation, you can use:

```powershell
Set-ExecutionPolicy -Scope Process -ExecutionPolicy Bypass
```

Then activate again:

```powershell
.\.venv\Scripts\Activate.ps1
```

### 3. Install Python packages

```powershell
pip install -r requirements.txt
```

### 4. Set up MySQL

Open MySQL Workbench or the MySQL command line.

Run:

```sql
SOURCE sql/ecommerce_analysis.sql;
```

Or open `sql/ecommerce_analysis.sql` in MySQL Workbench and execute it.

This creates:

```text
Database: ecommerce_db
Table: ecommerce_sales
```

### 5. Configure database credentials

For security, do not store your real MySQL password in GitHub.

Set these environment variables before running the Python script:

```powershell
$env:MYSQL_HOST="localhost"
$env:MYSQL_USER="root"
$env:MYSQL_PASSWORD="YOUR_MYSQL_PASSWORD"
$env:MYSQL_DATABASE="ecommerce_db"
```

Example:

```powershell
$env:MYSQL_HOST="localhost"
$env:MYSQL_USER="root"
$env:MYSQL_PASSWORD="root"
$env:MYSQL_DATABASE="ecommerce_db"
```

> The example password above is only a local-development example. Never commit a real password to GitHub.

### 6. Run the Python data loader

From the project root:

```powershell
python .\python\load_data.py
```

Expected result:

```text
Data inserted successfully!
Total records: 6000
```

### 7. Run SQL analysis

Open:

```text
sql/ecommerce_analysis.sql
```

Execute the required SELECT statements in MySQL Workbench.

### 8. Open the Power BI dashboard

Open:

```text
power bi/dashboard.pbix
```

If the dashboard is connected to your local MySQL database, update the data-source credentials when Power BI asks for them.

## 📈 Dashboard

The Power BI dashboard can be used to present:

- Total Revenue
- Total Orders
- Total Customers
- Product and Category Performance
- Monthly Revenue
- Payment Method Analysis
- State/City Performance
- Customer Demographics

## 🔐 Security

This project follows a basic GitHub-safe approach:

- Do not commit passwords.
- Do not commit API keys.
- Do not commit `.env` files.
- Do not commit virtual environments.
- Keep credentials in environment variables or local configuration.

## 📦 GitHub Upload

After checking the project locally, initialize Git from the project root:

```powershell
git init
```

Check the files:

```powershell
git status
```

Add the files:

```powershell
git add .
```

Create the first commit:

```powershell
git commit -m "Initial commit: e-commerce sales analytics project"
```

Rename the branch to `main`:

```powershell
git branch -M main
```

Create a new empty repository on GitHub, then connect it:

```powershell
git remote add origin https://github.com/YOUR-USERNAME/ecommerce-sales-analytics.git
```

Verify the remote:

```powershell
git remote -v
```

Push the project:

```powershell
git push -u origin main
```

## 🔄 Future Project Changes

Whenever you modify the project:

```powershell
git status
git add .
git commit -m "Describe the change"
git push
```

Example:

```powershell
git add .
git commit -m "Update SQL analysis queries"
git push
```

## 👨‍💻 Author

**Siva R**

Data Analytics / Python / SQL / Power BI

## ⭐ Project Goal

The goal of this project is to demonstrate practical skills in:

**Data Cleaning → Database Management → SQL Analysis → Business Insights → Power BI Visualization → GitHub Version Control**
