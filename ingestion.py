import mysql.connector
import csv

# Connexion MySQL
conn = mysql.connector.connect(
    host="localhost",
    user="root",
    password="passer",
    database="incidents_db"
)

cursor = conn.cursor()

with open("data/samples/incidents.csv", newline="") as csvfile:
    reader = csv.DictReader(csvfile)
    for row in reader:
        cursor.execute(
            """
            INSERT INTO incidents (
                service_name,
                severity,
                description,
                created_at,
                resolved_at
            )
            VALUES (%s, %s, %s, %s, %s)
            """,
            (
                row["service_name"],
                row["severity"],
                row["description"],
                row["created_at"],
                row["resolved_at"]
            )
        )

conn.commit()
cursor.close()
conn.close()

print("✅ Ingestion MySQL terminée")
