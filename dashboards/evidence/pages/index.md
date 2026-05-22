---
title: Retail Analytics Platform
---

# Retail Analytics Platform

End-to-end analytics for a Brazilian e-commerce platform.

---

## Key metrics

```sql total_metrics
select
    count(distinct order_id)            as total_orders,
    count(distinct customer_unique_id)  as total_customers,
    round(sum(total_payment_value), 2)  as total_revenue,
    round(avg(total_payment_value), 2)  as avg_order_value
from Postgres.fct_orders
where is_delivered = 'true'
```

<BigValue
    data={total_metrics}
    value="total_orders"
    title="Total Orders"
/>

<BigValue
    data={total_metrics}
    value="total_customers"
    title="Total Customers"
/>

<BigValue
    data={total_metrics}
    value="total_revenue"
    title="Total Revenue (R$)"
/>

<BigValue
    data={total_metrics}
    value="avg_order_value"
    title="Avg Order Value (R$)"
/>

---

## Monthly revenue trend

```sql monthly_revenue
select
    order_month,
    round(sum(total_payment_value), 2) as revenue,
    count(distinct order_id)           as orders
from Postgres.fct_orders
where order_month is not null
group by order_month
order by order_month
```

<LineChart
    data={monthly_revenue}
    x="order_month"
    y="revenue"
    title="Monthly Revenue (R$)"
/>

---

## Revenue by state

```sql revenue_by_state
select
    customer_state,
    round(sum(total_payment_value), 2) as revenue,
    count(distinct order_id)           as orders
from Postgres.fct_orders
group by customer_state
order by revenue desc
limit 10
```

<BarChart
    data={revenue_by_state}
    x="customer_state"
    y="revenue"
    title="Top 10 States by Revenue (R$)"
/>

---

## Order status breakdown

```sql order_status
select
    order_status,
    count(*) as orders
from Postgres.fct_orders
group by order_status
order by orders desc
```

<BarChart
    data={order_status}
    x="order_status"
    y="orders"
    title="Orders by Status"
/>
