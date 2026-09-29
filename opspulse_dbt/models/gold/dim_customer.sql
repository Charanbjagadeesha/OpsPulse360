{{ config(materialized='table') }}

SELECT
    customer_id,
    city,
    state,
    segment,
    registration_date
FROM {{ ref('silver_customers') }}