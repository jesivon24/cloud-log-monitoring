from flask import Flask, render_template, jsonify, request
import sqlite3
from datetime import datetime

from detector.failure_detector import analyze_log, detect_failure


app = Flask(__name__)

DATABASE = "database/logs.db"
LOG_FILE = "logs/sample.log"


# -----------------------------------------
# Initialize Database
# -----------------------------------------

def init_database():

    conn = sqlite3.connect(DATABASE)

    cursor = conn.cursor()

    cursor.execute("""
        CREATE TABLE IF NOT EXISTS logs (
            id INTEGER PRIMARY KEY AUTOINCREMENT,
            timestamp TEXT,
            level TEXT,
            message TEXT,
            failure INTEGER
        )
    """)

    conn.commit()
    conn.close()


# -----------------------------------------
# Process Sample Logs
# -----------------------------------------

def process_logs():

    conn = sqlite3.connect(DATABASE)

    cursor = conn.cursor()

    cursor.execute("DELETE FROM logs")

    with open(LOG_FILE, "r") as file:

        for line in file:

            line = line.strip()

            if not line:
                continue

            parts = line.split(" ", 3)

            timestamp = parts[0] + " " + parts[1]
            level = parts[2]
            message = parts[3]

            failure = detect_failure(line)

            cursor.execute("""
                INSERT INTO logs
                (timestamp, level, message, failure)
                VALUES (?, ?, ?, ?)
            """, (
                timestamp,
                level,
                message,
                int(failure)
            ))

    conn.commit()
    conn.close()


# -----------------------------------------
# Dashboard
# -----------------------------------------

@app.route("/")
def dashboard():

    return render_template("dashboard.html")


# -----------------------------------------
# Get All Logs
# -----------------------------------------

@app.route("/api/logs")
def get_logs():

    conn = sqlite3.connect(DATABASE)

    conn.row_factory = sqlite3.Row

    cursor = conn.cursor()

    cursor.execute("""
        SELECT *
        FROM logs
        ORDER BY id DESC
    """)

    logs = [dict(row) for row in cursor.fetchall()]

    conn.close()

    return jsonify(logs)


# -----------------------------------------
# Get Statistics
# -----------------------------------------

@app.route("/api/statistics")
def get_statistics():

    conn = sqlite3.connect(DATABASE)

    cursor = conn.cursor()

    cursor.execute("SELECT COUNT(*) FROM logs")
    total = cursor.fetchone()[0]

    cursor.execute("""
        SELECT COUNT(*)
        FROM logs
        WHERE level = 'ERROR'
    """)
    errors = cursor.fetchone()[0]

    cursor.execute("""
        SELECT COUNT(*)
        FROM logs
        WHERE level = 'WARNING'
    """)
    warnings = cursor.fetchone()[0]

    cursor.execute("""
        SELECT COUNT(*)
        FROM logs
        WHERE level = 'CRITICAL'
    """)
    critical = cursor.fetchone()[0]

    conn.close()

    return jsonify({
        "total": total,
        "errors": errors,
        "warnings": warnings,
        "critical": critical
    })


# -----------------------------------------
# Add New Log
# -----------------------------------------

@app.route("/api/logs", methods=["POST"])
def add_log():

    data = request.get_json()

    message = data.get("message", "").strip()

    if not message:

        return jsonify({
            "error": "Log message cannot be empty"
        }), 400


    # Use the SAME detector for severity and failure

    level = analyze_log(message)

    if level == "UNKNOWN":
        level = "INFO"


    failure = detect_failure(
        f"{datetime.now()} {message}"
    )


    timestamp = datetime.now().strftime(
        "%Y-%m-%d %H:%M:%S"
    )


    conn = sqlite3.connect(DATABASE)

    cursor = conn.cursor()


    cursor.execute("""
        INSERT INTO logs
        (timestamp, level, message, failure)
        VALUES (?, ?, ?, ?)
    """, (
        timestamp,
        level,
        message,
        int(failure)
    ))


    conn.commit()

    conn.close()


    return jsonify({
        "success": True,
        "timestamp": timestamp,
        "level": level,
        "message": message,
        "failure": failure
    })


# -----------------------------------------
# Start Application
# -----------------------------------------

if __name__ == "__main__":

    init_database()

    process_logs()

    app.run(debug=True)