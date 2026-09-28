{{ config(materialized='table') }}

SELECT
    campaign_id,
    channel,
    SUM(spend) AS spend,
    SUM(conversions) AS conversions,
    SAFE_DIVIDE(
        SUM(spend),
        SUM(conversions)
    ) AS cac
FROM {{ ref('fact_marketing') }}
GROUP BY
    campaign_id,
    channel
ORDER BY campaign_id