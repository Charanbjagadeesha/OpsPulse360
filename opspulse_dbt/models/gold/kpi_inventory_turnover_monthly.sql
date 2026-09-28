{{ config(materialized='table') }}

WITH total_cogs AS (
    SELECT
        SUM(o.quantity * p.cost) AS cogs
    FROM {{ ref('fact_orders') }} AS o
    JOIN {{ ref('dim_product') }} AS p
        ON o.product_id = p.product_id
    WHERE o.status = 'Completed'
),

inventory_value AS (
    SELECT
        SUM(
            (i.available_qty + i.reserved_qty) * p.cost
        ) AS inventory_value
    FROM {{ ref('fact_inventory') }} AS i
    JOIN {{ ref('dim_product') }} AS p
        ON i.product_id = p.product_id
)

SELECT
    c.cogs,
    i.inventory_value,
    SAFE_DIVIDE(
        c.cogs,
        i.inventory_value
    ) AS inventory_turnover
FROM total_cogs AS c
CROSS JOIN inventory_value AS i