# Power BI Dashboard Guide

## Connection Setup

| Setting | Value |
|---|---|
| Connector | MySQL Database |
| Server | localhost |
| Database | shopmax_returns |
| View used | vw_returns_analysis |

## DAX Measures Created

```dax
Total Refund Loss =
SUM('shopmax_returns vw_returns_analysis'[refund_amount])

Total Returns =
COUNTROWS('shopmax_returns vw_returns_analysis')

Pending Refunds =
CALCULATE(
    COUNTROWS('shopmax_returns vw_returns_analysis'),
    'shopmax_returns vw_returns_analysis'[refund_status] = "Pending"
)

Pending Refund Amount =
CALCULATE(
    SUM('shopmax_returns vw_returns_analysis'[refund_amount]),
    'shopmax_returns vw_returns_analysis'[refund_status] = "Pending"
)

Avg Refund Amount =
AVERAGE('shopmax_returns vw_returns_analysis'[refund_amount])
```

## Dashboard Visuals

| Visual | Type | Fields |
|---|---|---|
| KPI Cards (x4) | Card | Total Refund Loss, Total Returns, Pending Refunds, Pending Refund Amount |
| Refund Loss by Region | Clustered Bar Chart | Y-axis: region / X-axis: Total Refund Loss |
| Returns by Reason | Pie Chart | Legend: return_reason / Values: Total Returns |
| Seller-wise Loss Breakdown | Table | seller_name, Total Returns, Total Refund Loss, Pending Refund Amount |
| Filter by Region | Slicer | region |
| Filter by Return Reason | Slicer | return_reason |

## Key Business Insights from Dashboard

- **South region** has the highest refund loss — needs seller audit
- **Gadget Galaxy** (rating 3.8) accounts for 100% of returns — flagged as High Risk seller
- **66.67%** of returns are due to Defective products — quality control issue
- **₹49.99** still pending in unprocessed refunds — operations team action needed
