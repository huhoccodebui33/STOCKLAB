import os
import psycopg2
from dotenv import load_dotenv

load_dotenv()

def getConnection():
    connection = psycopg2.connect(
        host=os.getenv("DB_HOST") or os.getenv("DB_Host", "127.0.0.1"),
        port=os.getenv("DB_PORT", "5433"),
        dbname=os.getenv("DB_NAME") or os.getenv("DB_Name", "vnstock"),
        user=os.getenv("DB_USER") or os.getenv("DB_User", "postgres"),
        password=os.getenv("DB_PASSWORD") or os.getenv("DB_Password", ""),
    )
    return connection