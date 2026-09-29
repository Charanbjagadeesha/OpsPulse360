{{ config(materialized='table') }}

SELECT
    product_id,
    category,
    brand,
    cost,
    selling_price,
    supplier_id
FROM {{ ref('silver_products') }}