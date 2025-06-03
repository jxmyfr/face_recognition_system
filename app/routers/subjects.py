from fastapi import APIRouter, Depends, HTTPException
from sqlalchemy.orm import Session
from models import Subject
from app.schemas.subject_schema import SubjectCreate, SubjectOut
from core.database import get_db

router = APIRouter(prefix="/subjects", tags=["Subjects"])

@router.post("/", response_model=SubjectOut)
def create_subject(data: SubjectCreate, db: Session = Depends(get_db)):
    subject = Subject(**data.dict())
    db.add(subject)
    db.commit()
    db.refresh(subject)
    return subject

@router.get("/", response_model=list[SubjectOut])
def get_subjects(db: Session = Depends(get_db)):
    return db.query(Subject).all()

@router.get("/{subject_id}", response_model=SubjectOut)
def get_subject(subject_id: int, db: Session = Depends(get_db)):
    subject = db.query(Subject).get(subject_id)
    if not subject:
        raise HTTPException(status_code=404, detail="Subject not found")
    return subject

@router.delete("/{subject_id}")
def delete_subject(subject_id: int, db: Session = Depends(get_db)):
    subject = db.query(Subject).get(subject_id)
    if not subject:
        raise HTTPException(status_code=404, detail="Subject not found")
    db.delete(subject)
    db.commit()
    return {"message": "Subject deleted successfully"}
