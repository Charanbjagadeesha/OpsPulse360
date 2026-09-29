{{ config(materialized='table') }}

SELECT
    date_id,
    COUNT(*) AS orders
FROM {{ ref('fact_orders') }}
GROUP BY date_id
ORDER BY date_id