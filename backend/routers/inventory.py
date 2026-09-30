from fastapi import APIRouter
from database import client

router = APIRouter(
    prefix="/api/inventory",
    tags=["Inventory"]
)


@router.get("/stockout-risk")
def get_stockout_risk():
    query = """
        SELECT
            stockout_risk,
            COUNT(*) AS product_count
        FROM `psyched-myth-354703.opspulse360.kpi_inventory_stockout_risk`
        GROUP BY stockout_risk
        ORDER BY stockout_risk
    """

    result = client.query(query).result()

    return [
        {
            "stockout_risk": row.stockout_risk,
            "product_count": row.product_count
        }
        for row in result
    ]
    return [
        {
            "stockout_risk": row.stockout_risk,
            "product_count": row.product_count
        }
        for row in result
    ]


@router.get("/turnover")
def get_inventory_turnover():
    query = """
        SELECT
            cogs,
            inventory_value,
            inventory_turnover
        FROM `psyched-myth-354703.opspulse360.kpi_inventory_turnover_monthly`
    """

    result = client.query(query).result()

    return [
        {
            "cogs": row.cogs,
            "inventory_value": row.inventory_value,
            "inventory_turnover": row.inventory_turnover
        }
        for row in result
    ]

@router.get("/days")
def get_inventory_days():
    query = """
        SELECT
            inventory_value,
            daily_cogs,
            days_of_inventory
        FROM `psyched-myth-354703.opspulse360.kpi_inventory_days`
    """

    result = client.query(query).result()

    return [
        {
            "inventory_value": row.inventory_value,
            "daily_cogs": row.daily_cogs,
            "days_of_inventory": row.days_of_inventory
        }
        for row in result
    ]

@router.get("/reorder")
def get_inventory_reorder():
    query = """
        SELECT
            warehouse_id,
            product_id,
            available_qty,
            reserved_qty,
            reorder_level,
            reorder_required,
            reorder_quantity
        FROM `psyched-myth-354703.opspulse360.kpi_inventory_reorder`
        ORDER BY reorder_required DESC, reorder_quantity DESC
    """

    result = client.query(query).result()

    return [
        {
            "warehouse_id": row.warehouse_id,
            "product_id": row.product_id,
            "available_qty": row.available_qty,
            "reserved_qty": row.reserved_qty,
            "reorder_level": row.reorder_level,
            "reorder_required": row.reorder_required,
            "reorder_quantity": row.reorder_quantity
        }
        for row in result
    ]
