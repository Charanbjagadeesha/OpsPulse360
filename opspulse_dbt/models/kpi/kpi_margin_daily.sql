{{ config(materialized='table') }}

SELECT
    o.date_id,
    SUM(o.amount - (o.quantity * p.cost)) AS margin
FROM {{ ref('fact_orders') }} AS o
JOIN {{ ref('dim_product') }} AS p
    ON o.product_id = p.product_id
WHERE o.status = 'Completed'
GROUP BY o.date_id
ORDER BY o.date_id