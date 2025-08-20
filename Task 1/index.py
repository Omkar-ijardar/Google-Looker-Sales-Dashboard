import sqlite3
import pandas as pd
import matplotlib.pyplot as plt

conn = sqlite3.connect('sales_data.db')
cursor = conn.cursor()

cursor.executescript("""
CREATE TABLE IF NOT EXISTS customer_detail (
    customer_id TEXT,
    registered_date TEXT
);

CREATE TABLE IF NOT EXISTS sku_detail (
    sku_id TEXT,
    sku_name TEXT,
    mrp REAL,
    discounted_price INTEGER,
    category TEXT
);

CREATE TABLE IF NOT EXISTS payment_detail (
    payment_mode_id INTEGER,
    payment_mode TEXT
);

CREATE TABLE IF NOT EXISTS order_detail (
    order_id TEXT,
    customer_id TEXT,
    order_date TEXT,
    sku_id TEXT,
    price INTEGER,
    qty_ordered INTEGER,
    total_price INTEGER,
    discount INTEGER,
    before_discount INTEGER,
    is_valid INTEGER,
    is_net INTEGER,
    is_gross INTEGER,
    payment_mode_id INTEGER
);
""")
with open('order_detail_cleaned.sql', 'r', encoding='utf-8') as f:
    cursor.executescript(f.read())

with open('customer_detail.txt', 'r', encoding='utf-8') as f:
    cursor.executescript(f.read())

with open('sku_detail.txt', 'r', encoding='utf-8') as f:
    cursor.executescript(f.read())

with open('payment_detail.txt', 'r', encoding='utf-8') as f:
    cursor.executescript(f.read())

conn.commit()



query = """
SELECT 
    s.sku_name,
    SUM(o.qty_ordered) AS total_qty
FROM 
    order_detail o
JOIN 
    sku_detail s ON o.sku_id = s.sku_id
WHERE 
    s.category = 'Mobiles & Tablets'
    AND strftime('%Y', o.order_date) = '2022'
    AND o.is_valid = 1
GROUP BY 
    s.sku_name
ORDER BY 
    total_qty DESC
LIMIT 5;
"""
df = pd.read_sql_query(query, conn)
print("\nTop 5 Mobiles & Tablets Products in 2022:")
print(df)

plt.figure(figsize=(10, 6))
plt.barh(df['sku_name'], df['total_qty'], color='skyblue')
plt.xlabel('Quantity Ordered')
plt.title('Top 5 Mobiles & Tablets Products in 2022')
plt.gca().invert_yaxis() 
plt.tight_layout()
plt.show()

conn.close()