def generate_summary(logs):
    error_logs = [log for log in logs if "ERROR" in log]
    warning_logs = [log for log in logs if "WARNING" in log]

    summary = []

    if error_logs:
        summary.append(f"{len(error_logs)} errors detected.")
        summary.append(f"Most recent error: {error_logs[-1]}")

    if warning_logs:
        summary.append(f"{len(warning_logs)} warnings detected.")

    if not summary:
        summary.append("System operating normally.")

    return " ".join(summary)


# Example usage
if __name__ == "__main__":
    with open("data/system_logs.txt", "r") as f:
        logs = f.readlines()

    print(generate_summary(logs))
