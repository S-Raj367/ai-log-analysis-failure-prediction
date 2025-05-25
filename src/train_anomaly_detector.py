import pandas as pd
from sklearn.ensemble import IsolationForest
import joblib

# Load logs
with open("data/system_logs.txt", "r") as f:
    logs = f.readlines()

df = pd.DataFrame(logs, columns=["raw_log"])
df["raw_log"] = df["raw_log"].str.strip()

# Extract level
df["level"] = df["raw_log"].str.extract("(INFO|WARNING|ERROR)")

# Severity encoding
severity_map = {"INFO": 0, "WARNING": 1, "ERROR": 2}
df["severity"] = df["level"].map(severity_map)

# Failure flag
df["failure"] = (df["level"] == "ERROR").astype(int)

# Rolling error count
df["error_count_3"] = df["failure"].rolling(window=3).sum()
df = df.dropna()

X = df[["severity", "error_count_3"]]

# Train Isolation Forest
iso = IsolationForest(
    n_estimators=100,
    contamination=0.2,
    random_state=42
)

iso.fit(X)

# Save model
joblib.dump(iso, "models/anomaly_detector.pkl")
print("Anomaly detector saved to models/anomaly_detector.pkl")
