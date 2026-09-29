{{ config(materialized='table') }}

SELECT
    order_id,
    customer_id,
    product_id,
    warehouse_id,
    CAST(FORMAT_DATE('%Y%m%d', DATE(timestamp)) AS INT64) AS date_id,
    quantity,
    amount,
    status
FROM {{ ref('silver_orders') }}