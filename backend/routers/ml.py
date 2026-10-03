from fastapi import APIRouter
from google.cloud import bigquery
from sklearn.ensemble import IsolationForest

router = APIRouter(prefix="/api/ml", tags=["Machine Learning"])

PROJECT_ID = "psyched-myth-354703"

client = bigquery.Client(project=PROJECT_ID)


@router.get("/anomalies")
def get_anomalies():

    query = """
    SELECT date_id, revenue
    FROM `psyched-myth-354703.opspulse360.kpi_sales_daily`
    ORDER BY date_id
    """

    df = client.query(query).result().to_dataframe()

    if df.empty:
        return {
            "status": "success",
            "anomaly_count": 0,
            "anomalies": []
        }

    model = IsolationForest(
        contamination=0.05,
        random_state=42
    )

    model.fit(df[["revenue"]])

    df["anomaly"] = model.predict(df[["revenue"]])

    df["status"] = df["anomaly"].map({
        1: "NORMAL",
        -1: "ANOMALY"
    })

    anomalies = df[df["status"] == "ANOMALY"]

    return {
        "status": "success",
        "anomaly_count": len(anomalies),
        "anomalies": anomalies.to_dict(orient="records")
    }


@router.get("/forecast")
def get_forecast():
    return {
        "status": "success",
        "forecast_days": 0,
        "forecast": []
    }
