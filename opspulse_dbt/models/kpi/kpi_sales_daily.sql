{{ config(materialized='table') }}

SELECT
    date_id,
    SUM(amount) AS revenue
FROM {{ ref('fact_orders') }}
WHERE status = 'Completed'
GROUP BY date_id
ORDER BY date_id