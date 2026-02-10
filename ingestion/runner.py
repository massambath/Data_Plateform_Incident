
from .generate_data import generate_incidents
from .db import get_connection
from datetime import datetime

def ingest():
    #Générer 100 incidents
    incidents = generate_incidents(n=100, start_date=datetime.now())
    #Connexion à Mysql
    conn = get_connection()
    cursor = conn.cursor()

    #Requête d'insertion
    query = """
    insert into incidents(
                service_name,
            severity,
            incident_type,
            description,
            created_at,
            resolved_at
            )
    values(%s,%s,%s,%s,%s,%s)
    """
    # Préparer les valeurs 
    values = [(i["service_name"],
            i["severity"],
            i["incident_type"],
            i["description"],
            i["created_at"],
            i["resolved_at"]
        )
        for i in incidents
    ]
    #Exécuter 
    cursor.executemany(query,values)
    conn.commit()
    cursor.close()
    conn.close()
    print(f"✅ {len(values)} incidents ingérés")

# Point d'entrée
if __name__ == "__main__":
    ingest()
