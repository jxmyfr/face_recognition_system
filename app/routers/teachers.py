from fastapi import APIRouter, Depends, HTTPException
from sqlalchemy.orm import Session
from models import Teacher
from app.schemas.teacher_schema import TeacherCreate, TeacherOut
from core.database import get_db

router = APIRouter(prefix="/teachers", tags=["Teachers"])

@router.post("/", response_model=TeacherOut)
def create_teacher(data: TeacherCreate, db: Session = Depends(get_db)):
    teacher = Teacher(**data.dict())
    db.add(teacher)
    db.commit()
    db.refresh(teacher)
    return teacher

@router.get("/", response_model=list[TeacherOut])
def get_teachers(db: Session = Depends(get_db)):
    return db.query(Teacher).all()

@router.get("/{teacher_id}", response_model=TeacherOut)
def get_teacher(teacher_id: int, db: Session = Depends(get_db)):
    teacher = db.query(Teacher).get(teacher_id)
    if not teacher:
        raise HTTPException(status_code=404, detail="Teacher not found")
    return teacher

@router.delete("/{teacher_id}")
def delete_teacher(teacher_id: int, db: Session = Depends(get_db)):
    teacher = db.query(Teacher).get(teacher_id)
    if not teacher:
        raise HTTPException(status_code=404, detail="Teacher not found")
    db.delete(teacher)
    db.commit()
    return {"message": "Teacher deleted successfully"}
