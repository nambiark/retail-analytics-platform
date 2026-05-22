---
title: Customer Analytics
---

# Customer Analytics

---

## Customer segments

```sql segments
select
    customer_segment,
    count(*) as customers,
    round(avg(lifetime_value), 2) as avg_ltv
from Postgres.dim_customers
group by customer_segment
order by customers desc
```

<BarChart
    data={segments}
    x="customer_segment"
    y="customers"
    title="Customers by Segment"
/>

---

## Average lifetime value by state

```sql ltv_by_state
select
    state,
    round(avg(lifetime_value), 2) as avg_ltv,
    count(*) as customers
from Postgres.dim_customers
where lifetime_value > 0
group by state
order by avg_ltv desc
limit 10
```

<BarChart
    data={ltv_by_state}
    x="state"
    y="avg_ltv"
    title="Avg Lifetime Value by State (R$)"
/>

---

## New customers by month

```sql new_customers
select
    date_trunc('month', first_order_at) as month,
    count(*) as new_customers
from Postgres.dim_customers
where first_order_at is not null
group by month
order by month
```

<LineChart
    data={new_customers}
    x="month"
    y="new_customers"
    title="New Customer Acquisition by Month"
/>

---

## Segment summary

<DataTable data={segments} />
