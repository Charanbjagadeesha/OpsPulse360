{{ config(materialized='table') }}

SELECT DISTINCT
    warehouse_id,
    CONCAT('Warehouse ', CAST(warehouse_id AS STRING)) AS warehouse_name
FROM {{ ref('silver_inventory') }}
ORDER BY warehouse_id