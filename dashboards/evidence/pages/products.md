---
title: Product Performance
---

# Product Performance

---

## Revenue by category

```sql category_revenue
select
    category_name_en,
    round(sum(total_revenue), 2) as revenue,
    count(*) as products,
    round(avg(avg_price), 2) as avg_price
from Postgres.dim_products
where category_name_en is not null
group by category_name_en
order by revenue desc
limit 15
```

<BarChart
    data={category_revenue}
    x="category_name_en"
    y="revenue"
    title="Top 15 Categories by Revenue (R$)"
    swapXY=true
/>

---

## Products by revenue tier

```sql revenue_tiers
select
    revenue_tier,
    count(*) as products,
    round(sum(total_revenue), 2) as total_revenue
from Postgres.dim_products
group by revenue_tier
order by total_revenue desc
```

<BarChart
    data={revenue_tiers}
    x="revenue_tier"
    y="products"
    title="Products by Revenue Tier"
/>

---

## Top 20 products by revenue

```sql top_products
select
    product_id,
    category_name_en,
    round(total_revenue, 2) as revenue,
    total_orders,
    round(avg_price, 2) as avg_price,
    revenue_tier
from Postgres.dim_products
order by total_revenue desc
limit 20
```

<DataTable data={top_products} />
