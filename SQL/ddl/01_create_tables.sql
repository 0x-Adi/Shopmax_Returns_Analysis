-- ============================================================
-- Project   : ShopMax Returns & Refund Loss Recovery System
-- Author    : Aditya Krishna
-- Database  : MySQL
-- File      : 01_create_tables.sql
-- Purpose   : DDL - Create all tables
-- ============================================================

CREATE DATABASE IF NOT EXISTS shopmax_returns;
USE shopmax_returns;

CREATE TABLE sellers (
    seller_id     INT PRIMARY KEY,
    seller_name   VARCHAR(100),
    seller_rating DECIMAL(3,2),
    join_date     DATE
);

CREATE TABLE products (
    product_id   INT PRIMARY KEY,
    product_name VARCHAR(255),
    category     VARCHAR(100),
    price        DECIMAL(10,2),
    cost         DECIMAL(10,2)
);

CREATE TABLE orders (
    order_id      INT PRIMARY KEY,
    customer_id   INT,
    product_id    INT,
    seller_id     INT,
    order_date    DATE,
    delivery_date DATE,
    region        VARCHAR(50),
    FOREIGN KEY (product_id) REFERENCES products(product_id),
    FOREIGN KEY (seller_id)  REFERENCES sellers(seller_id)
);

CREATE TABLE returns (
    return_id        INT PRIMARY KEY,
    order_id         INT,
    return_date      DATE,
    return_reason    VARCHAR(255),
    refund_amount    DECIMAL(10,2),
    refund_status    VARCHAR(50),
    refund_issue_date DATE,
    FOREIGN KEY (order_id) REFERENCES orders(order_id)
);
