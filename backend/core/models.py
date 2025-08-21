from sqlalchemy import Column, Integer, String, ForeignKey, Enum, DateTime
from sqlalchemy.orm import relationship, declarative_base
import enum

Base = declarative_base()

class RoleEnum(str, enum.Enum):
    admin = "admin"
    teacher = "teacher"
    student = "student"

class User(Base):
    __tablename__ = "users"
    id = Column(Integer, primary_key=True, index=True)
    username = Column(String(255), unique=True, nullable=False)
    password = Column(String(255), nullable=False)
    role = Column(Enum(RoleEnum), nullable=False)

    student = relationship("Student", back_populates="user", uselist=False)
    teacher = relationship("Teacher", back_populates="user", uselist=False)

class Room(Base):
    __tablename__ = "rooms"
    id = Column(Integer, primary_key=True, index=True)
    class_name = Column(String(20))
    room_number = Column(Integer)
    building = Column(String(50))

    students = relationship("Student", back_populates="room")
    timetables = relationship("Timetable", back_populates="room")

class Student(Base):
    __tablename__ = "students"
    id = Column(Integer, primary_key=True, index=True)
    user_id = Column(Integer, ForeignKey("users.id"))
    fullname = Column(String(255))
    room_id = Column(Integer, ForeignKey("rooms.id"))
    number = Column(Integer)

    user = relationship("User", back_populates="student")
    room = relationship("Room", back_populates="students")
    attendances = relationship("Attendance", back_populates="student")

class Teacher(Base):
    __tablename__ = "teachers"
    id = Column(Integer, primary_key=True, index=True)
    user_id = Column(Integer, ForeignKey("users.id"))
    fullname = Column(String(255))

    user = relationship("User", back_populates="teacher")
    timetables = relationship("Timetable", back_populates="teacher")

class Subject(Base):
    __tablename__ = "subjects"
    id = Column(Integer, primary_key=True, index=True)
    name = Column(String(255))
    code = Column(String(100), unique=True)

    timetables = relationship("Timetable", back_populates="subject")

class Timetable(Base):
    __tablename__ = "timetable"
    id = Column(Integer, primary_key=True, index=True)
    subject_id = Column(Integer, ForeignKey("subjects.id"))
    teacher_id = Column(Integer, ForeignKey("teachers.id"))
    room_id = Column(Integer, ForeignKey("rooms.id"))
    day = Column(String(20))
    time_start = Column(String(10))  # HH:MM
    time_end = Column(String(10))

    subject = relationship("Subject", back_populates="timetables")
    teacher = relationship("Teacher", back_populates="timetables")
    room = relationship("Room", back_populates="timetables")
    attendances = relationship("Attendance", back_populates="timetable")

class Attendance(Base):
    __tablename__ = "attendances"
    id = Column(Integer, primary_key=True, index=True)
    student_id = Column(Integer, ForeignKey("students.id"))
    subject_id = Column(Integer, ForeignKey("subjects.id"))
    timetable_id = Column(Integer, ForeignKey("timetable.id"))
    datetime = Column(DateTime)
    status = Column(String(20))  # normal, late, absent

    student = relationship("Student", back_populates="attendances")
    timetable = relationship("Timetable", back_populates="attendances")
