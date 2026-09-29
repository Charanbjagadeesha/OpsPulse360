{{ config(materialized='view') }}

SELECT
    campaign_id,
    date,
    channel,
    spend,
    impressions,
    clicks,
    conversions
FROM `psyched-myth-354703.opspulse360.marketing`
