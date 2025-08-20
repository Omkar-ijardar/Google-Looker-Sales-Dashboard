import sqlite3
import pandas as pd
conn = sqlite3.connect('sales_data.db')
cursor = conn.cursor()
query = """
SELECT DISTINCT 
    o.customer_id,
    c.registered_date
FROM 
    order_detail o
JOIN 
    customer_detail c ON o.customer_id = c.customer_id
WHERE 
    strftime('%Y', o.order_date) = '2022'
    AND o.is_gross = 1
    AND o.is_valid = 0
    AND o.is_net = 0
"""

df = pd.read_sql_query(query, conn)

print("\nCustomers who checked out but did NOT pay in 2022:")
print(df)

if df.empty:
    print("✅ No customers found who checked out but didn’t pay in 2022.")
else:
    df.to_csv("customers_no_payment_2022.csv", index=False)
    print("Data saved to customers_no_payment_2022.csv")

conn.close()
