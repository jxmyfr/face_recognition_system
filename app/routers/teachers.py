from fastapi import APIRouter, Depends, HTTPException
from core.deps import get_current_admin
from sqlalchemy.orm import Session
from core.database import get_db
from models import Teacher, User, RoleEnum
from app.schemas.teacher_schema import TeacherCreate, TeacherOut

router = APIRouter(prefix="/teachers", tags=["Teachers"])

@router.post("/", response_model=TeacherOut)
def create_teacher(data: TeacherCreate, db: Session = Depends(get_db)):
    if db.query(User).filter_by(username=data.username).first():
        raise HTTPException(status_code=400, detail="Username already exists")

    user = User(username=data.username, password=data.password, role=RoleEnum.teacher)
    db.add(user)
    db.commit()
    db.refresh(user)

    teacher = Teacher(fullname=data.fullname, user_id=user.id)
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

@router.get("/", dependencies=[Depends(get_current_admin)])
def get_all_teachers():
    return {"message": "This route is for admin only"}
