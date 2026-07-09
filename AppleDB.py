import sqlite3

conn = sqlite3.connect("AppleDB.db")
cursor = conn.cursor()

cursor.execute("""
CREATE TABLE IF NOT EXISTS sales_transactions (
    transaction_id INTEGER PRIMARY KEY AUTOINCREMENT,
    transaction_date TEXT,
    customer_name TEXT,
    product_name TEXT,
    category TEXT,
    quantity INTEGER,
    unit_price REAL,
    total_amount REAL,
    payment_method TEXT,
    city TEXT,
    country TEXT
)
""")

data = [
    (
        "2026-07-09",
        "Avinash",
        "MacBook Pro",
        "Electronics",
        1,
        1999.99,
        1999.99,
        "UPI",
        "Hyderabad",
        "India"
    )
]

cursor.executemany("""
INSERT INTO sales_transactions (
    transaction_date,
    customer_name,
    product_name,
    category,
    quantity,
    unit_price,
    total_amount,
    payment_method,
    city,
    country
)
VALUES (?, ?, ?, ?, ?, ?, ?, ?, ?, ?)
""", data)

conn.commit()
conn.close()

print("AppleDB.db created successfully")