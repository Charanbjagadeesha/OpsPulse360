{{ config(materialized='table') }}

SELECT
    ticket_id,
    customer_id,
    order_id,
    CAST(FORMAT_DATE('%Y%m%d', DATE(created_at)) AS INT64) AS date_id,
    issue_type,
    priority,
    created_at,
    resolved_at
FROM {{ ref('silver_support') }}