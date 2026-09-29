{{ config(materialized='table') }}

WITH date_range AS (
    SELECT
        day AS date
    FROM UNNEST(
        GENERATE_DATE_ARRAY(
            (SELECT MIN(DATE(timestamp)) FROM {{ ref('silver_orders') }}),
            (SELECT MAX(DATE(timestamp)) FROM {{ ref('silver_orders') }})
        )
    ) AS day
)

SELECT
    CAST(FORMAT_DATE('%Y%m%d', date) AS INT64) AS date_id,
    date,
    EXTRACT(DAY FROM date) AS day,
    EXTRACT(MONTH FROM date) AS month,
    EXTRACT(QUARTER FROM date) AS quarter,
    EXTRACT(YEAR FROM date) AS year,
    FORMAT_DATE('%A', date) AS day_name
FROM date_range
ORDER BY date