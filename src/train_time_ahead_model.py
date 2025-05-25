import pandas as pd
from sklearn.linear_model import LogisticRegression
from sklearn.model_selection import train_test_split
import joblib

# Load logs
with open("data/system_logs.txt", "r") as f:
    logs = f.readlines()

df = pd.DataFrame(logs, columns=["raw_log"])
df["raw_log"] = df["raw_log"].str.strip()

df["level"] = df["raw_log"].str.extract("(INFO|WARNING|ERROR)")
df["severity"] = df["level"].map({"INFO": 0, "WARNING": 1, "ERROR": 2})
df["failure"] = (df["level"] == "ERROR").astype(int)

# Predict failure 2 logs ahead (proxy for ~30 min)
df["future_failure"] = df["failure"].shift(-2)
df = df.dropna()

X = df[["severity"]]
y = df["future_failure"]

X_train, X_test, y_train, y_test = train_test_split(
    X, y, test_size=0.3, random_state=42
)

model = LogisticRegression()
model.fit(X_train, y_train)

joblib.dump(model, "models/time_ahead_failure_model.pkl")
print("30-min ahead prediction model saved")
