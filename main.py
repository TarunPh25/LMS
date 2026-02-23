# main.py
# Requirements:
# pip install fastapi uvicorn sqlalchemy pydantic psycopg2-binary "pydantic[email]"

from fastapi import FastAPI, HTTPException, Depends, status
from sqlalchemy import create_engine, Column, Integer, String, Date, Boolean, DateTime, func
from sqlalchemy.ext.declarative import declarative_base
from sqlalchemy.orm import sessionmaker, Session
from pydantic import BaseModel, EmailStr, constr, ConfigDict
from typing import List, Optional
from datetime import date, datetime

# ── Database Configuration ────────────────────────────────────────────────
DATABASE_URL = "postgresql://postgres:Tarun25%40@localhost:5432/mydatabase"

engine = create_engine(DATABASE_URL)
SessionLocal = sessionmaker(autocommit=False, autoflush=False, bind=engine)
Base = declarative_base()

# ── Student Model (SQLAlchemy) ────────────────────────────────────────────
class Student(Base):
    __tablename__ = "students"

    id              = Column(Integer, primary_key=True, index=True)
    first_name      = Column(String(100), nullable=False, index=True)
    last_name       = Column(String(100), nullable=False, index=True)
    email           = Column(String(255), unique=True, nullable=False, index=True)
    phone           = Column(String(20))
    date_of_birth   = Column(Date)
    enrollment_date = Column(Date, server_default=func.current_date())
    status          = Column(String(20), server_default="active")  # active/inactive/suspended/graduated
    created_at      = Column(DateTime(timezone=True), server_default=func.now())
    updated_at      = Column(DateTime(timezone=True), server_default=func.now(), onupdate=func.now())
    is_deleted      = Column(Boolean, default=False, nullable=False)  # Soft delete

# ── Pydantic Models ───────────────────────────────────────────────────────
class StudentCreate(BaseModel):
    first_name: constr(max_length=100)
    last_name: constr(max_length=100)
    email: EmailStr
    phone: Optional[str] = None
    date_of_birth: Optional[date] = None
    status: Optional[str] = "active"


class StudentUpdate(BaseModel):
    first_name: Optional[constr(max_length=100)] = None
    last_name: Optional[constr(max_length=100)] = None
    email: Optional[EmailStr] = None
    phone: Optional[str] = None
    date_of_birth: Optional[date] = None
    status: Optional[str] = None


class StudentResponse(BaseModel):
    id: int
    first_name: str
    last_name: str
    email: EmailStr
    phone: Optional[str] = None
    date_of_birth: Optional[date] = None
    enrollment_date: date
    status: str
    created_at: datetime
    updated_at: datetime
    is_deleted: bool

    model_config = ConfigDict(
        from_attributes=True,                # Allows ORM mode (SQLAlchemy → Pydantic)
        populate_by_name=True,               # Allows snake_case keys
        json_encoders={
            datetime: lambda v: v.isoformat(),
            date: lambda v: v.isoformat(),
        }
    )


# ── Create tables automatically if they don't exist ───────────────────────
Base.metadata.create_all(bind=engine)

# ── FastAPI Application ───────────────────────────────────────────────────
app = FastAPI(
    title="LMS Student Management API",
    description="Industry-grade Student CRUD API for Learning Management System",
    version="1.0.0"
)

# ── CORS Middleware ───────────────────────────────────────────────────────
from fastapi.middleware.cors import CORSMiddleware

app.add_middleware(
    CORSMiddleware,
    allow_origins=["*"],  # Allows all origins
    allow_credentials=True,
    allow_methods=["*"],  # Allows all methods
    allow_headers=["*"],  # Allows all headers
)


# ── Database Dependency ───────────────────────────────────────────────────
def get_db():
    db = SessionLocal()
    try:
        yield db
    finally:
        db.close()


# ── CRUD Endpoints ────────────────────────────────────────────────────────

@app.post("/students/", response_model=StudentResponse, status_code=status.HTTP_201_CREATED)
def create_student(student: StudentCreate, db: Session = Depends(get_db)):
    # Prevent duplicate email
    existing = db.query(Student).filter(Student.email == student.email).first()
    if existing:
        raise HTTPException(status_code=400, detail="Email already registered")

    db_student = Student(**student.dict())
    db.add(db_student)
    db.commit()
    db.refresh(db_student)
    return db_student


@app.get("/students/", response_model=List[StudentResponse])
def read_students(
    skip: int = 0,
    limit: int = 20,
    status: Optional[str] = None,
    db: Session = Depends(get_db)
):
    query = db.query(Student).filter(Student.is_deleted == False)
    if status:
        query = query.filter(Student.status == status)
    return query.offset(skip).limit(limit).all()


@app.get("/students/{student_id}", response_model=StudentResponse)
def read_student(student_id: int, db: Session = Depends(get_db)):
    student = db.query(Student).filter(
        Student.id == student_id,
        Student.is_deleted == False
    ).first()
    if not student:
        raise HTTPException(status_code=404, detail="Student not found or has been deleted")
    return student


@app.put("/students/{student_id}", response_model=StudentResponse)
def update_student(
    student_id: int,
    student_update: StudentUpdate,
    db: Session = Depends(get_db)
):
    db_student = db.query(Student).filter(
        Student.id == student_id,
        Student.is_deleted == False
    ).first()
    if not db_student:
        raise HTTPException(status_code=404, detail="Student not found or has been deleted")

    update_data = student_update.dict(exclude_unset=True)
    for key, value in update_data.items():
        setattr(db_student, key, value)

    db.commit()
    db.refresh(db_student)
    return db_student


@app.delete("/students/{student_id}", status_code=status.HTTP_204_NO_CONTENT)
def delete_student(student_id: int, db: Session = Depends(get_db)):
    db_student = db.query(Student).filter(Student.id == student_id).first()
    if not db_student:
        raise HTTPException(status_code=404, detail="Student not found")

    # Soft delete
    db_student.is_deleted = True
    db.commit()
    return None


# Optional: Permanent delete (use with caution)
@app.delete("/students/{student_id}/hard", status_code=status.HTTP_204_NO_CONTENT)
def hard_delete_student(student_id: int, db: Session = Depends(get_db)):
    db_student = db.query(Student).filter(Student.id == student_id).first()
    if not db_student:
        raise HTTPException(status_code=404, detail="Student not found")
    db.delete(db_student)
    db.commit()
    return None


# ── Run the application ───────────────────────────────────────────────────
if __name__ == "__main__":
    import uvicorn
    uvicorn.run(
        app,
        host="127.0.0.1",
        port=8001,
        reload=True,
        log_level="info"
    )