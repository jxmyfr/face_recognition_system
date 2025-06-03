# create_admin_user.py

from core.database import SessionLocal
from models import User
from passlib.hash import bcrypt
import sys

def create_admin():
    db = SessionLocal()
    existing_user = db.query(User).filter(User.username == "admin").first()
    if existing_user:
        print("⚠️ Admin user already exists.")
        return

    admin = User(
        username="admin",
        password=bcrypt.hash("admin123"),
        role="admin"
    )
    db.add(admin)
    db.commit()
    db.refresh(admin)
    print("✅ Created admin user: admin / admin123")
    db.close()

if __name__ == "__main__":
    create_admin()
