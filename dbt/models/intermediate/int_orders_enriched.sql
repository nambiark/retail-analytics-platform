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
    c.city                                        as customer_city,
    c.state                                       as customer_state,
    c.zip_code                                    as customer_zip_code,

    -- payment info (coalesce handles orders with no payment record)
    coalesce(p.total_payment_value, 0)            as total_payment_value,
    coalesce(p.payment_types_used, 0)             as payment_types_used,
    coalesce(p.max_installments, 0)               as max_installments,
    coalesce(p.payment_methods, 'none')           as payment_methods,

    -- items info
    coalesce(i.item_count, 0)                     as item_count,
    coalesce(i.total_items_price, 0)              as total_items_price,
    coalesce(i.total_freight_value, 0)            as total_freight_value,
    coalesce(i.total_order_value, 0)              as total_order_value,

    -- derived (null safe)
    case
        when o.delivered_at is not null
        then datediff('day', o.purchased_at, o.delivered_at)
    end                                           as days_to_deliver,
    case
        when o.delivered_at is not null
        and o.estimated_delivery_at is not null
        then datediff('day', o.delivered_at, o.estimated_delivery_at)
    end                                           as days_early_or_late

from orders o
left join customers c       using (customer_id)
left join payments p        using (order_id)
left join order_items i     using (order_id)
