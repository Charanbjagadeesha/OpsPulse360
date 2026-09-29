{{ config(materialized='table') }}

SELECT
    campaign_id,
    channel,
    SUM(impressions) AS impressions,
    SUM(clicks) AS clicks,
    SAFE_DIVIDE(
        SUM(clicks),
        SUM(impressions)
    ) * 100 AS ctr_pct
FROM {{ ref('fact_marketing') }}
GROUP BY
    campaign_id,
    channel
ORDER BY campaign_id