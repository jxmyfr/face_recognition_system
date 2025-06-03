from fastapi import APIRouter, Depends, HTTPException
from sqlalchemy.orm import Session
from core.database import get_db
from models import Timetable
from app.schemas.timetable_schema import TimetableCreate, TimetableOut

router = APIRouter(prefix="/timetable", tags=["Timetable"])

@router.get("/")
def get_data(db: Session = Depends(get_db)):
    result = db.query(Timetable).all()
    return result

@router.post("/", response_model=TimetableOut)
def create_timetable(data: TimetableCreate, db: Session = Depends(get_db)):
    timetable = Timetable(**data.dict())
    db.add(timetable)
    db.commit()
    db.refresh(timetable)
    return timetable

@router.get("/", response_model=list[TimetableOut])
def get_timetable(db: Session = Depends(get_db)):
    return db.query(Timetable).all()

@router.get("/{timetable_id}", response_model=TimetableOut)
def get_timetable_by_id(timetable_id: int, db: Session = Depends(get_db)):
    timetable = db.query(Timetable).get(timetable_id)
    if not timetable:
        raise HTTPException(status_code=404, detail="Timetable not found")
    return timetable

@router.delete("/{timetable_id}")
def delete_timetable(timetable_id: int, db: Session = Depends(get_db)):
    timetable = db.query(Timetable).get(timetable_id)
    if not timetable:
        raise HTTPException(status_code=404, detail="Timetable not found")
    db.delete(timetable)
    db.commit()
    return {"message": "Timetable deleted successfully"}
