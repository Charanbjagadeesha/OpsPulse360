from fastapi import APIRouter
from database import client

router = APIRouter(
    prefix="/api/customers",
    tags=["Customers"]
)
@router.get("/new")
def get_new_customers():
    query = """
        SELECT SUM(new_customers) AS total_new_customers
        FROM `psyched-myth-354703.opspulse360.kpi_new_customers_daily`
    """

    result = client.query(query).result()
    row = next(result)

    return {
        "metric": "new_customers",
        "value": row.total_new_customers
    }
@router.get("/repeat-rate")
def get_repeat_rate():
    query = """
        SELECT
            repeat_customers,
            active_customers,
            repeat_rate_pct
        FROM `psyched-myth-354703.opspulse360.kpi_repeat_rate`
    """

    result = client.query(query).result()
    row = next(result)

    return {
        "metric": "repeat_rate",
        "repeat_customers": row.repeat_customers,
        "active_customers": row.active_customers,
        "repeat_rate_pct": row.repeat_rate_pct
    }
@router.get("/retention")
def get_customer_retention():
    query = """
        SELECT
            order_month,
            current_month_customers,
            retained_customers,
            retention_rate_pct
        FROM `psyched-myth-354703.opspulse360.kpi_customer_retention_monthly`
        ORDER BY order_month
    """

    result = client.query(query).result()

    return [
        {
            "order_month": row.order_month,
            "current_month_customers": row.current_month_customers,
            "retained_customers": row.retained_customers,
            "retention_rate_pct": row.retention_rate_pct
        }
        for row in result
    ]
@router.get("/segments")
def get_customer_segments():
    query = """
        SELECT
            segment,
            customers,
            orders,
            revenue
        FROM `psyched-myth-354703.opspulse360.kpi_customer_segment_performance`
        ORDER BY segment
    """

    result = client.query(query).result()

    return [
        {
            "segment": row.segment,
            "customers": row.customers,
            "orders": row.orders,
            "revenue": row.revenue
        }
        for row in result
    ]
