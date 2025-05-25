from pydantic import BaseModel

class TeacherBase(BaseModel):
    fullname: str

class TeacherCreate(TeacherBase):
    username: str
    password: str

class TeacherOut(TeacherBase):
    id: int

    class Config:
        orm_mode = True
