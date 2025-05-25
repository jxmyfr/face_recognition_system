from fastapi import APIRouter, HTTPException, Depends
from sqlalchemy.orm import Session
from core.database import get_db
from models import Student, User, Room, RoleEnum
from app.schemas import student_schema

router = APIRouter(prefix="/students", tags=["Students"])

@router.post("/", response_model=student_schema.StudentOut)
def create_student(data: student_schema.StudentCreate, db: Session = Depends(get_db)):
    if db.query(User).filter_by(username=data.username).first():
        raise HTTPException(status_code=400, detail="Username already exists")

    user = User(username=data.username, password=data.password, role=RoleEnum.student)
    db.add(user)
    db.commit()
    db.refresh(user)

    student = Student(fullname=data.fullname, number=data.number, room_id=data.room_id, user_id=user.id)
    db.add(student)
    db.commit()
    db.refresh(student)
    return student

@router.get("/", response_model=list[student_schema.StudentOut])
def get_students(db: Session = Depends(get_db)):
    return db.query(Student).all()

@router.get("/{student_id}", response_model=student_schema.StudentOut)
def get_student(student_id: int, db: Session = Depends(get_db)):
    student = db.query(Student).get(student_id)
    if not student:
        raise HTTPException(status_code=404, detail="Student not found")
    return student

@router.put("/{student_id}", response_model=student_schema.StudentOut)
def update_student(student_id: int, data: student_schema.StudentUpdate, db: Session = Depends(get_db)):
    student = db.query(Student).get(student_id)
    if not student:
        raise HTTPException(status_code=404, detail="Student not found")

    student.fullname = data.fullname
    student.room_id = data.room_id
    student.number = data.number
    db.commit()
    db.refresh(student)
    return student

@router.delete("/{student_id}")
def delete_student(student_id: int, db: Session = Depends(get_db)):
    student = db.query(Student).get(student_id)
    if not student:
        raise HTTPException(status_code=404, detail="Student not found")
    db.delete(student)
    db.commit()
    return {"message": "Student deleted successfully"}
