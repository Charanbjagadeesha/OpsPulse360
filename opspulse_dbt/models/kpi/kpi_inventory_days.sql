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
),

daily_cogs AS (
    SELECT
        cogs / 365 AS daily_cogs
    FROM total_cogs
)

SELECT
    i.inventory_value,
    c.daily_cogs,
    SAFE_DIVIDE(
        i.inventory_value,
        c.daily_cogs
    ) AS days_of_inventory
FROM inventory_value AS i
CROSS JOIN daily_cogs AS c