from passlib.context import CryptContext
from sqlalchemy.orm import Session
from core.database import engine, SessionLocal
from models import User

pwd_context = CryptContext(schemes=["bcrypt"], deprecated="auto")

def create_admin():
    db: Session = SessionLocal()
    hashed = pwd_context.hash("admin123")
    user = User(username="admin", password=hashed, role="admin")
    db.add(user)
    db.commit()
    db.refresh(user)
    print("✅ Created admin user: admin / admin123")

if __name__ == "__main__":
    create_admin()