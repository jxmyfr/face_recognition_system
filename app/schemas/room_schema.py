from pydantic import BaseModel

class RoomBase(BaseModel):
    class_name: str
    room_number: int
    building: str

class RoomCreate(RoomBase):
    pass

class RoomOut(RoomBase):
    id: int

    class Config:
        orm_mode = True
