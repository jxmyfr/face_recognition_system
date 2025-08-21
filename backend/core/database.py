from sqlalchemy import create_engine
from sqlalchemy.ext.declarative import declarative_base
from sqlalchemy.orm import sessionmaker, declarative_base, Session
import os
from dotenv import load_dotenv

load_dotenv()

DB_URL = os.getenv("DB_URL")

engine = create_engine(
    DB_URL,
    echo=False,
    pool_pre_ping=True,      # ตรวจสอบ connection ก่อนใช้ทุกครั้ง
    pool_recycle=1800,       # recycle connection ทุก 30 นาที
    pool_timeout=30          # timeout ถ้าเชื่อมต่อนานเกิน
)

SessionLocal = sessionmaker(autocommit=False, autoflush=False, bind=engine)
Base = declarative_base()

def get_db():
    db: Session = SessionLocal()
    try:
        yield db
    finally:
        db.close()