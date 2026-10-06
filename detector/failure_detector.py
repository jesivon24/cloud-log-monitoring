def analyze_log(log_line):

    upper_line = log_line.upper()

    if "CRITICAL" in upper_line:
        return "CRITICAL"

    elif "ERROR" in upper_line:
        return "ERROR"

    elif "WARNING" in upper_line:
        return "WARNING"

    elif "INFO" in upper_line:
        return "INFO"

    # Detect failure keywords even when severity is not explicitly written
    elif any(word in upper_line for word in [
        "FAILED",
        "FAILURE",
        "UNAVAILABLE",
        "EXCEPTION",
        "TIMEOUT",
        "CRASH"
    ]):
        return "ERROR"

    return "UNKNOWN"


def detect_failure(log_line):

    severity = analyze_log(log_line)

    if severity in ["ERROR", "CRITICAL"]:
        return True

    return False