from pydantic import BaseModel
from datetime import datetime

class AttendanceBase(BaseModel):
    student_id: int
    subject_id: int
    timetable_id: int
    datetime: datetime
    status: str  # e.g. normal, late, absent

class AttendanceCreate(AttendanceBase):
    pass

class AttendanceOut(AttendanceBase):
    id: int

    class Config:
        orm_mode = True
