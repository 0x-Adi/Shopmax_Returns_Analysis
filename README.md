# ShopMax — Returns & Refund Loss Recovery System
### End-to-End Data Analytics Project: MySQL + Power BI

---

## Business Problem

ShopMax, a growing e-commerce brand, was losing significant revenue every month due to product returns and unprocessed refunds. The operations team had no visibility into:
- Which sellers were causing the most returns
- Which regions had the highest refund losses
- How many refunds were still pending and for how long
- Whether returns were due to defective products or customer behaviour

**Goal:** Build a data pipeline and executive dashboard to identify loss hotspots and help the business recover revenue.

---

## Project Architecture

```
MySQL Database
      │
      ▼
  SQL Views (cleaned + joined data)
      │
      ▼
Power BI (connected via MySQL Connector)
      │
      ▼
Executive Dashboard (KPIs + Charts + Slicers)
```

---

## Tools & Technologies

| Tool | Purpose |
|---|---|
| MySQL | Database & SQL analysis |
| MySQL Workbench | Query execution |
| Power BI Desktop | Dashboard & visualization |
| VS Code | SQL script editing |
| Git + GitHub | Version control |

---

## Database Schema

```
sellers ──────┐
              ├──> orders ──> returns
products ─────┘
```

**Tables:**
- `sellers` — seller info and ratings
- `products` — product catalog with price and cost
- `orders` — all customer orders with region and delivery info
- `returns` — return records with reason, refund amount, and status

---

## SQL Features Used

- `JOIN` across 4 tables
- `CTEs` (Common Table Expressions)
- `RANK()` window function — regional and seller loss ranking
- `CASE WHEN` — risk tier classification
- `DATEDIFF` — days to return calculation
- `GROUP BY` with aggregations
- 3 analytical `VIEWS` for Power BI consumption

---

## Power BI Dashboard

**KPI Cards:**
- Total Refund Loss
- Total Returns
- Pending Refunds
- Pending Refund Amount

**Visuals:**
- Refund Loss by Region (Bar Chart)
- Returns by Reason (Pie Chart)
- Seller-wise Loss Breakdown (Table)
- Filter by Region (Slicer)
- Filter by Return Reason (Slicer)

> Dashboard file: `powerbi/ShopMax_Returns_Dashboard.pbix`

---

## Key Insights

- South region accounts for the highest refund loss
- Gadget Galaxy (seller rating: 3.8) is responsible for all returns — classified as High Risk
- 66.67% of returns are due to defective products — signals a quality control gap
- Pending refunds worth $49.99 require immediate operations team action

---

## Folder Structure

```
shopmax-returns-analysis/
│
├── sql/
│   ├── ddl/
│   │   └── 01_create_tables.sql
│   ├── dml/
│   │   └── 02_insert_data.sql
│   └── views/
│       └── 03_views.sql
│
├── powerbi/
│   ├── ShopMax_Returns_Dashboard.pbix
│   └── POWERBI_GUIDE.md
│
├── assets/
│   └── dashboard_screenshot.png
│
└── README.md
```

---

## How to Run This Project

1. Install MySQL and create the database:
```sql
CREATE DATABASE shopmax_returns;
```

2. Run SQL scripts in order:
```
01_create_tables.sql
02_insert_data.sql
03_views.sql
```

3. Install MySQL Connector/NET for Power BI

4. Open Power BI → Get Data → MySQL Database
   - Server: `localhost`
   - Database: `shopmax_returns`
   - Load: `vw_returns_analysis` view

5. Open `ShopMax_Returns_Dashboard.pbix`

---

## Author

**Your Name**
- LinkedIn: https://www.linkedin.com/in/0x-adi/
- GitHub: https://github.com/0x-Adi

---

*This is a portfolio project built to demonstrate real-world data analytics skills using MySQL and Power BI.*
