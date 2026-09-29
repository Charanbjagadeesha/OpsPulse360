import json
from kafka import KafkaConsumer

OUTPUT_FILE = "processed_events.jsonl"

consumer = KafkaConsumer(
    "orders",
    bootstrap_servers="localhost:9092",
    auto_offset_reset="earliest",
    group_id="opspulse360-multi-event-processor",
    value_deserializer=lambda value: json.loads(value.decode("utf-8"))
)

print("Kafka stream processor started...")

for message in consumer:
    event = message.value
    event_type = event.get("event_type")

    if event_type == "order":
        required_fields = [
            "order_id",
            "customer_id",
            "product_id",
            "amount"
        ]

        if not all(field in event for field in required_fields):
            print("Invalid order event:", event)
            continue

        amount = int(event["amount"])

        processed_event = {
            "event_type": "order",
            "order_id": int(event["order_id"]),
            "customer_id": int(event["customer_id"]),
            "product_id": int(event["product_id"]),
            "amount": amount,
            "amount_category": (
                "HIGH_VALUE" if amount >= 1000 else "NORMAL_VALUE"
            )
        }

    elif event_type == "payment":
        processed_event = {
            "event_type": "payment",
            "order_id": int(event["order_id"]),
            "payment_status": event["payment_status"],
            "amount": int(event["amount"])
        }

    elif event_type == "delivery":
        processed_event = {
            "event_type": "delivery",
            "order_id": int(event["order_id"]),
            "delivery_status": event["delivery_status"],
            "sla_breach": event["delivery_status"] == "sla_breach"
        }

    elif event_type == "inventory":
        available_qty = int(event["available_qty"])

        processed_event = {
            "event_type": "inventory",
            "product_id": int(event["product_id"]),
            "warehouse_id": int(event["warehouse_id"]),
            "available_qty": available_qty,
            "stock_status": (
                "LOW_STOCK" if available_qty <= 20 else "NORMAL_STOCK"
            )
        }

    else:
        print("Unknown event type:", event)
        continue

    with open(OUTPUT_FILE, "a") as file:
        file.write(json.dumps(processed_event) + "\n")

    print("Processed:", processed_event)
