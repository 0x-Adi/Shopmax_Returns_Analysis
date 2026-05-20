-- ============================================================
-- Project   : ShopMax Returns & Refund Loss Recovery System
-- File      : 02_insert_data.sql
-- Purpose   : DML - Insert sample data
-- ============================================================

USE shopmax_returns;

-- ─────────────────────────────────────────
-- 1. Sellers
-- ─────────────────────────────────────────
INSERT INTO sellers (seller_id, seller_name, seller_rating, join_date) VALUES
(101, 'Tech Haven',    4.5, '2025-01-15'),
(102, 'Gadget Galaxy', 3.8, '2025-02-20'),
(103, 'Electro World', 4.8, '2025-03-10');

-- ─────────────────────────────────────────
-- 2. Products
-- ─────────────────────────────────────────
INSERT INTO products (product_id, product_name, category, price, cost) VALUES
(201, 'Wireless Earbuds',    'Audio',       49.99,  20.00),
(202, 'Smart Watch',         'Wearables',  199.99,  90.00),
(203, 'Gaming Mouse',        'Accessories', 59.99,  25.00),
(204, 'Mechanical Keyboard', 'Accessories',129.99,  60.00);

-- ─────────────────────────────────────────
-- 3. Orders
-- ─────────────────────────────────────────
INSERT INTO orders (order_id, customer_id, product_id, seller_id, order_date, delivery_date, region) VALUES
(1001, 501, 201, 101, '2026-05-01', '2026-05-04', 'North'),
(1002, 502, 203, 102, '2026-05-02', '2026-05-05', 'South'),
(1003, 503, 202, 103, '2026-05-03', '2026-05-05', 'East'),
(1004, 504, 204, 101, '2026-05-04', '2026-05-08', 'West'),
(1005, 505, 201, 102, '2026-05-05', '2026-05-07', 'North'),
(1006, 506, 203, 102, '2026-05-06', '2026-05-09', 'South');

-- ─────────────────────────────────────────
-- 4. Returns
-- ─────────────────────────────────────────
INSERT INTO returns (return_id, order_id, return_date, return_reason, refund_amount, refund_status, refund_issue_date) VALUES
(5001, 1002, '2026-05-07', 'Defective',    59.99, 'Processed', '2026-05-08'),
(5002, 1005, '2026-05-09', 'Changed Mind', 49.99, 'Pending',   NULL),
(5003, 1006, '2026-05-11', 'Defective',    59.99, 'Processed', '2026-05-12');
