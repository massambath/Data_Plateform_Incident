import mysql.connector
import os

def get_connection():
    return mysql.connector.connect(
        host="localhost",
        user="incident_user",
        password="incident_pwd",
        database="incidents_db"
        )
