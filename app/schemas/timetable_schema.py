from pydantic import BaseModel

class TimetableBase(BaseModel):
    subject_id: int
    teacher_id: int
    room_id: int
    day: str
    time_start: str
    time_end: str

class TimetableCreate(TimetableBase):
    pass

class TimetableOut(TimetableBase):
    id: int

    class Config:
        orm_mode = True
