{{ config(materialized='table') }}

SELECT
    warehouse_id,
    product_id,
    available_qty,
    reserved_qty,
    reorder_level,
    CASE
        WHEN available_qty <= reorder_level THEN 'YES'
        ELSE 'NO'
    END AS reorder_required,
    CASE
        WHEN available_qty < reorder_level
            THEN reorder_level - available_qty
        ELSE 0
    END AS reorder_quantity
FROM {{ ref('fact_inventory') }}
ORDER BY warehouse_id, product_id