{{
    config(
        materialized='table'
    )
}}

with customers as (
    select * from {{ ref('stg_customers') }}
),

-- count orders per customer for segmentation
order_counts as (
    select
        customer_unique_id,
        count(distinct order_id)            as total_orders,
        min(purchased_at)                   as first_order_at,
        max(purchased_at)                   as last_order_at,
        sum(total_payment_value)            as lifetime_value
    from {{ ref('int_orders_enriched') }}
    group by customer_unique_id
)

select
    c.customer_id,
    c.customer_unique_id,
    c.city,
    c.state,
    c.zip_code,
    coalesce(o.total_orders, 0)             as total_orders,
    o.first_order_at,
    o.last_order_at,
    coalesce(o.lifetime_value, 0)           as lifetime_value,

    -- segmentation
    case
        when o.total_orders >= 5            then 'vip'
        when o.total_orders >= 2            then 'repeat'
        when o.total_orders = 1             then 'one_time'
        else                                     'no_orders'
    end                                     as customer_segment

from customers c
left join order_counts o    using (customer_unique_id)
