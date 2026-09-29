{{ config(materialized='table') }}

WITH first_completed_order AS (
    SELECT
        customer_id,
        MIN(date_id) AS first_order_date_id
    FROM {{ ref('fact_orders') }}
    WHERE status = 'Completed'
    GROUP BY customer_id
)

SELECT
    first_order_date_id AS date_id,
    COUNT(*) AS new_customers
FROM first_completed_order
GROUP BY first_order_date_id
ORDER BY first_order_date_id