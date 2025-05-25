# AI Log Intelligence & Failure Prediction System

## Overview
An end-to-end AI system that analyzes system/application logs to detect anomalies, predict failures, and provide early warnings.  
The project integrates machine learning, NLP (TF-IDF), anomaly detection, and time-ahead prediction, deployed via an interactive Streamlit dashboard.

---

## Features
- Log parsing and feature engineering  
- Failure prediction using Logistic Regression  
- 30-minute ahead failure prediction  
- Anomaly detection using Isolation Forest  
- NLP-based log message analysis (TF-IDF)  
- Auto-generated incident summary  
- Interactive Streamlit dashboard  

---

## System Architecture
Raw Logs
↓
Log Parsing & Cleaning
↓
Feature Engineering (Severity, Error Counts, TF-IDF)
↓
ML Models
├─ Failure Prediction
├─ Time-Ahead Prediction
├─ Anomaly Detection
└─ NLP-Based Prediction
↓
Decision Layer & Incident Summary
↓
Streamlit Dashboard

---

## Models Used
| Task | Model |
|-----|------|
| Failure prediction | Logistic Regression |
| 30-min ahead prediction | Logistic Regression |
| Anomaly detection | Isolation Forest |
| Log text analysis | TF-IDF + Logistic Regression |

---

## Tech Stack
- Python  
- pandas, scikit-learn  
- TF-IDF (NLP)  
- Streamlit  
- Git & GitHub  

---

## How to Run
```bash
pip install -r requirements.txt
streamlit run dashboard/app.py
