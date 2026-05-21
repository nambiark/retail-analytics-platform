# Standardised Metrics

This document defines the company-wide metrics available in the mart layer.
All metrics are computed in dbt and served via Metabase.

## Revenue metrics

| Metric | Definition | Source model |
|---|---|---|
| Gross Merchandise Value (GMV) | `SUM(total_payment_value)` | `fct_orders` |
| Average Order Value (AOV) | `AVG(total_payment_value)` | `fct_orders` |
| Revenue by state | `SUM(total_payment_value) GROUP BY customer_state` | `fct_orders` |
| Monthly revenue | `SUM(total_payment_value) GROUP BY order_month` | `fct_orders` |

## Customer metrics

| Metric | Definition | Source model |
|---|---|---|
| Customer Lifetime Value (LTV) | `SUM(total_payment_value)` per `customer_unique_id` | `dim_customers` |
| Customer segments | VIP (5+ orders), Repeat (2-4), One-time (1) | `dim_customers` |
| New customers | `COUNT(customer_unique_id)` by `first_order_at` month | `dim_customers` |

## Operational metrics

| Metric | Definition | Source model |
|---|---|---|
| Average delivery time | `AVG(days_to_deliver)` for delivered orders | `fct_orders` |
| On-time delivery rate | `COUNT(*) WHERE days_early_or_late >= 0` / total | `fct_orders` |
| Order fulfillment rate | Delivered orders / total orders | `fct_orders` |

## Product metrics

| Metric | Definition | Source model |
|---|---|---|
| Revenue by category | `SUM(total_revenue)` per `category_name_en` | `dim_products` |
| Revenue tier | High (>10k), Medium (1k-10k), Low (<1k) | `dim_products` |
| Average product price | `AVG(avg_price)` per category | `dim_products` |

## Data quality metrics

| Metric | Target | Tool |
|---|---|---|
| Raw expectation pass rate | 100% | Great Expectations |
| dbt test pass rate | 100% | dbt Core |
| Pipeline success rate | >95% | Prefect |
