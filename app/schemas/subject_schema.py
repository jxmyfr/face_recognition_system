from pydantic import BaseModel

class SubjectBase(BaseModel):
    name: str
    code: str

class SubjectCreate(SubjectBase):
    pass

class SubjectOut(SubjectBase):
    id: int

    class Config:
        orm_mode = True
