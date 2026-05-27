import pandas as pd
import matplotlib.pyplot as plt
import seaborn as sns
import mysql.connector
import os

import matplotlib
matplotlib.use('Agg')  # Save charts without opening windows
import pandas as pd
import matplotlib.pyplot as plt
import seaborn as sns
import mysql.connector
import os

# ─────────────────────────────────────────
# Connect & Load Data
# ─────────────────────────────────────────
conn = mysql.connector.connect(
    host="localhost",
    user="root",
    password="password",  # your MySQL password
    database="shopmax_v2"
)

df         = pd.read_sql("SELECT * FROM vw_returns_analysis", conn)
df_monthly = pd.read_sql("SELECT * FROM vw_monthly_loss_trend", conn)
df_seller  = pd.read_sql("SELECT * FROM vw_seller_scorecard", conn)
df_delay   = pd.read_sql("SELECT * FROM vw_delay_refund_correlation", conn)
df_category= pd.read_sql("SELECT * FROM vw_refund_rate_by_category", conn)
conn.close()

# Output folder
os.makedirs("eda_charts", exist_ok=True)
sns.set_theme(style="darkgrid")
plt.rcParams.update({"figure.dpi": 150, "figure.figsize": (10, 5)})

print(f"✅ Data loaded — {len(df)} return records\n")
print(df.head(3))

# ─────────────────────────────────────────
# Chart 1: Top Return Reasons
# ─────────────────────────────────────────
plt.figure()
reason_counts = df['return_reason'].value_counts()
sns.barplot(x=reason_counts.values, y=reason_counts.index, palette="Reds_r")
plt.title("Top Return Reasons", fontsize=14, fontweight='bold')
plt.xlabel("Number of Returns")
plt.tight_layout()
plt.savefig("eda_charts/01_top_return_reasons.png")
plt.show()
print("✅ Chart 1 saved")

# ─────────────────────────────────────────
# Chart 2: Monthly Refund Loss Trend
# ─────────────────────────────────────────
plt.figure()
df_monthly['period'] = df_monthly['month_name'].astype(str) + " " + df_monthly['return_year'].astype(str)
sns.lineplot(data=df_monthly, x='period', y='total_refund_loss',
             marker='o', color='crimson', linewidth=2)
plt.xticks(rotation=45, ha='right')
plt.title("Monthly Refund Loss Trend", fontsize=14, fontweight='bold')
plt.xlabel("Month")
plt.ylabel("Total Refund Loss (₹)")
plt.tight_layout()
plt.savefig("eda_charts/02_monthly_loss_trend.png")
plt.show()
print("✅ Chart 2 saved")

# ─────────────────────────────────────────
# Chart 3: Shipping Delay vs Avg Refund
# ─────────────────────────────────────────
plt.figure()
order = ['On Time', 'Slight Delay', 'Moderate Delay', 'Severe Delay']
df_delay['delay_category'] = pd.Categorical(df_delay['delay_category'],
                                             categories=order, ordered=True)
df_delay = df_delay.sort_values('delay_category')
sns.barplot(data=df_delay, x='delay_category', y='avg_refund_amount', palette="OrRd")
plt.title("Shipping Delay vs Average Refund Amount", fontsize=14, fontweight='bold')
plt.xlabel("Delay Category")
plt.ylabel("Avg Refund (₹)")
plt.tight_layout()
plt.savefig("eda_charts/03_delay_vs_refund.png")
plt.show()
print("✅ Chart 3 saved")

# ─────────────────────────────────────────
# Chart 4: Seller Performance
# ─────────────────────────────────────────
plt.figure()
sns.barplot(data=df_seller, x='seller_name', y='return_rate_pct', palette="coolwarm")
plt.title("Seller Return Rate (%)", fontsize=14, fontweight='bold')
plt.xlabel("Seller")
plt.ylabel("Return Rate %")
plt.tight_layout()
plt.savefig("eda_charts/04_seller_performance.png")
plt.show()
print("✅ Chart 4 saved")

# ─────────────────────────────────────────
# Chart 5: Refund Rate by Product Category
# ─────────────────────────────────────────
plt.figure()
sns.barplot(data=df_category, x='refund_rate_pct', y='product_category', palette="Blues_r")
plt.title("Refund Rate by Product Category (%)", fontsize=14, fontweight='bold')
plt.xlabel("Refund Rate %")
plt.ylabel("Category")
plt.tight_layout()
plt.savefig("eda_charts/05_refund_rate_by_category.png")
plt.show()
print("✅ Chart 5 saved")

# ─────────────────────────────────────────
# Chart 6: Fraud vs Non-Fraud by Region
# ─────────────────────────────────────────
plt.figure()
fraud_region = df.groupby(['region', 'fraud_flag']).size().reset_index(name='count')
fraud_region['fraud_flag'] = fraud_region['fraud_flag'].map({0: 'Legitimate', 1: 'Fraud'})
sns.barplot(data=fraud_region, x='region', y='count',
            hue='fraud_flag', palette={'Legitimate':'steelblue','Fraud':'crimson'})
plt.title("Fraud vs Legitimate Returns by Region", fontsize=14, fontweight='bold')
plt.xlabel("Region")
plt.ylabel("Count")
plt.tight_layout()
plt.savefig("eda_charts/06_fraud_by_region.png")
plt.show()
print("✅ Chart 6 saved")

# ─────────────────────────────────────────
# Chart 7: Customer Rating Distribution
# ─────────────────────────────────────────
plt.figure()
sns.countplot(data=df, x='customer_rating', palette="RdYlGn")
plt.title("Customer Rating Distribution on Returns", fontsize=14, fontweight='bold')
plt.xlabel("Rating (1=Worst, 5=Best)")
plt.ylabel("Count")
plt.tight_layout()
plt.savefig("eda_charts/07_customer_rating.png")
plt.show()
print("✅ Chart 7 saved")

print("\n🎯 All 7 EDA charts saved in eda_charts/ folder!")