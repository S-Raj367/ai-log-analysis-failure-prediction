import pandas as pd
from sklearn.model_selection import train_test_split
from sklearn.linear_model import LogisticRegression
from sklearn.metrics import classification_report
import joblib

# Load processed data
with open("data/system_logs.txt", "r") as f:
    logs = f.readlines()

df = pd.DataFrame(logs, columns=["raw_log"])
df["raw_log"] = df["raw_log"].str.strip()

df["level"] = df["raw_log"].str.extract("(INFO|WARNING|ERROR)")
df["message"] = df["raw_log"].str.replace(
    r".*(INFO|WARNING|ERROR)\s+", "", regex=True
)

severity_map = {"INFO": 0, "WARNING": 1, "ERROR": 2}
df["severity"] = df["level"].map(severity_map)
df["failure"] = (df["level"] == "ERROR").astype(int)
df["error_count_3"] = df["failure"].rolling(window=3).sum()
df = df.dropna()

# Features and target
X = df[["severity", "error_count_3"]]
y = df["failure"]

# Train-test split
X_train, X_test, y_train, y_test = train_test_split(
    X, y, test_size=0.3, random_state=42
)

# Train model
model = LogisticRegression()
model.fit(X_train, y_train)

# Evaluate
y_pred = model.predict(X_test)
print(classification_report(y_test, y_pred))

# Save model
joblib.dump(model, "models/failure_predictor.pkl")
print("Model saved to models/failure_predictor.pkl")
