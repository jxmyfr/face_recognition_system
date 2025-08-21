from fastapi import APIRouter, Depends, HTTPException
from sqlalchemy.orm import Session
from core.database import get_db
from core.models import Room
from app.schemas.room_schema import RoomCreate, RoomOut
from core.deps import get_current_admin

router = APIRouter(prefix="/rooms", tags=["Rooms"])

@router.get("/", response_model=list[RoomOut])
def get_rooms(db: Session = Depends(get_db)):
    return db.query(Room).all()

@router.post("/", response_model=RoomOut, dependencies=[Depends(get_current_admin)])
def create_room(data: RoomCreate, db: Session = Depends(get_db)):
    room = Room(**data.dict())
    db.add(room)
    db.commit()
    db.refresh(room)
    return room

@router.get("/{room_id}", response_model=RoomOut)
def get_room(room_id: int, db: Session = Depends(get_db)):
    room = db.query(Room).get(room_id)
    if not room:
        raise HTTPException(status_code=404, detail="Room not found")
    return room

@router.delete("/{room_id}", dependencies=[Depends(get_current_admin)])
def delete_room(room_id: int, db: Session = Depends(get_db)):
    room = db.query(Room).get(room_id)
    if not room:
        raise HTTPException(status_code=404, detail="Room not found")
    db.delete(room)
    db.commit()
    return {"message": "Room deleted successfully"}
