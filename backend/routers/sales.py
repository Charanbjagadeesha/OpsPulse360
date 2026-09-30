from fastapi import APIRouter
from database import client

router = APIRouter(
    prefix="/api/sales",
    tags=["Sales"]
)


@router.get("/revenue")
def get_revenue():
    query = """
        SELECT SUM(revenue) AS total_revenue
        FROM `psyched-myth-354703.opspulse360.kpi_sales_daily`
    """

    result = client.query(query).result()
    row = next(result)

    return {
        "metric": "revenue",
        "value": row.total_revenue
    }
@router.get("/orders")
def get_orders():
    query = """
        SELECT SUM(orders) AS total_orders
        FROM `psyched-myth-354703.opspulse360.kpi_orders_daily`
    """

    result = client.query(query).result()
    row = next(result)

    return {
        "metric": "orders",
        "value": row.total_orders
    }
@router.get("/aov")
def get_aov():
    query = """
        SELECT AVG(aov) AS average_order_value
        FROM `psyched-myth-354703.opspulse360.kpi_aov_daily`
    """

    result = client.query(query).result()
    row = next(result)

    return {
        "metric": "aov",
        "value": row.average_order_value
    }
@router.get("/units")
def get_units():
    query = """
        SELECT SUM(units) AS total_units
        FROM `psyched-myth-354703.opspulse360.kpi_units_daily`
    """

    result = client.query(query).result()
    row = next(result)

    return {
        "metric": "units",
        "value": row.total_units
    }
@router.get("/margin")
def get_margin():
    query = """
        SELECT SUM(margin) AS total_margin
        FROM `psyched-myth-354703.opspulse360.kpi_margin_daily`
    """

    result = client.query(query).result()
    row = next(result)

    return {
        "metric": "margin",
        "value": row.total_margin
    }
@router.get("/growth")
def get_revenue_growth():
    query = """
        SELECT
            date_id,
            revenue,
            previous_revenue,
            growth_pct
        FROM `psyched-myth-354703.opspulse360.kpi_revenue_growth_daily`
        ORDER BY date_id DESC
        LIMIT 1
    """

    result = client.query(query).result()
    row = next(result)

    return {
        "metric": "revenue_growth",
        "date_id": row.date_id,
        "revenue": row.revenue,
        "previous_revenue": row.previous_revenue,
        "growth_pct": row.growth_pct
    }
