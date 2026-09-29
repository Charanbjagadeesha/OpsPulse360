{{ config(materialized='table') }}

SELECT
    campaign_id,
    channel,
    SUM(clicks) AS clicks,
    SUM(conversions) AS conversions,
    SAFE_DIVIDE(
        SUM(conversions),
        SUM(clicks)
    ) * 100 AS conversion_rate_pct
FROM {{ ref('fact_marketing') }}
GROUP BY
    campaign_id,
    channel
ORDER BY campaign_id