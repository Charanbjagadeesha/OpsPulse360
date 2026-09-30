from fastapi import APIRouter
from database import client

router = APIRouter(
    prefix="/api/delivery",
    tags=["Delivery"]
)


@router.get("/ontime")
def get_delivery_ontime():
    query = """
        SELECT
            total_deliveries,
            on_time_deliveries,
            on_time_pct
        FROM `psyched-myth-354703.opspulse360.kpi_delivery_ontime`
    """

    result = client.query(query).result()

    return [
        {
            "total_deliveries": row.total_deliveries,
            "on_time_deliveries": row.on_time_deliveries,
            "on_time_pct": row.on_time_pct
        }
        for row in result
    ]
@router.get("/average-time")
def get_delivery_average_time():
    query = """
        SELECT
            total_deliveries,
            avg_delivery_time_hours
        FROM `psyched-myth-354703.opspulse360.kpi_delivery_avg_time`
    """

    result = client.query(query).result()

    return [
        {
            "total_deliveries": row.total_deliveries,
            "avg_delivery_time_hours": row.avg_delivery_time_hours
        }
        for row in result
    ]
@router.get("/sla-breach")
def get_delivery_sla_breach():
    query = """
        SELECT
            total_deliveries,
            sla_breach_deliveries,
            sla_breach_pct
        FROM `psyched-myth-354703.opspulse360.kpi_delivery_sla_breach`
    """

    result = client.query(query).result()

    return [
        {
            "total_deliveries": row.total_deliveries,
            "sla_breach_deliveries": row.sla_breach_deliveries,
            "sla_breach_pct": row.sla_breach_pct
        }
        for row in result
    ]
@router.get("/partners")
def get_delivery_partner_performance():
    query = """
        SELECT
            partner,
            total_deliveries,
            on_time_deliveries,
            on_time_pct,
            avg_delivery_time_hours
        FROM `psyched-myth-354703.opspulse360.kpi_delivery_partner_performance`
        ORDER BY partner
    """

    result = client.query(query).result()

    return [
        {
            "partner": row.partner,
            "total_deliveries": row.total_deliveries,
            "on_time_deliveries": row.on_time_deliveries,
            "on_time_pct": row.on_time_pct,
            "avg_delivery_time_hours": row.avg_delivery_time_hours
        }
        for row in result
    ]
