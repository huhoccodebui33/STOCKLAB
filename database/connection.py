import os
import psycopg2
from dotenv import load_dotenv

load_dotenv()

def getConnection():
    connection = psycopg2.connect(
        host = os.getenv("DB_Host"),
        port = os.getenv("DB_PORT"),
        dbname = os.getenv("DB_NAME"),
        user = os.getenv("DB_USER"),
        password = os.getenv("DB_PASSWORD"),
    )
    return connection