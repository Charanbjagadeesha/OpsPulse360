{{ config(materialized='view') }}

SELECT
    customer_id,
    city,
    state,
    segment,
    registration_date
FROM `psyched-myth-354703.opspulse360.customers`