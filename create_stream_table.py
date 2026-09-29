from google.cloud import bigquery

client = bigquery.Client(project="psyched-myth-354703")

table_id = "psyched-myth-354703.opspulse360.stream_orders"

schema = [
    bigquery.SchemaField("order_id", "INT64"),
    bigquery.SchemaField("customer_id", "INT64"),
    bigquery.SchemaField("product_id", "INT64"),
    bigquery.SchemaField("amount", "INT64"),
    bigquery.SchemaField("amount_category", "STRING"),
]

table = bigquery.Table(table_id, schema=schema)

table = client.create_table(table)

print(f"Created table: {table.full_table_id}")
