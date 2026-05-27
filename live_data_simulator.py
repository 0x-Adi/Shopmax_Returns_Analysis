import mysql.connector
import random
import time
from faker import Faker
from datetime import date, timedelta

fake = Faker()

# ─────────────────────────────────────────
# Database Connection
# ─────────────────────────────────────────
conn = mysql.connector.connect(
    host="localhost",
    user="root",          # change if different
    password="password",          # your MySQL password
    database="shopmax_returns"
)
cursor = conn.cursor()

# ─────────────────────────────────────────
# Config
# ─────────────────────────────────────────
SELLER_IDS    = [101, 102, 103]
PRODUCT_IDS   = [201, 202, 203, 204]
REGIONS       = ["North", "South", "East", "West"]
RETURN_REASONS= ["Defective", "Changed Mind", "Wrong Item", "Late Delivery", "Damaged"]
REFUND_STATUS = ["Processed", "Pending"]

order_id  = 2000   # starting from 2000 to avoid conflicts
return_id = 6000

# ─────────────────────────────────────────
# Insert Function
# ─────────────────────────────────────────
def insert_live_data():
    global order_id, return_id

    # Random order
    customer_id   = random.randint(600, 999)
    product_id    = random.choice(PRODUCT_IDS)
    seller_id     = random.choice(SELLER_IDS)
    order_date    = date.today() - timedelta(days=random.randint(1, 10))
    delivery_date = order_date + timedelta(days=random.randint(2, 7))
    region        = random.choice(REGIONS)

    cursor.execute("""
        INSERT INTO orders (order_id, customer_id, product_id, seller_id, order_date, delivery_date, region)
        VALUES (%s, %s, %s, %s, %s, %s, %s)
    """, (order_id, customer_id, product_id, seller_id, order_date, delivery_date, region))

    # Random return for this order
    return_date   = delivery_date + timedelta(days=random.randint(1, 5))
    reason        = random.choice(RETURN_REASONS)
    refund_amount = round(random.uniform(20, 200), 2)
    status        = random.choice(REFUND_STATUS)
    refund_issue  = return_date + timedelta(days=2) if status == "Processed" else None

    cursor.execute("""
        INSERT INTO returns (return_id, order_id, return_date, return_reason, refund_amount, refund_status, refund_issue_date)
        VALUES (%s, %s, %s, %s, %s, %s, %s)
    """, (return_id, order_id, return_date, reason, refund_amount, status, refund_issue))

    conn.commit()

    print(f"✅ Inserted → Order {order_id} | Region: {region} | Reason: {reason} | Refund: ₹{refund_amount} | Status: {status}")

    order_id  += 1
    return_id += 1

# ─────────────────────────────────────────
# Run Every 10 Seconds
# ─────────────────────────────────────────
print("🚀 Live data simulator started... inserting every 10 seconds")
print("   Press Ctrl + C to stop\n")

while True:
    insert_live_data()
    time.sleep(10)