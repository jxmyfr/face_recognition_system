from core.database import Base, engine
import models

print("🔧 Creating all tables on the connected database...")
Base.metadata.create_all(bind=engine)
print("✅ Tables created successfully!")
