{{ config(materialized='view') }}

SELECT
    ticket_id,
    customer_id,
    order_id,
    issue_type,
    priority,
    created_at,
    resolved_at
FROM `psyched-myth-354703.opspulse360.support`