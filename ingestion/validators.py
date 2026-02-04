# ingestion/validators.py
import mysql.connector
import json
from datetime import datetime, timedelta

from ingestion.db import get_connection

class DBValidator:
    def __init__(self, table_name="incidents", max_age_hours=24, min_rows=10):
        self.table_name = table_name
        self.max_age_hours = max_age_hours
        self.min_rows = min_rows
        self.report = {
            "dataset": table_name,
            "freshness": "unknown",
            "volume": "unknown",
            "nulls": {},
        }
        self.conn = None
        self.cursor = None

    def connect(self):
        self.conn = get_connection()
        self.cursor = self.conn.cursor(dictionary=True)

    def close(self):
        if self.cursor:
            self.cursor.close()
        if self.conn:
            self.conn.close()

    def check_volume(self):
        self.cursor.execute(f"SELECT COUNT(*) AS n FROM {self.table_name}")
        n_rows = self.cursor.fetchone()["n"]
        self.report["volume"] = "ok" if n_rows >= self.min_rows else f"fail ({n_rows} rows)"

    def check_freshness(self, timestamp_col="created_at"):
        self.cursor.execute(f"SELECT MAX({timestamp_col}) AS last_ts FROM {self.table_name}")
        last_ts = self.cursor.fetchone()["last_ts"]
        if last_ts is None:
            self.report["freshness"] = "fail (no data)"
        else:
            age = datetime.now() - last_ts
            self.report["freshness"] = "ok" if age <= timedelta(hours=self.max_age_hours) else f"fail (last record {age} ago)"

    def check_nulls(self):
        self.cursor.execute(f"SHOW COLUMNS FROM {self.table_name}")
        columns = [row["Field"] for row in self.cursor.fetchall()]
        nulls = {}
        for col in columns:
            self.cursor.execute(f"SELECT COUNT(*) AS n_nulls FROM {self.table_name} WHERE {col} IS NULL")
            nulls[col] = self.cursor.fetchone()["n_nulls"]
        self.report["nulls"] = nulls

    def run_all_checks(self):
        self.connect()
        self.check_volume()
        self.check_freshness()
        self.check_nulls()
        self.close()
        return self.report

    def save_report(self, output_file="observability_report.json"):
        with open(output_file, "w") as f:
            json.dump(self.report, f, indent=4)
        print(f"[INFO] Report saved to {output_file}")

# ======================
# Example d'utilisation
# ======================
if __name__ == "__main__":
    validator = DBValidator()
    report = validator.run_all_checks()
    print(json.dumps(report, indent=4))
    validator.save_report()
