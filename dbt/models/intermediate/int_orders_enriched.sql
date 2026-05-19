with orders as (
    select * from {{ ref('stg_orders') }}
),

customers as (
    select * from {{ ref('stg_customers') }}
),

payments as (
    select
        order_id,
        sum(payment_value)                    as total_payment_value,
        count(distinct payment_type)          as payment_types_used,
        max(payment_installments)             as max_installments,
        listagg(payment_type, ', ')           as payment_methods
    from {{ ref('stg_payments') }}
    group by order_id
),

order_items as (
    select
        order_id,
        count(order_item_id)                  as item_count,
        sum(price)                            as total_items_price,
        sum(freight_value)                    as total_freight_value,
        sum(price + freight_value)            as total_order_value
    from {{ ref('stg_order_items') }}
    group by order_id
)

select
    o.order_id,
    o.customer_id,
    o.order_status,
    o.purchased_at,
    o.approved_at,
    o.shipped_at,
    o.delivered_at,
    o.estimated_delivery_at,

    -- customer info
    c.customer_unique_id,
    c.city                                    as customer_city,
    c.state                                   as customer_state,
    c.zip_code                                as customer_zip_code,

    -- payment info
    p.total_payment_value,
    p.payment_types_used,
    p.max_installments,
    p.payment_methods,

    -- items info
    i.item_count,
    i.total_items_price,
    i.total_freight_value,
    i.total_order_value,

    -- derived
    datediff('day', o.purchased_at, o.delivered_at) as days_to_deliver,
    datediff('day', o.delivered_at, o.estimated_delivery_at) as days_early_or_late

from orders o
left join customers c       using (customer_id)
left join payments p        using (order_id)
left join order_items i     using (order_id)
