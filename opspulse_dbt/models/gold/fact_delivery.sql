{{ config(materialized='table') }}

SELECT
    order_id,
    CAST(FORMAT_DATE('%Y%m%d', DATE(pickup_time)) AS INT64) AS date_id,
    partner,
    pickup_time,
    expected_delivery,
    actual_delivery,
    status
FROM {{ ref('silver_delivery') }}