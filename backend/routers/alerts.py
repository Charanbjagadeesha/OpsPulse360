from fastapi import APIRouter
from database import client

router = APIRouter(
    prefix="/api/alerts",
    tags=["Alerts"]
)


@router.get("")
def get_alerts():
    alerts = []

    # Inventory stockout alerts
    inventory_query = """
        SELECT
            stockout_risk,
            COUNT(*) AS product_count
        FROM `psyched-myth-354703.opspulse360.kpi_inventory_stockout_risk`
        GROUP BY stockout_risk
    """

    inventory_result = client.query(inventory_query).result()

    for row in inventory_result:
        if row.stockout_risk == "HIGH":
            alerts.append({
                "type": "inventory",
                "severity": "HIGH",
                "message": f"{row.product_count} products have high stockout risk"
            })

    # Delivery SLA alert
    delivery_query = """
        SELECT
            sla_breach_deliveries,
            sla_breach_pct
        FROM `psyched-myth-354703.opspulse360.kpi_delivery_sla_breach`
    """

    delivery_result = client.query(delivery_query).result()

    for row in delivery_result:
        if row.sla_breach_pct > 30:
            alerts.append({
                "type": "delivery",
                "severity": "HIGH",
                "message": f"{row.sla_breach_deliveries} deliveries breached SLA ({row.sla_breach_pct:.2f}%)"
            })

    return {
        "alert_count": len(alerts),
        "alerts": alerts
    }
