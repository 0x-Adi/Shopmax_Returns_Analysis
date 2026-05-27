import mysql.connector
import random
from faker import Faker
from datetime import date, timedelta

fake = Faker('en_IN')  # Indian locale for realistic data

# ─────────────────────────────────────────
# Connect to MySQL
# ─────────────────────────────────────────
conn = mysql.connector.connect(
    host="localhost",
    user="root",
    password="password",        # your MySQL password
    charset='utf8mb4'
)
cursor = conn.cursor()

# ─────────────────────────────────────────
# Create Fresh Database
# ─────────────────────────────────────────
cursor.execute("DROP DATABASE IF EXISTS shopmax_v2")
cursor.execute("CREATE DATABASE shopmax_v2")
cursor.execute("USE shopmax_v2")
print("✅ Database created")

# ─────────────────────────────────────────
# Create Tables
# ─────────────────────────────────────────
cursor.execute("""
CREATE TABLE customers (
    customer_id     INT PRIMARY KEY,
    customer_name   VARCHAR(100),
    email           VARCHAR(100),
    city            VARCHAR(50),
    signup_date     DATE
)""")

cursor.execute("""
CREATE TABLE sellers (
    seller_id               INT PRIMARY KEY,
    seller_name             VARCHAR(100),
    seller_rating           DECIMAL(3,2),
    category_speciality     VARCHAR(50),
    join_date               DATE
)""")

cursor.execute("""
CREATE TABLE products (
    product_id          INT PRIMARY KEY,
    product_name        VARCHAR(255),
    product_category    VARCHAR(100),
    price               DECIMAL(10,2),
    cost                DECIMAL(10,2)
)""")

cursor.execute("""
CREATE TABLE orders (
    order_id                INT PRIMARY KEY,
    customer_id             INT,
    product_id              INT,
    seller_id               INT,
    delivery_partner        VARCHAR(50),
    payment_method          VARCHAR(50),
    order_amount            DECIMAL(10,2),
    order_date              DATE,
    delivery_date           DATE,
    shipping_delay_days     INT,
    region                  VARCHAR(50),
    FOREIGN KEY (customer_id) REFERENCES customers(customer_id),
    FOREIGN KEY (product_id)  REFERENCES products(product_id),
    FOREIGN KEY (seller_id)   REFERENCES sellers(seller_id)
)""")

cursor.execute("""
CREATE TABLE returns (
    return_id           INT PRIMARY KEY,
    order_id            INT,
    return_date         DATE,
    return_reason       VARCHAR(100),
    refund_amount       DECIMAL(10,2),
    refund_status       VARCHAR(50),
    refund_issue_date   DATE,
    fraud_flag          TINYINT(1),
    customer_rating     INT,
    FOREIGN KEY (order_id) REFERENCES orders(order_id)
)""")
print("✅ Tables created")

# ─────────────────────────────────────────
# Reference Data
# ─────────────────────────────────────────
CITIES          = ['Mumbai', 'Delhi', 'Bangalore', 'Hyderabad', 'Chennai',
                   'Kolkata', 'Pune', 'Ahmedabad', 'Jaipur', 'Lucknow']
REGIONS         = ['North', 'South', 'East', 'West']
DELIVERY        = ['Delhivery', 'BlueDart', 'Ekart', 'XpressBees', 'DTDC']
PAYMENTS        = ['UPI', 'Credit Card', 'Debit Card', 'Net Banking', 'COD', 'Wallet']
RETURN_REASONS  = ['Defective', 'Changed Mind', 'Wrong Item',
                   'Late Delivery', 'Damaged', 'Not as Described']
CATEGORIES      = ['Audio', 'Wearables', 'Accessories', 'Mobile', 'Laptop',
                   'Home Appliances', 'Fashion', 'Sports']

SELLERS = [
    (101, 'Tech Haven',    4.5, 'Electronics',   '2023-01-15'),
    (102, 'Gadget Galaxy', 3.8, 'Accessories',   '2023-02-20'),
    (103, 'Electro World', 4.8, 'Electronics',   '2023-03-10'),
    (104, 'Fashion Hub',   4.2, 'Fashion',        '2023-04-05'),
    (105, 'Sport Zone',    3.9, 'Sports',         '2023-05-18'),
]

