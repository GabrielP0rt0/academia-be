"""
Students routes.

CRUD operations for students management.
"""
from fastapi import APIRouter, HTTPException
from typing import List
from app.schemas import StudentCreate, StudentResponse
from app import crud

router = APIRouter(prefix="/api/students", tags=["Students"])


@router.get("", response_model=List[StudentResponse], status_code=200)
async def get_students():
    """Get all students."""
    students = crud.get_all_students()
    return students


@router.get("/{student_id}", response_model=StudentResponse, status_code=200)
async def get_student(student_id: str):
    """Get a specific student by ID."""
    student = crud.get_student_by_id(student_id)
    if not student:
        raise HTTPException(
            status_code=404,
            detail=f"Student with id {student_id} not found"
        )
    return student


@router.post("", response_model=StudentResponse, status_code=201)
async def create_student(student: StudentCreate):
    """Create a new student."""
    student_data = student.model_dump()
    new_student = crud.create_student(student_data)
    return new_student

