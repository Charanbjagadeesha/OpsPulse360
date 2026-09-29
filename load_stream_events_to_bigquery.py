import json
from google.cloud import bigquery

PROJECT_ID = "psyched-myth-354703"
TABLE_ID = f"{PROJECT_ID}.opspulse360.stream_events"
INPUT_FILE = "processed_events.jsonl"

client = bigquery.Client(project=PROJECT_ID)

with open(INPUT_FILE, "r") as file:
    rows = [json.loads(line) for line in file if line.strip()]

job_config = bigquery.LoadJobConfig(
    schema=[
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
    ],
    write_disposition="WRITE_APPEND",
)

job = client.load_table_from_json(
    rows,
    TABLE_ID,
    job_config=job_config
)

job.result()

print(f"Loaded {len(rows)} events into BigQuery.")
