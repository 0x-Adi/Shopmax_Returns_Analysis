-- ============================================================
-- Project   : ShopMax Returns & Refund Loss Recovery System
-- File      : 03_views.sql
-- Purpose   : Views & analytical queries for Power BI
-- ============================================================

USE shopmax_returns;

-- ─────────────────────────────────────────
-- View 1: Main Returns Analysis View
-- Used directly in Power BI
-- ─────────────────────────────────────────
CREATE VIEW vw_returns_analysis AS
WITH ReturnData AS (
    SELECT
        r.return_id,
        r.return_date,
        r.return_reason,
        r.refund_amount,
        r.refund_status,
        r.refund_issue_date,
        o.order_date,
        o.region,
        p.product_name,
        p.category,
        p.price,
        p.cost,
        s.seller_name,
        s.seller_rating,
        DATEDIFF(r.return_date, o.order_date) AS days_to_return
    FROM returns r
    JOIN orders  o ON r.order_id   = o.order_id
    JOIN products p ON o.product_id = p.product_id
    JOIN sellers  s ON o.seller_id  = s.seller_id
)
SELECT
    *,
    RANK() OVER (PARTITION BY region  ORDER BY refund_amount DESC) AS regional_loss_rank,
    RANK() OVER (PARTITION BY seller_name ORDER BY refund_amount DESC) AS seller_loss_rank
FROM ReturnData;


-- ─────────────────────────────────────────
-- View 2: Seller Risk Summary
-- ─────────────────────────────────────────
CREATE VIEW vw_seller_risk_summary AS
SELECT
    s.seller_name,
    s.seller_rating,
    COUNT(r.return_id)       AS total_returns,
    SUM(r.refund_amount)     AS total_refund_loss,
    ROUND(AVG(r.refund_amount), 2) AS avg_refund,
    SUM(CASE WHEN r.refund_status = 'Pending'   THEN r.refund_amount ELSE 0 END) AS pending_amount,
    SUM(CASE WHEN r.return_reason = 'Defective' THEN 1 ELSE 0 END) AS defective_returns,
    CASE
        WHEN COUNT(r.return_id) >= 3 THEN 'High Risk'
        WHEN COUNT(r.return_id) = 2  THEN 'Medium Risk'
        ELSE 'Low Risk'
    END AS risk_tier
FROM sellers s
LEFT JOIN orders  o ON s.seller_id  = o.seller_id
LEFT JOIN returns r ON o.order_id   = r.order_id
GROUP BY s.seller_id, s.seller_name, s.seller_rating;


-- ─────────────────────────────────────────
-- View 3: Region Loss Summary
-- ─────────────────────────────────────────
CREATE VIEW vw_region_loss_summary AS
SELECT
    o.region,
    COUNT(r.return_id)   AS total_returns,
    SUM(r.refund_amount) AS total_refund_loss,
    ROUND(SUM(r.refund_amount) / COUNT(r.return_id), 2) AS avg_loss_per_return
FROM orders  o
JOIN returns r ON o.order_id = r.order_id
GROUP BY o.region
ORDER BY total_refund_loss DESC;
