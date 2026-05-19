{{
    config(
        materialized='incremental',
        unique_key='order_id',
        on_schema_change='fail'
    )
}}

with orders as (
    select * from {{ ref('int_orders_enriched') }}

    {% if is_incremental() %}
        where purchased_at > (select max(purchased_at) from {{ this }})
    {% endif %}
),

items as (
    select
        order_id,
        count(order_item_id)                as item_count,
        listagg(distinct category_name_en, ', ') as categories
    from {{ ref('int_order_items_enriched') }}
    group by order_id
)

select
    o.order_id,
    o.customer_id,
    o.customer_unique_id,
    o.order_status,
    o.purchased_at,
    o.approved_at,
    o.shipped_at,
    o.delivered_at,
    o.estimated_delivery_at,
    o.customer_city,
    o.customer_state,
    o.total_payment_value,
    o.payment_methods,
    o.max_installments,
    o.total_freight_value,
    o.days_to_deliver,
    o.days_early_or_late,
    i.item_count,
    i.categories,

    -- date parts for easy BI filtering
    date_trunc('month', o.purchased_at)     as order_month,
    date_trunc('week', o.purchased_at)      as order_week,
    dayofweek(o.purchased_at)               as order_day_of_week,
    year(o.purchased_at)                    as order_year,

    -- flags
    o.order_status = 'delivered'            as is_delivered,
    o.days_to_deliver < 0                   as is_late

from orders o
left join items i using (order_id)
