import streamlit as st
import pandas as pd
import joblib

# =========================
# Load Models
# =========================
failure_model = joblib.load("models/failure_predictor.pkl")
anomaly_model = joblib.load("models/anomaly_detector.pkl")
time_ahead_model = joblib.load("models/time_ahead_failure_model.pkl")
tfidf_model = joblib.load("models/tfidf_failure_model.pkl")
tfidf_vectorizer = joblib.load("models/tfidf_vectorizer.pkl")

# =========================
# UI
# =========================
st.title("AI Log Intelligence & Failure Prediction System")
st.write("Unified dashboard for log analysis, failure prediction, anomaly detection, and incident explanation.")

st.divider()

# =========================
# Input Section
# =========================
severity_label = st.selectbox("Log Severity", ["INFO", "WARNING", "ERROR"])
severity_map = {"INFO": 0, "WARNING": 1, "ERROR": 2}
severity = severity_map[severity_label]

error_count_3 = st.slider(
    "Recent Error Count (last 3 logs)",
    min_value=0,
    max_value=3,
    value=1
)

log_message = st.text_input(
    "Log Message (for NLP analysis)",
    value="Database connection timeout"
)

input_df = pd.DataFrame(
    [[severity, error_count_3]],
    columns=["severity", "error_count_3"]
)

st.divider()

# =========================
# Predictions
# =========================
current_failure = failure_model.predict(input_df)[0]
future_failure = time_ahead_model.predict(pd.DataFrame([[severity]], columns=["severity"]))[0]
anomaly = anomaly_model.predict(input_df)[0]

tfidf_input = tfidf_vectorizer.transform([log_message])
tfidf_prediction = tfidf_model.predict(tfidf_input)[0]

# =========================
# Results Section
# =========================
st.subheader("Prediction Results")

# Current failure
if current_failure == 1:
    st.error("⚠️ Immediate Failure Risk Detected")
else:
    st.success("✅ No Immediate Failure Detected")

# Future failure
if future_failure == 1:
    st.warning("⏳ Failure Likely in the Next 30 Minutes")
else:
    st.info("🕒 No Near-Future Failure Expected")

# Anomaly detection
if anomaly == -1:
    st.warning("🚨 Anomalous Log Behavior Detected")
else:
    st.info("ℹ️ Log Pattern Appears Normal")

# NLP-based prediction
if tfidf_prediction == 1:
    st.warning("🧠 Log Message Indicates Failure-Related Pattern")
else:
    st.success("🧠 Log Message Appears Benign")

st.divider()

# =========================
# Auto-Generated Incident Summary
# =========================
st.subheader("📝 Auto-Generated Incident Summary")

summary = []

if anomaly == -1:
    summary.append("Unusual log behavior detected.")

if current_failure == 1:
    summary.append("System currently at risk of failure.")

if future_failure == 1:
    summary.append("High probability of failure within 30 minutes.")

if tfidf_prediction == 1:
    summary.append("Log message semantics resemble past failure incidents.")

if not summary:
    summary.append("System operating within normal parameters.")

for line in summary:
    st.write("•", line)
