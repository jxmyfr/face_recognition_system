# routers/students.py
from fastapi import APIRouter, Depends, HTTPException
from sqlalchemy.orm import Session
from core.database import get_db
from models import Student, Room
from app.schemas.student_schema import StudentCreate, StudentOut

router = APIRouter(prefix="/students", tags=["Students"])

@router.post("/", response_model=StudentOut)
def create_student(data: StudentCreate, db: Session = Depends(get_db)):
    # ตรวจสอบว่า room_id มีอยู่จริงหรือไม่
    room = db.query(Room).get(data.room_id)
    if not room:
        raise HTTPException(status_code=404, detail="Room not found")

    student = Student(**data.dict())
    db.add(student)
    db.commit()
    db.refresh(student)
    return student

@router.get("/", response_model=list[StudentOut])
def get_students(db: Session = Depends(get_db)):
    return db.query(Student).all()

@router.get("/{student_id}", response_model=StudentOut)
def get_student(student_id: int, db: Session = Depends(get_db)):
    student = db.query(Student).get(student_id)
    if not student:
        raise HTTPException(status_code=404, detail="Student not found")
    return student

@router.delete("/{student_id}")
def delete_student(student_id: int, db: Session = Depends(get_db)):
    student = db.query(Student).get(student_id)
    if not student:
        raise HTTPException(status_code=404, detail="Student not found")
    db.delete(student)
    db.commit()
    return {"message": "Student deleted successfully"}
