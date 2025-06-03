# create_tables.py
import os
from dotenv import load_dotenv
from core.database import Base, engine
from models import *  # ต้อง import ให้ครบทุกตาราง

load_dotenv()

print("🔧 Creating all tables on the connected database...")
Base.metadata.create_all(bind=engine)
print("✅ Tables created successfully!")
