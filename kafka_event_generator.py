import json
import random
import time

from kafka import KafkaProducer


producer = KafkaProducer(
    bootstrap_servers="localhost:9092",
    value_serializer=lambda value: json.dumps(value).encode("utf-8")
)


event_types = ["order", "payment", "delivery", "inventory"]


def generate_event(event_number):
    event_type = random.choice(event_types)

    order_id = 10000 + event_number

    if event_type == "order":
        return {
            "event_type": "order",
            "order_id": order_id,
            "customer_id": random.randint(1, 10),
            "product_id": random.randint(1, 20),
            "amount": random.randint(200, 2000)
        }

    if event_type == "payment":
        return {
            "event_type": "payment",
            "order_id": order_id,
            "payment_status": random.choice(["success", "failed"]),
            "amount": random.randint(200, 2000)
        }

    if event_type == "delivery":
        return {
            "event_type": "delivery",
            "order_id": order_id,
            "delivery_status": random.choice(
                ["in_transit", "delivered", "sla_breach"]
            )
        }

    return {
        "event_type": "inventory",
        "product_id": random.randint(1, 20),
        "warehouse_id": random.randint(1, 8),
        "available_qty": random.randint(0, 100)
    }


print("OpsPulse 360 event generator started...")

i = 1

while True:
    event = generate_event(i)

    producer.send("orders", value=event)
    producer.flush()

    print("Sent:", event)

    i += 1
    time.sleep(1)
