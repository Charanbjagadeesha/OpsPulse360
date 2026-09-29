import json
from kafka import KafkaConsumer

consumer = KafkaConsumer(
    "orders",
    bootstrap_servers="localhost:9092",
    auto_offset_reset="earliest",
    group_id="opspulse360-processor",
    value_deserializer=lambda value: json.loads(value.decode("utf-8"))
)

print("Stream processor started...")

for message in consumer:
    event = message.value

    # Validate required fields
    required_fields = ["order_id", "customer_id", "product_id", "amount"]

    if not all(field in event for field in required_fields):
        print("Invalid event:", event)
        continue

    # Process the event
    amount = event["amount"]

    if amount >= 1000:
        amount_category = "HIGH_VALUE"
    else:
        amount_category = "NORMAL_VALUE"

    processed_event = {
        **event,
        "amount_category": amount_category
    }

    print("Processed event:")
    print(processed_event)
