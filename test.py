import sys
from pathlib import Path

PROJECT_ROOT = Path(__file__).resolve().parent
if str(PROJECT_ROOT) not in sys.path:
    sys.path.insert(0, str(PROJECT_ROOT))

from database.connection import getConnection

try:
    con = getConnection()

    print("✅ Connected to PostgreSQL successfully!")

    con.close()

    print("🔒 Connection closed.")

    
except Exception as e:
    print("❌ Connection failed!")
    print(e)