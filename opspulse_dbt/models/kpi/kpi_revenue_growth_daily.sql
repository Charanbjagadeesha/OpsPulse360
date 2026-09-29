{{ config(materialized='table') }}

WITH revenue_with_previous_day AS (
    SELECT
        date_id,
        revenue,
        LAG(revenue) OVER (ORDER BY date_id) AS previous_revenue
    FROM {{ ref('kpi_sales_daily') }}
)

SELECT
    date_id,
    revenue,
    previous_revenue,
    SAFE_DIVIDE(
        revenue - previous_revenue,
        previous_revenue
    ) * 100 AS growth_pct
FROM revenue_with_previous_day
ORDER BY date_id