PRODUCTS = [
    (201, 'Wireless Earbuds',    'Audio',           1499, 600),
    (202, 'Smart Watch',         'Wearables',       8999, 4000),
    (203, 'Gaming Mouse',        'Accessories',     2499, 900),
    (204, 'Mechanical Keyboard', 'Accessories',     5999, 2500),
    (205, 'Smartphone X12',      'Mobile',         19999, 9000),
    (206, 'Laptop Pro 15',       'Laptop',         65999, 35000),
    (207, 'Running Shoes',       'Sports',          3499, 1200),
    (208, 'Casual T-Shirt',      'Fashion',          799,  250),
    (209, 'Air Purifier',        'Home Appliances', 9999, 4500),
    (210, 'Bluetooth Speaker',   'Audio',           3999, 1500),
]

# ─────────────────────────────────────────
# Insert Sellers & Products
# ─────────────────────────────────────────
cursor.executemany("""
    INSERT INTO sellers VALUES (%s,%s,%s,%s,%s)
""", SELLERS)

cursor.executemany("""
    INSERT INTO products VALUES (%s,%s,%s,%s,%s)
""", PRODUCTS)
print("✅ Sellers & Products inserted")

# ─────────────────────────────────────────
# Insert 1000 Customers
# ─────────────────────────────────────────
customers = []
for i in range(1, 1001):
    customers.append((
        i,
        fake.name(),
        fake.email(),
        random.choice(CITIES),
        fake.date_between(start_date=date(2022,1,1), end_date=date(2023,12,31))
    ))
cursor.executemany("INSERT INTO customers VALUES (%s,%s,%s,%s,%s)", customers)
print("✅ 1000 Customers inserted")

# ─────────────────────────────────────────
# Insert 5000 Orders + Returns
# ─────────────────────────────────────────
order_id  = 1
return_id = 1
orders_inserted  = 0
returns_inserted = 0

for _ in range(5000):
    customer_id    = random.randint(1, 1000)
    product        = random.choice(PRODUCTS)
    seller         = random.choice(SELLERS)
    order_date     = fake.date_between(start_date=date(2023,1,1), end_date=date(2024,12,31))
    delay_days     = random.choices([0,1,2,3,5,7,10,15], weights=[40,20,15,10,5,4,3,3])[0]
    delivery_date  = order_date + timedelta(days=random.randint(2,7) + delay_days)
    region         = random.choice(REGIONS)
    payment        = random.choice(PAYMENTS)
    delivery_co    = random.choice(DELIVERY)
    order_amount   = round(product[4] * random.uniform(0.9, 1.2), 2)

    cursor.execute("""
        INSERT INTO orders VALUES (%s,%s,%s,%s,%s,%s,%s,%s,%s,%s,%s)
    """, (order_id, customer_id, product[0], seller[0],
          delivery_co, payment, order_amount,
          order_date, delivery_date, delay_days, region))
    orders_inserted += 1

    # 30% chance of return
    if random.random() < 0.30:
        return_date   = delivery_date + timedelta(days=random.randint(1,7))
        reason        = random.choice(RETURN_REASONS)
        refund_amount = round(order_amount * random.uniform(0.5, 1.0), 2)
        status        = random.choices(['Processed','Pending','Rejected'],
                                       weights=[60,30,10])[0]
        refund_issue  = return_date + timedelta(days=random.randint(1,5)) \
                        if status == 'Processed' else None

        # fraud logic — high return amount + delay + COD
        fraud = 1 if (refund_amount > 5000 and delay_days > 5
                      and payment == 'COD') else 0

        rating = random.randint(1, 3) if reason in ['Defective','Damaged'] \
                 else random.randint(2, 5)

        cursor.execute("""
            INSERT INTO returns VALUES (%s,%s,%s,%s,%s,%s,%s,%s,%s)
        """, (return_id, order_id, return_date, reason,
              refund_amount, status, refund_issue, fraud, rating))
        returns_inserted += 1
        return_id += 1

    order_id += 1

conn.commit()
print(f"✅ {orders_inserted} Orders inserted")
print(f"✅ {returns_inserted} Returns inserted")
print("\n🚀 shopmax_v2 database is ready!")
cursor.close()
conn.close()