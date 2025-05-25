from pydantic import BaseModel

class StudentBase(BaseModel):
    fullname: str
    room_id: int
    number: int

class StudentCreate(StudentBase):
    username: str
    password: str

class StudentUpdate(StudentBase):
    pass

class StudentOut(StudentBase):
    id: int

    class Config:
        orm_mode = True
