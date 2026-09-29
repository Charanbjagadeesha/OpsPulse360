{{ config(materialized='view') }}

SELECT
    warehouse_id,
    product_id,
    available_qty,
    reserved_qty,
    reorder_level,
    updated_at
FROM `psyched-myth-354703.opspulse360.inventory`