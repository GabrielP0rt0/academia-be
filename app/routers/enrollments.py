"""
Enrollments routes.

Operations for managing student enrollments in classes.
"""
from fastapi import APIRouter, HTTPException
from typing import List
from app.schemas import EnrollmentCreate, EnrollmentResponse, StudentResponse
from app import crud

router = APIRouter(prefix="/api/enrollments", tags=["Enrollments"])


@router.get("", response_model=List[EnrollmentResponse], status_code=200)
async def get_all_enrollments():
    """Get all enrollments."""
    enrollments = crud.get_all_enrollments()
    return enrollments


@router.get("/class/{class_id}", response_model=List[EnrollmentResponse], status_code=200)
async def get_enrollments_by_class(class_id: str):
    """Get all enrollments for a specific class."""
    # Validate class exists
    class_item = crud.get_class_by_id(class_id)
    if not class_item:
        raise HTTPException(
            status_code=404,
            detail=f"Class with id {class_id} not found"
        )
    
    enrollments = crud.get_enrollments_by_class(class_id)
    return enrollments


@router.get("/class/{class_id}/students", response_model=List[StudentResponse], status_code=200)
async def get_enrolled_students_by_class(class_id: str):
    """Get all students enrolled in a specific class."""
    # Validate class exists
    class_item = crud.get_class_by_id(class_id)
    if not class_item:
        raise HTTPException(
            status_code=404,
            detail=f"Class with id {class_id} not found"
        )
    
    students = crud.get_enrolled_students_by_class(class_id)
    return students


@router.get("/student/{student_id}", response_model=List[EnrollmentResponse], status_code=200)
async def get_enrollments_by_student(student_id: str):
    """Get all enrollments for a specific student."""
    # Validate student exists
    student = crud.get_student_by_id(student_id)
    if not student:
        raise HTTPException(
            status_code=404,
            detail=f"Student with id {student_id} not found"
        )
    
    enrollments = crud.get_enrollments_by_student(student_id)
    return enrollments


@router.post("", response_model=EnrollmentResponse, status_code=201)
async def create_enrollment(enrollment: EnrollmentCreate):
    """Enroll a student in a class."""
    # Validate class exists
    class_item = crud.get_class_by_id(enrollment.class_id)
    if not class_item:
        raise HTTPException(
            status_code=404,
            detail=f"Class with id {enrollment.class_id} not found"
        )
    
    # Validate student exists
    student = crud.get_student_by_id(enrollment.student_id)
    if not student:
        raise HTTPException(
            status_code=404,
            detail=f"Student with id {enrollment.student_id} not found"
        )
    
    # Check if already enrolled
    if crud.is_student_enrolled(enrollment.student_id, enrollment.class_id):
        raise HTTPException(
            status_code=400,
            detail="Student is already enrolled in this class"
        )
    
    enrollment_data = enrollment.model_dump()
    new_enrollment = crud.create_enrollment(enrollment_data)
    return new_enrollment


@router.delete("/{enrollment_id}", status_code=204)
async def delete_enrollment(enrollment_id: str):
    """Delete an enrollment by ID."""
    success = crud.delete_enrollment(enrollment_id)
    if not success:
        raise HTTPException(
            status_code=404,
            detail=f"Enrollment with id {enrollment_id} not found"
        )


@router.delete("/student/{student_id}/class/{class_id}", status_code=204)
async def delete_enrollment_by_student_and_class(student_id: str, class_id: str):
    """Delete an enrollment by student_id and class_id."""
    success = crud.delete_enrollment_by_student_and_class(student_id, class_id)
    if not success:
        raise HTTPException(
            status_code=404,
            detail=f"Enrollment not found for student {student_id} in class {class_id}"
        )

