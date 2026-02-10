from datetime import datetime , timedelta
import random

SERVICES = ["auth-service","payment-api","inventory-api","notification-service","search-service","reporting-service"]

SEVERITIES = ["LOW","MEDIUM","HIGH","CRITICAL"]
INCIDENT_TYPES = ["OUTAGE","LATENCY","ERROR_RATE","DEPLOYMENT","DATA_QUALITY"]


def generate_incident(start_date: datetime):
    created_at = start_date + timedelta(minutes=random.randint(0,60*24))
    duration = random.choice([None, random.randint(10,180)])
    resolved_at = (created_at + timedelta(minutes=duration)) if duration else None
    return {
        "service_name": random.choice(SERVICES),
        "severity": random.choice(SEVERITIES),
        "incident_type": random.choice(INCIDENT_TYPES),
        "description": "Synthetic incident generated for testing",
        "created_at": created_at,
        "resolved_at": resolved_at
    }
def generate_incidents(n=10, start_date=None):
    if start_date is None:
        start_date = datetime.now() - timedelta(days=1)
    # ✅ retourner bien une liste
    return [generate_incident(start_date) for _ in range(n)]



