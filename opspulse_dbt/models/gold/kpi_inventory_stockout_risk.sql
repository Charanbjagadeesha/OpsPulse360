{{ config(materialized='table') }}

SELECT
    warehouse_id,
    product_id,
    available_qty,
    reorder_level,
    CASE
        WHEN available_qty <= reorder_level THEN 'HIGH'
        ELSE 'LOW'
    END AS stockout_risk
FROM {{ ref('fact_inventory') }}
ORDER BY warehouse_id, product_id