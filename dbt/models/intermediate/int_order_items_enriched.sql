with order_items as (
    select * from {{ ref('stg_order_items') }}
),

products as (
    select * from {{ ref('stg_products') }}
),

sellers as (
    select * from {{ ref('stg_sellers') }}
),

translations as (
    select * from raw.category_translation
)

select
    oi.order_id,
    oi.order_item_id,
    oi.product_id,
    oi.seller_id,
    oi.price,
    oi.freight_value,
    oi.price + oi.freight_value             as total_item_value,
    oi.shipping_limit_at,

    -- product info
    p.category_name_pt,
    coalesce(t.product_category_name, p.category_name_pt) as category_name_en,
    p.weight_g,
    p.length_cm,
    p.height_cm,
    p.width_cm,
    p.photos_qty,

    -- seller info
    s.city                                  as seller_city,
    s.state                                 as seller_state

from order_items oi
left join products p        using (product_id)
left join sellers s         using (seller_id)
left join translations t    on p.category_name_pt = t.product_category_name



