import pandas as pd

# Load logs
with open("data/system_logs.txt", "r") as f:
    logs = f.readlines()

# Create DataFrame
df = pd.DataFrame(logs, columns=["raw_log"])

# Remove newline characters
df["raw_log"] = df["raw_log"].str.strip()

# Extract log level
df["level"] = df["raw_log"].str.extract("(INFO|WARNING|ERROR)")

# Extract message
df["message"] = df["raw_log"].str.replace(
    r".*(INFO|WARNING|ERROR)\s+", "", regex=True
)

# Convert severity to numbers
severity_map = {"INFO": 0, "WARNING": 1, "ERROR": 2}
df["severity"] = df["level"].map(severity_map)

# Create failure label (ERROR = 1, else 0)
df["failure"] = (df["level"] == "ERROR").astype(int)

# Rolling error count (last 3 logs)
df["error_count_3"] = df["failure"].rolling(window=3).sum()

# Drop NaN rows caused by rolling window
df = df.dropna()

print(df)
