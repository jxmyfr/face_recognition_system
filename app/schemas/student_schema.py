from pydantic import BaseModel

class StudentBase(BaseModel):
    fullname: str
    room_id: int
    number: int

class StudentCreate(BaseModel):
    fullname: str
    room_id: int
    number: int

class StudentUpdate(StudentBase):
    pass

class StudentOut(StudentBase):
    id: int

    class Config:
        orm_mode = True
