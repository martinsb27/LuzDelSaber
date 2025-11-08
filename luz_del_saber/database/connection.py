import os
import pyodbc
from dotenv import load_dotenv

load_dotenv()  # Carga las variables del archivo .env

def get_connection():
    server = os.getenv("SQL_SERVER")
    database = os.getenv("SQL_DATABASE")
    driver = os.getenv("SQL_DRIVER")
    trusted = os.getenv("SQL_TRUSTED_CONNECTION")

    try:
        if trusted and trusted.lower() == "yes":
            # Usa autenticación de Windows
            connection_string = f"DRIVER={{{driver}}};SERVER={server};DATABASE={database};Trusted_Connection=yes;"
        else:
            username = os.getenv("SQL_USERNAME")
            password = os.getenv("SQL_PASSWORD")
            connection_string = f"DRIVER={{{driver}}};SERVER={server};DATABASE={database};UID={username};PWD={password}"

        conn = pyodbc.connect(connection_string)
        print("✅ Conexión exitosa a SQL Server.")
        return conn

    except Exception as e:
        print("❌ Error al conectar a la base de datos:", e)
        return None

if __name__ == "__main__":
    conn = get_connection()
    if conn:
        cursor = conn.cursor()
        cursor.execute("SELECT name FROM sys.databases;")
        for row in cursor.fetchall():
            print("-", row[0])
        conn.close()
