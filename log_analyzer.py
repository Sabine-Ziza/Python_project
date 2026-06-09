import argparse
import json
from datetime import datetime
import csv

parser = argparse.ArgumentParser(description="Log Analyzer CLI")

parser.add_argument("-file", required=True, help="Path to log file")
parser.add_argument("--level", help="Filter by log level (ERROR, WARNING, INFO)")
parser.add_argument("--from", dest="from_time", help="Start time (YYYY-MM-DD HH:MM:SS)")
parser.add_argument("--to", dest="to_time", help="End time (YYYY-MM-DD HH:MM:SS)")
parser.add_argument("--export", help="Export summary to CSV file")

args = parser.parse_args()

TIME_FORMAT = "%Y-%m-%d %H:%M:%S"

from_time = datetime.strptime(args.from_time, TIME_FORMAT) if args.from_time else None
to_time = datetime.strptime(args.to_time, TIME_FORMAT) if args.to_time else None

errors = 0
warnings = 0
info = 0

error_message = {}
error_times = []

total_logs = 0

with open(args.file, "r") as file:
    for line in file:
        line = line.strip()

        if not line:
            continue

        try:
            log = json.loads(line)
            timestamp = log["timestamp"]
            level = log["level"]
            message = log["message"]

        except:
            parts = line.split(" ", 3)
            if len(parts) < 4:
                continue

            timestamp = parts[0] + " " + parts[1]
            level = parts[2]
            message = parts[3]

        log_time = datetime.strptime(timestamp, TIME_FORMAT)

        if args.level and level != args.level:
            continue

        if from_time and log_time < from_time:
            continue

        if to_time and log_time > to_time:
            continue

        total_logs += 1

        if level == "ERROR":
            errors += 1
            error_message[message] = error_message.get(message, 0) + 1
            error_times.append(timestamp)

        elif level == "WARNING":
            warnings += 1

        elif level == "INFO":
            info += 1

most_common_error = None
if error_message:
    most_common_error = max(error_message, key=error_message.get)

print("\n===== LOG ANALYSIS REPORT =====")
print("Total logs:          ", total_logs)
print("Errors:              ", errors)
print("Warnings:            ", warnings)
print("Info:                ", info)
print("Most frequent error:", most_common_error)
print("Failure timestamps:  ", ", ".join(error_times))

if args.export:
    with open(args.export, "w", newline="") as csvfile:
        writer = csv.writer(csvfile)

        summary = [
            ["metric", "value"],
            ["total_logs", total_logs],
            ["errors", errors],
            ["warnings", warnings],
            ["info", info],
            ["most_common_error", most_common_error]
        ]

        writer.writerows(summary)

    print(f"Summary exported to {args.export}")
