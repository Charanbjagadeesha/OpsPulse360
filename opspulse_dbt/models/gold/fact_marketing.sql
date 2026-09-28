{{ config(materialized='table') }}

SELECT
    campaign_id,
    CAST(FORMAT_DATE('%Y%m%d', date) AS INT64) AS date_id,
    channel,
    spend,
    impressions,
    clicks,
    conversions
FROM {{ ref('silver_marketing') }}