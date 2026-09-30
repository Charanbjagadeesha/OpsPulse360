from google.cloud import bigquery
import pandas as pd
from sklearn.ensemble import RandomForestRegressor

# Connect to BigQuery
client = bigquery.Client(project="psyched-myth-354703")

# Read historical daily revenue
query = """
SELECT date_id, revenue
FROM `psyched-myth-354703.opspulse360.kpi_sales_daily`
ORDER BY date_id
"""

df = client.query(query).result().to_dataframe()

# Convert date_id into a real date
df["date"] = pd.to_datetime(df["date_id"].astype(str))

# Create lag features
df["lag_1"] = df["revenue"].shift(1)
df["lag_7"] = df["revenue"].shift(7)

# Remove rows without enough history
train = df.dropna().copy()

# Features and target
X = train[["lag_1", "lag_7"]]
y = train["revenue"]

# Train forecasting model
model = RandomForestRegressor(
    n_estimators=200,
    random_state=42
)

model.fit(X, y)
# Evaluate model using the last 30 historical days
test_size = 30

train_eval = train.iloc[:-test_size]
test_eval = train.iloc[-test_size:]

X_train_eval = train_eval[["lag_1", "lag_7"]]
y_train_eval = train_eval["revenue"]

X_test_eval = test_eval[["lag_1", "lag_7"]]
y_test_eval = test_eval["revenue"]

eval_model = RandomForestRegressor(
    n_estimators=200,
    random_state=42
)

eval_model.fit(X_train_eval, y_train_eval)

predictions = eval_model.predict(X_test_eval)

mae = abs(y_test_eval - predictions).mean()

print(f"Mean Absolute Error (MAE): ₹{mae:,.2f}")

# Forecast next 7 days
forecast_rows = []

history = df[["date", "revenue"]].copy()

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
        "date": next_date,
        "forecast_revenue": prediction
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

forecast = pd.DataFrame(forecast_rows)

# Save forecast
forecast.to_csv("sales_forecast.csv", index=False)

print("7-day sales forecast:")
print(forecast)
