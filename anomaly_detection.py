from google.cloud import bigquery
from sklearn.ensemble import IsolationForest

# Connect to BigQuery
client = bigquery.Client(project="psyched-myth-354703")

# Read daily revenue
query = """
SELECT date_id, revenue
FROM `psyched-myth-354703.opspulse360.kpi_sales_daily`
ORDER BY date_id
"""

df = client.query(query).result().to_dataframe()

# Train anomaly detection model
model = IsolationForest(
    contamination=0.05,
    random_state=42
)

model.fit(df[["revenue"]])

# Predict anomalies
df["anomaly"] = model.predict(df[["revenue"]])

# Convert model output into business-friendly labels
df["status"] = df["anomaly"].map({
    1: "NORMAL",
    -1: "ANOMALY"
})

# Show detected anomalies
anomalies = df[df["status"] == "ANOMALY"]
# Business recommendation for a low-revenue anomaly
recommendation = (
    "Investigate the low-value order mix on 2025-07-26 by reviewing "
    "product/category sales and promotions. If the pattern is confirmed, "
    "review promotional pricing or product mix to determine why AOV dropped sharply."
)

print()
print("Business Recommendation:")
print(recommendation)
print()
anomalies.to_csv("anomalies.csv", index=False)

print("Total days:", len(df))
print("Anomalous days:", len(anomalies))
print()
print(anomalies)
