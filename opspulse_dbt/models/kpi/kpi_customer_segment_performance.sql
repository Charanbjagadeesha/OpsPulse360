{{ config(materialized='table') }}

SELECT
    c.segment,
    COUNT(DISTINCT c.customer_id) AS customers,
    COUNT(o.order_id) AS orders,
    SUM(o.amount) AS revenue
FROM {{ ref('dim_customer') }} AS c
JOIN {{ ref('fact_orders') }} AS o
    ON c.customer_id = o.customer_id
WHERE o.status = 'Completed'
GROUP BY c.segment
ORDER BY revenue DESC