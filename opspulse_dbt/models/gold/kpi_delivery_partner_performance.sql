{{ config(materialized='table') }}

SELECT
    partner,

    COUNT(*) AS total_deliveries,

    COUNTIF(
        actual_delivery <= expected_delivery
    ) AS on_time_deliveries,

    SAFE_DIVIDE(
        COUNTIF(actual_delivery <= expected_delivery),
        COUNT(*)
    ) * 100 AS on_time_pct,

    AVG(
        TIMESTAMP_DIFF(
            actual_delivery,
            pickup_time,
            HOUR
        )
    ) AS avg_delivery_time_hours

FROM {{ ref('fact_delivery') }}

WHERE pickup_time IS NOT NULL
  AND expected_delivery IS NOT NULL
  AND actual_delivery IS NOT NULL

GROUP BY partner
ORDER BY partner