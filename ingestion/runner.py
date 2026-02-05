from .generate_data import generate_incident
from ingestion.db import get_connection
from ingestion.validators import DBValidator
import json
def ingest():
    conn = get_connection()
    cursor = conn.cursor()

    incidents = generate_incident(n=100)

    query = """
        INSERT INTO incidents (
            service_name,
            severity,
            incident_type,
            description,
            created_at,
            resolved_at
        )
        VALUES (%s, %s, %s, %s, %s, %s)
    """

    values = [
        (
            i["service_name"],
            i["severity"],
            i["incident_type"],
            i["description"],
            i["created_at"],
            i["resolved_at"]
        )
        for i in incidents
    ]

    cursor.executemany(query, values)
    conn.commit()

    cursor.close()
    conn.close()

    print(f"✅ {len(values)} incidents ingérés")

    # ===== Lancement des checks =====
    validator = DBValidator()
    report = validator.run_all_checks()
    print("🔎 Observability report:")
    print(json.dumps(report, indent=4))
    validator.save_report()

if __name__ == "__main__":
    ingest()
