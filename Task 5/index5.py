import sqlite3
import pandas as pd
import matplotlib.pyplot as plt

conn=sqlite3.connect('sales_data.db')

query ="""
SELECT 
    strftime('%m', order_date) AS month,
    strftime('%w', order_date) AS weekday_number,  -- 0=Sunday, 6=Saturday
    strftime('%Y-%m-%d', order_date) AS date,
    SUM(before_discount) AS total_sales
FROM 
    order_detail
WHERE 
    strftime('%Y', order_date) = '2022'
    AND strftime('%m', order_date) IN ('10', '11', '12')
    AND is_valid = 1
GROUP BY 
    date
"""

df = pd.read_sql_query(query, conn)
df['weekday_number'] = df['weekday_number'].astype(int)

# Label as weekend/weekday
df['day_type'] = df['weekday_number'].apply(lambda x: 'Weekend' if x in [0, 6] else 'Weekday')

month_map = {'10': 'October', '11': 'November', '12': 'December'}
df['month_name'] = df['month'].map(month_map)

grouped = df.groupby(['month_name', 'day_type'])['total_sales'].mean().reset_index()
grouped.rename(columns={'total_sales': 'avg_daily_sales'}, inplace=True)

total_grouped = df.groupby(['day_type'])['total_sales'].mean().reset_index()
total_grouped.rename(columns={'total_sales': 'avg_daily_sales'}, inplace=True)

print("\n📊 Monthly Comparison of Avg Daily Sales:")
print(grouped)

print("\n📊 Overall Q4 Comparison of Avg Daily Sales:")
print(total_grouped)
plt.figure(figsize=(10, 6))
for month in grouped['month_name'].unique():
    data = grouped[grouped['month_name'] == month]
    plt.bar(data['day_type'] + ' - ' + month, data['avg_daily_sales'])

plt.title("Avg Daily Sales: Weekends vs Weekdays (Q4 2022)")
plt.ylabel("Avg Daily Sales (Before Discount)")
plt.tight_layout()
plt.show()


plt.figure(figsize=(6, 4))
plt.bar(total_grouped['day_type'], total_grouped['avg_daily_sales'], color=['lightgreen', 'orange'])
plt.title("Overall Avg Daily Sales: Weekends vs Weekdays (Q4 2022)")
plt.ylabel("Avg Daily Sales (Before Discount)")
plt.tight_layout()
plt.show()

# Close DB
conn.close()
