{{ config(materialized='view') }}

SELECT
    order_id,
    partner,
    pickup_time,
    expected_delivery,
    actual_delivery,
    status
FROM `psyched-myth-354703.opspulse360.delivery`