import pandas as pd
from sklearn.feature_extraction.text import TfidfVectorizer
from sklearn.linear_model import LogisticRegression
from sklearn.model_selection import train_test_split
from sklearn.metrics import classification_report
import joblib

# Load logs
with open("data/system_logs.txt", "r") as f:
    logs = f.readlines()

df = pd.DataFrame(logs, columns=["raw_log"])
df["raw_log"] = df["raw_log"].str.strip()

df["level"] = df["raw_log"].str.extract("(INFO|WARNING|ERROR)")
df["message"] = df["raw_log"].str.replace(
    r".*(INFO|WARNING|ERROR)\s+", "", regex=True
)

# Label
df["failure"] = (df["level"] == "ERROR").astype(int)

# TF-IDF
vectorizer = TfidfVectorizer(stop_words="english")
X = vectorizer.fit_transform(df["message"])
y = df["failure"]

# Train
X_train, X_test, y_train, y_test = train_test_split(
    X, y, test_size=0.3, random_state=42
)

model = LogisticRegression()
model.fit(X_train, y_train)

# Evaluate
print(classification_report(y_test, model.predict(X_test)))

# Save
joblib.dump(model, "models/tfidf_failure_model.pkl")
joblib.dump(vectorizer, "models/tfidf_vectorizer.pkl")

print("TF-IDF model and vectorizer saved")
