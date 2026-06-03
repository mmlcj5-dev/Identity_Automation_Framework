import json
import os
from datetime import datetime

LOGS_DIR = "logs"

# Ensure logs directory exists
os.makedirs(LOGS_DIR, exist_ok=True)

def write_audit_log(entry: dict):
    """
    Writes a structured audit log entry to a daily log file.
    Each entry is appended as a JSON object on its own line.
    """

    # Create filename based on today's date
    log_filename = f"audit_{datetime.utcnow().strftime('%Y-%m-%d')}.log"
    log_path = os.path.join(LOGS_DIR, log_filename)

    # Add timestamp if not already present
    if "timestamp" not in entry:
        entry["timestamp"] = datetime.utcnow().isoformat()

    # Append JSON entry to the daily log file
    with open(log_path, "a") as log_file:
        log_file.write(json.dumps(entry) + "\n")

    print(f"📝 Audit entry written to {log_filename}")
