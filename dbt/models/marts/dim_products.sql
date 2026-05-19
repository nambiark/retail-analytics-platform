{{
    config(
        materialized='table'
    )
}}

with products as (
    select * from {{ ref('stg_products') }}
),

translations as (
    select * from raw.category_translation
),

-- sales stats per product
product_sales as (
    select
        product_id,
        count(distinct order_id)            as total_orders,
        sum(price)                          as total_revenue,
        avg(price)                          as avg_price,
        sum(freight_value)                  as total_freight
    from {{ ref('int_order_items_enriched') }}
    group by product_id
)

select
    p.product_id,
    p.category_name_pt,
    coalesce(t.product_category_name, p.category_name_pt) as category_name_en,
    p.weight_g,
    p.length_cm,
    p.height_cm,
    p.width_cm,
    p.photos_qty,

    -- sales performance
    coalesce(s.total_orders, 0)             as total_orders,
    coalesce(s.total_revenue, 0)            as total_revenue,
    coalesce(s.avg_price, 0)               as avg_price,
    coalesce(s.total_freight, 0)           as total_freight,

    -- product tier by revenue
    case
        when s.total_revenue >= 10000       then 'high'
        when s.total_revenue >= 1000        then 'medium'
        else                                     'low'
    end                                     as revenue_tier

from products p
left join translations t    on p.category_name_pt = t.product_category_name
left join product_sales s   using (product_id)
