from fastapi import APIRouter
from google.cloud import bigquery

router = APIRouter(
    prefix="/api/stream",
    tags=["Streaming"]
)

PROJECT_ID = "psyched-myth-354703"

client = bigquery.Client(project=PROJECT_ID)


@router.get("/events")
def get_stream_events():

    query = """
    SELECT
        order_id,
        customer_id,
        product_id,
        amount,
        amount_category
    FROM `psyched-myth-354703.opspulse360.stream_orders`
    ORDER BY order_id DESC
    LIMIT 100
    """

    rows = client.query(query).result()

    events = []

    for row in rows:
        events.append({
            "event_type": "order",
            "order_id": row.order_id,
            "customer_id": row.customer_id,
            "product_id": row.product_id,
            "amount": row.amount,
            "amount_category": row.amount_category
        })

    return events
