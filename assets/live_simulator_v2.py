import mysql.connector
import random
import time
from datetime import date, timedelta

conn = mysql.connector.connect(
    host="localhost",
    user="root",
    password="password",  # your MySQL password
    database="shopmax_v2"
)
cursor = conn.cursor()

SELLER_IDS   = [101, 102, 103, 104, 105]
PRODUCT_IDS  = [201, 202, 203, 204, 205, 206, 207, 208, 209, 210]
REGIONS      = ["North", "South", "East", "West"]
REASONS      = ["Defective", "Changed Mind", "Wrong Item", "Late Delivery", "Damaged", "Not as Described"]
PAYMENTS     = ["UPI", "Credit Card", "Debit Card", "COD", "Wallet"]
DELIVERY     = ["Delhivery", "BlueDart", "Ekart", "XpressBees", "DTDC"]

# Get max IDs
cursor.execute("SELECT MAX(order_id) FROM orders")
order_id = cursor.fetchone()[0] + 1

cursor.execute("SELECT MAX(return_id) FROM returns")
return_id = cursor.fetchone()[0] + 1

print("🚀 Live simulator started for shopmax_v2...")
print("   Press Ctrl+C to stop\n")

while True:
    customer_id   = random.randint(1, 1000)
    product_id    = random.choice(PRODUCT_IDS)
    seller_id     = random.choice(SELLER_IDS)
    delay_days    = random.choices([0,1,2,3,5,7,10], weights=[40,20,15,10,5,4,6])[0]
    order_date    = date.today() - timedelta(days=random.randint(1,10))
    delivery_date = order_date + timedelta(days=random.randint(2,7) + delay_days)
    region        = random.choice(REGIONS)
    payment       = random.choice(PAYMENTS)
    delivery_co   = random.choice(DELIVERY)
    order_amount  = round(random.uniform(500, 70000), 2)

    cursor.execute("""
        INSERT INTO orders VALUES (%s,%s,%s,%s,%s,%s,%s,%s,%s,%s,%s)
    """, (order_id, customer_id, product_id, seller_id,
          delivery_co, payment, order_amount,
          order_date, delivery_date, delay_days, region))

    if random.random() < 0.80:
        return_date   = delivery_date + timedelta(days=random.randint(1,7))
        reason        = random.choice(REASONS)
        refund_amount = round(order_amount * random.uniform(0.5, 1.0), 2)
        status        = random.choices(['Processed','Pending','Rejected'],
                                       weights=[60,30,10])[0]
        refund_issue  = return_date + timedelta(days=2) if status == 'Processed' else None
        fraud         = 1 if (refund_amount > 5000 and delay_days > 5 and payment == 'COD') else 0
        rating        = random.randint(1,3) if reason in ['Defective','Damaged'] else random.randint(2,5)

        cursor.execute("""
            INSERT INTO returns VALUES (%s,%s,%s,%s,%s,%s,%s,%s,%s)
        """, (return_id, order_id, return_date, reason,
              refund_amount, status, refund_issue, fraud, rating))

        print(f"✅ Order {order_id} | {region} | {reason} | ₹{refund_amount} | {status}")
        return_id += 1

    conn.commit()
    order_id += 1
    time.sleep(10)