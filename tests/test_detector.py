from detector.failure_detector import analyze_log, detect_failure


test_logs = [
    "2026-10-05 10:00:01 INFO Application started successfully",
    "2026-10-05 10:02:30 WARNING High memory usage detected",
    "2026-10-05 10:03:15 ERROR Database connection failed",
    "2026-10-05 10:05:10 CRITICAL Server unavailable"
]


for log in test_logs:

    severity = analyze_log(log)
    failure = detect_failure(log)

    print("--------------------------------")
    print("Log:", log)
    print("Severity:", severity)
    print("Failure:", failure)