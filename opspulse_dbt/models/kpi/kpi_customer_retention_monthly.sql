{{ config(materialized='table') }}

WITH monthly_customers AS (
    SELECT DISTINCT
        customer_id,
        DATE_TRUNC(
            PARSE_DATE('%Y%m%d', CAST(date_id AS STRING)),
            MONTH
        ) AS order_month
    FROM {{ ref('fact_orders') }}
    WHERE status = 'Completed'
),

retention AS (
    SELECT
        curr.order_month,
        COUNT(DISTINCT curr.customer_id) AS current_month_customers,
        COUNT(DISTINCT next_month.customer_id) AS retained_customers
    FROM monthly_customers AS curr
    LEFT JOIN monthly_customers AS next_month
        ON curr.customer_id = next_month.customer_id
        AND next_month.order_month = DATE_ADD(
            curr.order_month,
            INTERVAL 1 MONTH
        )
    GROUP BY curr.order_month
)

SELECT
    order_month,
    current_month_customers,
    retained_customers,
    SAFE_DIVIDE(
        retained_customers,
        current_month_customers
    ) * 100 AS retention_rate_pct
FROM retention
ORDER BY order_month