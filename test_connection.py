from core.database import engine

try:
    connection = engine.connect()
    print("✅ Connected to Railway MySQL successfully!")
    connection.close()
except Exception as e:
    print("❌ Connection failed:", e)
