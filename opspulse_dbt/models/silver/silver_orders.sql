{{ config(materialized='view') }}

SELECT
    order_id,
    customer_id,
    product_id,
    warehouse_id,
    timestamp,
    quantity,
    amount,
    status
FROM `psyched-myth-354703.opspulse360.orders`