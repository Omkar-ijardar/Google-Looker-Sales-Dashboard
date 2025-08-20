import sqlite3
import pandas as pd
import matplotlib.pyplot as plt

conn=sqlite3.connect('sales_data.db')

query_2021 = """
SELECT 
    s.sku_name,
    SUM(o.qty_ordered) AS qty_2021
FROM 
    order_detail o
JOIN 
    sku_detail s ON o.sku_id = s.sku_id
WHERE 
    strftime('%Y', o.order_date) = '2021'
    AND o.is_valid = 1
GROUP BY 
    s.sku_name
"""
df_2021=pd.read_sql_query(query_2021, conn)

query_2022 = """
SELECT 
    s.sku_name,
    SUM(o.qty_ordered) AS qty_2022
FROM 
    order_detail o
JOIN 
    sku_detail s ON o.sku_id = s.sku_id
WHERE 
    strftime('%Y', o.order_date) = '2022'
    AND o.is_valid = 1
GROUP BY 
    s.sku_name
"""
df_2022=pd.read_sql_query(query_2022, conn)

merged=pd.merge(df_2021, df_2022, on='sku_name', how='outer')

merged.fillna(0, inplace=True)

merged['qty_diff'] =merged['qty_2022'] - merged['qty_2021']



drop_df = merged[merged['qty_diff']<0]

top10_drop = drop_df.sort_values(by='qty_diff').head(10)

print("\n Top 10 Products with Largest Sales Decrease (2022 vs 2021):")
print(top10_drop[['sku_name', 'qty_2021', 'qty_2022', 'qty_diff']])


plt.figure(figsize=(10, 6))
plt.barh(top10_drop['sku_name'], top10_drop['qty_diff'], color='red')
plt.xlabel("Decrease in Quantity Ordered")
plt.title("Top 10 Products with Largest Sales Drop (2022 vs 2021)")
plt.tight_layout()
plt.show()

conn.close()
