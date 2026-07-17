from database.connection import getConnection

try:
    con = getConnection()

    print("✅ Connected to PostgreSQL successfully!")

    con.close()

    print("🔒 Connection closed.")

    
except Exception as e:
    print("❌ Connection failed!")
    print(e)