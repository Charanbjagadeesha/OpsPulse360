{{ config(materialized='table') }}

SELECT
    COUNT(*) AS total_deliveries,
    AVG(
        TIMESTAMP_DIFF(
            actual_delivery,
            pickup_time,
            HOUR
        )
    ) AS avg_delivery_time_hours
FROM {{ ref('fact_delivery') }}
WHERE pickup_time IS NOT NULL
  AND actual_delivery IS NOT NULL