{{ config(materialized='table') }}

SELECT
    warehouse_id,
    product_id,
    CAST(FORMAT_DATE('%Y%m%d', DATE(updated_at)) AS INT64) AS date_id,
    available_qty,
    reserved_qty,
    reorder_level,
    updated_at
FROM {{ ref('silver_inventory') }}