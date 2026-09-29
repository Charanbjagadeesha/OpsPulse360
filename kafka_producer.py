import json
from kafka import KafkaProducer

producer = KafkaProducer(
    bootstrap_servers="localhost:9092",
    value_serializer=lambda value: json.dumps(value).encode("utf-8")
)

event = {
    "event_type": "order_created",
    "order_id": "ORD10001",
    "customer_id": "CUST001",
    "product_id": "PROD001",
    "quantity": 2,
    "amount": 5000
}

producer.send("orders", value=event)
producer.flush()

print("Order event sent successfully!")
