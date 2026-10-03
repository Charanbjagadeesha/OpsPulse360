import pandas as pd
from fastapi import APIRouter
from google.cloud import bigquery
from sklearn.ensemble import IsolationForest, RandomForestRegressor

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

    query = """
    SELECT date_id, revenue
    FROM `psyched-myth-354703.opspulse360.kpi_sales_daily`
    ORDER BY date_id
    """

    df = client.query(query).result().to_dataframe()

    if len(df) < 8:
        return {
            "status": "error",
            "message": "Not enough historical data for forecasting."
        }

    df["date"] = pd.to_datetime(df["date_id"].astype(str))

    df["lag_1"] = df["revenue"].shift(1)
    df["lag_7"] = df["revenue"].shift(7)

    train = df.dropna().copy()

    X = train[["lag_1", "lag_7"]]
    y = train["revenue"]

    model = RandomForestRegressor(
        n_estimators=200,
        random_state=42
    )

    model.fit(X, y)

    history = df[["date", "revenue"]].copy()

    forecast_rows = []

    for i in range(1, 8):

        last_date = history["date"].iloc[-1]
        next_date = last_date + pd.Timedelta(days=1)

        lag_1 = history["revenue"].iloc[-1]
        lag_7 = history["revenue"].iloc[-7]

        prediction_input = pd.DataFrame(
            [[lag_1, lag_7]],
            columns=["lag_1", "lag_7"]
        )

        prediction = model.predict(prediction_input)[0]

        forecast_rows.append({
            "date": next_date.strftime("%Y-%m-%d"),
            "forecast_revenue": float(prediction)
        })

        history = pd.concat(
            [
                history,
                pd.DataFrame({
                    "date": [next_date],
                    "revenue": [prediction]
                })
            ],
            ignore_index=True
        )

    return {
        "status": "success",
        "forecast_days": len(forecast_rows),
        "forecast": forecast_rows
    }
