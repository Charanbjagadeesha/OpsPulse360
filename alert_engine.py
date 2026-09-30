import json
import os
import requests
from datetime import datetime

from google.cloud import bigquery


PROJECT_ID = "psyched-myth-354703"

client = bigquery.Client(project=PROJECT_ID)


def run_query(query):
    return list(client.query(query).result())


# ---------------------------------------------------------
# RULE 1: INVENTORY ALERT
# ---------------------------------------------------------

def inventory_alert():

    query = """
    SELECT
        COUNTIF(stockout_risk = 'HIGH') AS high_risk
    FROM `psyched-myth-354703.opspulse360.kpi_inventory_stockout_risk`
    """

    row = run_query(query)[0]

    high_risk = int(row.high_risk or 0)

    if high_risk > 0:

        return {
            "type": "inventory",
            "severity": "HIGH",
            "message": (
                f"{high_risk} products have high stockout risk."
            )
        }

    return None


# ---------------------------------------------------------
# RULE 2: DELIVERY SLA ALERT
# ---------------------------------------------------------

def delivery_alert():

    query = """
    SELECT
        sla_breach_pct
    FROM `psyched-myth-354703.opspulse360.kpi_delivery_sla_breach`
    """

    row = run_query(query)[0]

    breach_rate = float(row.sla_breach_pct or 0)

    threshold = 30

    if breach_rate > threshold:

        return {
            "type": "delivery",
            "severity": "HIGH",
            "message": (
                f"Delivery SLA breach rate is "
                f"{breach_rate:.2f}%, "
                f"above the {threshold}% threshold."
            )
        }

    return None


# ---------------------------------------------------------
# RULE 3: REVENUE ANOMALY ALERT
# ---------------------------------------------------------

def revenue_anomaly_alert():

    try:

        with open("anomalies.csv", "r") as file:
            lines = file.readlines()

        anomaly_count = max(len(lines) - 1, 0)

    except FileNotFoundError:

        anomaly_count = 0

    if anomaly_count > 0:

        return {
            "type": "revenue_anomaly",
            "severity": "HIGH",
            "message": (
                f"{anomaly_count} revenue anomalies detected "
                "by the ML anomaly detection workflow."
            )
        }

    return None


# ---------------------------------------------------------
# RULE 4: PAYMENT FAILURE ALERT
# ---------------------------------------------------------

def payment_failure_alert():

    query = """
    SELECT
        COUNTIF(payment_status = 'failed') AS failed,
        COUNT(*) AS total
    FROM `psyched-myth-354703.opspulse360.stream_events`
    WHERE event_type = 'payment'
    """

    row = run_query(query)[0]

    failed = int(row.failed or 0)

    total = int(row.total or 0)

    failure_rate = (
        failed / total * 100
        if total
        else 0
    )

    threshold = 20

    if failure_rate > threshold:

        return {
            "type": "payment_failure",
            "severity": "HIGH",
            "message": (
                f"Payment failure rate is "
                f"{failure_rate:.2f}%, "
                f"above the {threshold}% threshold."
            )
        }

    return None


# ---------------------------------------------------------
# SLACK NOTIFICATION
# ---------------------------------------------------------

def send_slack_notification(alerts):

    webhook_url = os.getenv("SLACK_WEBHOOK_URL")

    if not webhook_url:

        print("Slack webhook not configured.")

        return

    if not alerts:

        print("No alerts to send.")

        return

    message = (
        "*OpsPulse 360 Alert Notification*\n\n"
    )

    for alert in alerts:

        message += (
            f"*{alert['severity']}* | "
            f"{alert['type']}\n"
            f"{alert['message']}\n\n"
        )

    response = requests.post(
        webhook_url,
        json={
            "text": message
        },
        timeout=10
    )

    response.raise_for_status()

    print(
        "Slack notification sent successfully!"
    )


# ---------------------------------------------------------
# ALERT ENGINE
# ---------------------------------------------------------

def run_alert_engine():

    alerts = []

    rules = [
        inventory_alert,
        delivery_alert,
        revenue_anomaly_alert,
        payment_failure_alert,
    ]

    for rule in rules:

        try:

            alert = rule()

            if alert:

                alerts.append(alert)

        except Exception as error:

            alerts.append(
                {
                    "type": "system",
                    "severity": "HIGH",
                    "message": (
                        f"Alert rule failed: {str(error)}"
                    )
                }
            )

    result = {
        "generated_at": datetime.now().isoformat(),
        "alert_count": len(alerts),
        "alerts": alerts,
    }

    # Save alert results
    with open("alerts.json", "w") as file:

        json.dump(
            result,
            file,
            indent=2
        )

    # Display results
    print(
        json.dumps(
            result,
            indent=2
        )
    )

    # Send notification
    send_slack_notification(alerts)


# ---------------------------------------------------------
# START PROGRAM
# ---------------------------------------------------------

if __name__ == "__main__":

    run_alert_engine()
