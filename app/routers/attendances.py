from fastapi import APIRouter, Depends, HTTPException
from sqlalchemy.orm import Session
from core.database import get_db
from models import Attendance
from app.schemas.attendance_schema import AttendanceCreate, AttendanceOut

router = APIRouter(prefix="/attendances", tags=["Attendances"])

@router.post("/", response_model=AttendanceOut)
def create_attendance(data: AttendanceCreate, db: Session = Depends(get_db)):
    attendance = Attendance(**data.dict())
    db.add(attendance)
    db.commit()
    db.refresh(attendance)
    return attendance

@router.get("/", response_model=list[AttendanceOut])
def get_attendances(db: Session = Depends(get_db)):
    return db.query(Attendance).all()

@router.get("/{attendance_id}", response_model=AttendanceOut)
def get_attendance(attendance_id: int, db: Session = Depends(get_db)):
    attendance = db.query(Attendance).get(attendance_id)
    if not attendance:
        raise HTTPException(status_code=404, detail="Attendance not found")
    return attendance

@router.delete("/{attendance_id}")
def delete_attendance(attendance_id: int, db: Session = Depends(get_db)):
    attendance = db.query(Attendance).get(attendance_id)
    if not attendance:
        raise HTTPException(status_code=404, detail="Attendance not found")
    db.delete(attendance)
    db.commit()
    return {"message": "Attendance deleted successfully"}
