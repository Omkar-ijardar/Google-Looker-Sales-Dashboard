import sqlite3
import pandas as pd
import matplotlib.pyplot as plt

conn = sqlite3.connect('sales_data.db')
cursor = conn.cursor()


query_2021 = """
SELECT 
    s.sku_name,
    SUM(o.qty_ordered) AS qty_2021
FROM 
    order_detail o
JOIN 
    sku_detail s ON o.sku_id = s.sku_id
WHERE 
    s.category = 'Others'
    AND strftime('%Y', o.order_date) = '2021'
    AND o.is_valid = 1
GROUP BY 
    s.sku_name
"""

query_2022 = """
SELECT 
    s.sku_name,
    SUM(o.qty_ordered) AS qty_2022
FROM 
    order_detail o
JOIN 
    sku_detail s ON o.sku_id = s.sku_id
WHERE 
    s.category = 'Others'
    AND strftime('%Y', o.order_date) = '2022'
    AND o.is_valid = 1
GROUP BY 
    s.sku_name
"""

df_2021 = pd.read_sql_query(query_2021, conn)
df_2022 = pd.read_sql_query(query_2022, conn)


df = pd.merge(df_2021, df_2022, on='sku_name', how='outer')

df.fillna(0, inplace=True)

df['qty_diff'] = df['qty_2022'] - df['qty_2021']
df['pct_change'] = ((df['qty_2022'] - df['qty_2021']) / df['qty_2021'].replace(0, 1)) * 100

def classify(change):
    if change < -10:
        return 'DOWN'
    elif change > 10:
        return 'UP'
    else:
        return 'FAIR'

df['trend'] = df['pct_change'].apply(classify)
df_down = df.sort_values(by='qty_diff').head(20)

print("\nTop 20 'Others' Products with Largest Decrease in Sales (2022 vs 2021):")
print(df_down[['sku_name', 'qty_2021', 'qty_2022', 'qty_diff', 'pct_change', 'trend']])


plt.figure(figsize=(10, 6))
plt.barh(df_down['sku_name'], df_down['qty_diff'], color='tomato')
plt.xlabel('Decrease in Quantity Ordered')
plt.title("Top 20 'Others' Products with Largest Decrease in Sales (2022 vs 2021)")
plt.gca().invert_yaxis()
plt.tight_layout()
plt.show()

conn.close()