from fastapi import APIRouter
from google.cloud import bigquery

router = APIRouter(
    prefix="/api/stream",
    tags=["Streaming"]
)

client = bigquery.Client(project="psyched-myth-354703")


@router.get("/events")
def get_stream_events():
    query = """
        SELECT
            event_type,
            order_id,
            customer_id,
            product_id,
            warehouse_id,
            amount,
            amount_category,
            payment_status,
            delivery_status,
            sla_breach,
            available_qty,
            stock_status
        FROM `psyched-myth-354703.opspulse360.stream_events`
        ORDER BY event_type
    """

    result = client.query(query).result()

    return [
        {
            "event_type": row.event_type,
            "order_id": row.order_id,
            "customer_id": row.customer_id,
            "product_id": row.product_id,
            "warehouse_id": row.warehouse_id,
            "amount": row.amount,
            "amount_category": row.amount_category,
            "payment_status": row.payment_status,
            "delivery_status": row.delivery_status,
            "sla_breach": row.sla_breach,
            "available_qty": row.available_qty,
            "stock_status": row.stock_status
        }
        for row in result
    ]
