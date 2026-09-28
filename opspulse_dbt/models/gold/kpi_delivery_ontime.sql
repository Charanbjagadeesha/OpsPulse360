{{ config(materialized='table') }}

SELECT
    COUNT(*) AS total_deliveries,
    COUNTIF(actual_delivery <= expected_delivery) AS on_time_deliveries,
    SAFE_DIVIDE(
        COUNTIF(actual_delivery <= expected_delivery),
        COUNT(*)
    ) * 100 AS on_time_pct
FROM {{ ref('fact_delivery') }}
WHERE actual_delivery IS NOT NULL
  AND expected_delivery IS NOT NULL