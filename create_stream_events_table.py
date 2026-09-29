from google.cloud import bigquery

PROJECT_ID = "psyched-myth-354703"
TABLE_ID = f"{PROJECT_ID}.opspulse360.stream_events"

client = bigquery.Client(project=PROJECT_ID)

schema = [
    bigquery.SchemaField("event_type", "STRING"),
    bigquery.SchemaField("order_id", "INT64"),
    bigquery.SchemaField("customer_id", "INT64"),
    bigquery.SchemaField("product_id", "INT64"),
    bigquery.SchemaField("warehouse_id", "INT64"),
    bigquery.SchemaField("amount", "INT64"),
    bigquery.SchemaField("amount_category", "STRING"),
    bigquery.SchemaField("payment_status", "STRING"),
    bigquery.SchemaField("delivery_status", "STRING"),
    bigquery.SchemaField("sla_breach", "BOOL"),
    bigquery.SchemaField("available_qty", "INT64"),
    bigquery.SchemaField("stock_status", "STRING"),
]

table = bigquery.Table(TABLE_ID, schema=schema)

table = client.create_table(table)

print(f"Created table: {table.full_table_id}")
