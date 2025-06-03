from fastapi import APIRouter, Depends, HTTPException
from sqlalchemy.orm import Session
from core.database import get_db
from models import Room
from app.schemas.room_schema import RoomCreate, RoomOut

router = APIRouter(prefix="/rooms", tags=["Rooms"])

@router.get("/")
def get_data(db: Session = Depends(get_db)):
    result = db.query(Room).all()
    return result

@router.post("/", response_model=RoomOut)
def create_room(data: RoomCreate, db: Session = Depends(get_db)):
    room = Room(**data.dict())
    db.add(room)
    db.commit()
    db.refresh(room)
    return room

@router.get("/", response_model=list[RoomOut])
def get_rooms(db: Session = Depends(get_db)):
    return db.query(Room).all()

@router.get("/{room_id}", response_model=RoomOut)
def get_room(room_id: int, db: Session = Depends(get_db)):
    room = db.query(Room).get(room_id)
    if not room:
        raise HTTPException(status_code=404, detail="Room not found")
    return room

@router.delete("/{room_id}")
def delete_room(room_id: int, db: Session = Depends(get_db)):
    room = db.query(Room).get(room_id)
    if not room:
        raise HTTPException(status_code=404, detail="Room not found")
    db.delete(room)
    db.commit()
    return {"message": "Room deleted successfully"}