from datetime import datetime
from pathlib import Path

from airflow.sdk import DAG
from airflow.providers.standard.operators.python import PythonOperator


SOURCE_DIR = Path("/mnt/c/OpsPulse360/data/source")
DBT_PROJECT_DIR = Path("/mnt/c/OpsPulse360/opspulse_dbt")
DBT_EXECUTABLE = "/home/hp_v/dbt-venv/bin/dbt"

REQUIRED_FILES = [
    "customers.csv",
    "products.csv",
    "orders.csv",
    "inventory.csv",
    "delivery.csv",
    "support.csv",
    "marketing.csv",
]


def validate_source_files():
    missing_files = [
        filename
        for filename in REQUIRED_FILES
        if not (SOURCE_DIR / filename).exists()
    ]

    if missing_files:
        raise FileNotFoundError(
            f"Missing source files: {', '.join(missing_files)}"
        )

    print("All required source files are present.")

def validate_data():
    import pandas as pd

    required_columns = {
        "customers.csv": [
            "customer_id",
            "city",
            "state",
            "segment",
            "registration_date",
        ],
        "products.csv": [
            "product_id",
            "category",
            "brand",
            "cost",
            "selling_price",
            "supplier_id",
        ],
        "orders.csv": [
            "order_id",
            "customer_id",
            "product_id",
            "warehouse_id",
            "timestamp",
            "quantity",
            "status",
            "amount",
        ],
        "inventory.csv": [
            "warehouse_id",
            "product_id",
            "available_qty",
            "reserved_qty",
            "reorder_level",
            "updated_at",
        ],
        "delivery.csv": [
            "order_id",
            "partner",
            "pickup_time",
            "expected_delivery",
            "actual_delivery",
            "status",
        ],
        "support.csv": [
            "ticket_id",
            "customer_id",
            "order_id",
            "issue_type",
            "priority",
            "created_at",
            "resolved_at",
        ],
        "marketing.csv": [
            "campaign_id",
            "date",
            "channel",
            "spend",
            "impressions",
            "clicks",
            "conversions",
        ],
    }

    for filename, expected_columns in required_columns.items():
        file_path = SOURCE_DIR / filename
        df = pd.read_csv(file_path)

        if df.empty:
            raise ValueError(f"{filename} is empty.")

        missing_columns = [
            column
            for column in expected_columns
            if column not in df.columns
        ]

        if missing_columns:
            raise ValueError(
                f"{filename} is missing columns: "
                f"{', '.join(missing_columns)}"
            )

    print("All source data validation checks passed.")

def run_dbt_silver():
    import subprocess

    command = [
        DBT_EXECUTABLE,
        "run",
        "--select",
        "path:models/silver",
    ]

    result = subprocess.run(
        command,
        cwd=DBT_PROJECT_DIR,
        capture_output=False,
        text=True,
    )

    if result.returncode != 0:
        raise RuntimeError("dbt Silver run failed.")

    print("dbt Silver run completed successfully.")


def run_dbt_gold():
    import subprocess

    command = [
        DBT_EXECUTABLE,
        "run",
        "--select",
        "path:models/gold",
    ]

    result = subprocess.run(
        command,
        cwd=DBT_PROJECT_DIR,
        capture_output=False,
        text=True,
    )

    if result.returncode != 0:
        raise RuntimeError("dbt Gold run failed.")

    print("dbt Gold run completed successfully.")
def run_dbt_kpi():
    import subprocess

    command = [
        DBT_EXECUTABLE,
        "run",
        "--select",
        "path:models/kpi",
    ]

    result = subprocess.run(
        command,
        cwd=DBT_PROJECT_DIR,
        capture_output=False,
        text=True,
    )

    if result.returncode != 0:
        raise RuntimeError("dbt KPI run failed.")

    print("dbt KPI run completed successfully.")


with DAG(
    dag_id="opspulse360_pipeline",
    start_date=datetime(2026, 9, 28),
    schedule=None,
    catchup=False,
    tags=["opspulse360"],
) as dag:

    validate_source = PythonOperator(
        task_id="validate_source",
        python_callable=validate_source_files,
    )

    validate_data_task = PythonOperator(
        task_id="validate_data",
        python_callable=validate_data,
    )


    dbt_silver = PythonOperator(
        task_id="dbt_silver",
        python_callable=run_dbt_silver,
    )

    dbt_gold = PythonOperator(
        task_id="dbt_gold",
        python_callable=run_dbt_gold,
    )

    dbt_kpi = PythonOperator(
        task_id="dbt_kpi",
        python_callable=run_dbt_kpi,
    )

    validate_source >> validate_data_task >> dbt_silver >> dbt_gold >> dbt_kpi
