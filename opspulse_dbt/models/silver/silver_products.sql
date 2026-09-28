{{ config(materialized='view') }}

SELECT
    product_id,
    category,
    brand,
    cost,
    selling_price,
    supplier_id
FROM `psyched-myth-354703.opspulse360.products`