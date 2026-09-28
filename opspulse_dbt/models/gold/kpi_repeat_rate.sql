{{ config(materialized='table') }}

WITH customer_orders AS (
    SELECT
        customer_id,
        COUNT(*) AS completed_orders
    FROM {{ ref('fact_orders') }}
    WHERE status = 'Completed'
    GROUP BY customer_id
)

SELECT
    COUNTIF(completed_orders >= 2) AS repeat_customers,
    COUNT(*) AS active_customers,
    SAFE_DIVIDE(
        COUNTIF(completed_orders >= 2),
        COUNT(*)
    ) * 100 AS repeat_rate_pct
FROM customer_orders