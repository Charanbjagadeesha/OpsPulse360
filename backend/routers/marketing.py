from fastapi import APIRouter
from google.cloud import bigquery

from database import client, PROJECT_ID

router = APIRouter(prefix="/api/marketing", tags=["Marketing"])


@router.get("/ctr")
def marketing_ctr():
    query = f"""
        SELECT
            campaign_id,
            channel,
            impressions,
            clicks,
            ctr_pct
        FROM `{PROJECT_ID}.opspulse360.kpi_marketing_ctr`
        ORDER BY campaign_id
    """
    rows = client.query(query).result()

    return [
        {
            "campaign_id": row.campaign_id,
            "channel": row.channel,
            "impressions": row.impressions,
            "clicks": row.clicks,
            "ctr_pct": row.ctr_pct,
        }
        for row in rows
    ]


@router.get("/conversion-rate")
def marketing_conversion_rate():
    query = f"""
        SELECT *
        FROM `{PROJECT_ID}.opspulse360.kpi_marketing_conversion_rate`
        ORDER BY campaign_id
    """
    rows = client.query(query).result()

    return [dict(row.items()) for row in rows]


@router.get("/cac")
def marketing_cac():
    query = f"""
        SELECT *
        FROM `{PROJECT_ID}.opspulse360.kpi_marketing_cac`
        ORDER BY campaign_id
    """
    rows = client.query(query).result()

    return [dict(row.items()) for row in rows]


@router.get("/campaign-roi")
def marketing_campaign_roi():
    query = f"""
        SELECT *
        FROM `{PROJECT_ID}.opspulse360.kpi_marketing_campaign_roi`
    """
    rows = client.query(query).result()

    return [dict(row.items()) for row in rows]


@router.get("/roas")
def marketing_roas():
    query = f"""
        SELECT *
        FROM `{PROJECT_ID}.opspulse360.kpi_marketing_roas`
    """
    rows = client.query(query).result()

    return [dict(row.items()) for row in rows]
