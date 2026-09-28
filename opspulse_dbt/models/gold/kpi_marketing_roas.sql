{{ config(materialized='table') }}

WITH marketing_spend AS (
    SELECT
        SUM(spend) AS total_spend
    FROM {{ ref('fact_marketing') }}
),

completed_revenue AS (
    SELECT
        SUM(amount) AS total_revenue
    FROM {{ ref('fact_orders') }}
    WHERE status = 'Completed'
)

SELECT
    r.total_revenue,
    m.total_spend,
    SAFE_DIVIDE(
        r.total_revenue,
        m.total_spend
    ) AS roas
FROM completed_revenue AS r
CROSS JOIN marketing_spend AS m