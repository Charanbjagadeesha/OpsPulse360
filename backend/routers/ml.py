from fastapi import APIRouter
import pandas as pd
from pathlib import Path

router = APIRouter(prefix="/api/ml", tags=["Machine Learning"])

PROJECT_DIR = Path("/mnt/c/OpsPulse360")


@router.get("/anomalies")
def get_anomalies():
    file_path = PROJECT_DIR / "anomalies.csv"

    if not file_path.exists():
        return {
            "status": "error",
            "message": "Anomaly results are not available."
        }

    df = pd.read_csv(file_path)

    return {
        "status": "success",
        "anomaly_count": len(df),
        "anomalies": df.to_dict(orient="records")
    }


@router.get("/forecast")
def get_forecast():
    file_path = PROJECT_DIR / "sales_forecast.csv"

    if not file_path.exists():
        return {
            "status": "error",
            "message": "Forecast results are not available."
        }

    df = pd.read_csv(file_path)

    return {
        "status": "success",
        "forecast_days": len(df),
        "forecast": df.to_dict(orient="records")
    }
