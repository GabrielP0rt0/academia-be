"""
Attendance routes.

Operations for managing class attendance records.
"""
from fastapi import APIRouter, HTTPException, Query
from typing import List, Optional
from app.schemas import (
    AttendanceCreate,
    AttendanceBulkCreate,
    AttendanceResponse,
    StudentResponse
)
from app import crud

router = APIRouter(prefix="/api/attendance", tags=["Attendance"])


@router.get("/class/{class_id}/students", response_model=List[StudentResponse], status_code=200)
async def get_enrolled_students_for_attendance(class_id: str):
    """Get all enrolled students for a class (for attendance list)."""
    # Validate class_id exists
    class_item = crud.get_class_by_id(class_id)
    if not class_item:
        raise HTTPException(
            status_code=404,
            detail=f"Class with id {class_id} not found"
        )
    
    # Get only enrolled students
    enrolled_students = crud.get_enrolled_students_by_class(class_id)
    return enrolled_students


@router.post("", response_model=AttendanceResponse, status_code=201)
async def create_attendance(attendance: AttendanceCreate):
    """Create a single attendance record."""
    # Validate class_id exists
    class_item = crud.get_class_by_id(attendance.class_id)
    if not class_item:
        raise HTTPException(
            status_code=404,
            detail=f"Class with id {attendance.class_id} not found"
        )
    
    # Validate student_id exists
    student = crud.get_student_by_id(attendance.student_id)
    if not student:
        raise HTTPException(
            status_code=404,
            detail=f"Student with id {attendance.student_id} not found"
        )
    
    # Validate student is enrolled in the class
    if not crud.is_student_enrolled(attendance.student_id, attendance.class_id):
        raise HTTPException(
            status_code=400,
            detail="Student is not enrolled in this class"
        )
    
    attendance_data = attendance.model_dump()
    new_attendance = crud.create_attendance(attendance_data)
    return new_attendance


@router.post("/bulk", response_model=List[AttendanceResponse], status_code=201)
async def create_attendance_bulk(bulk_data: AttendanceBulkCreate):
    """Create multiple attendance records at once."""
    created_records = []
    
    for entry in bulk_data.entries:
        # Validate class_id exists
        class_item = crud.get_class_by_id(entry.class_id)
        if not class_item:
            raise HTTPException(
                status_code=404,
                detail=f"Class with id {entry.class_id} not found"
            )
        
        # Validate student_id exists
        student = crud.get_student_by_id(entry.student_id)
        if not student:
            raise HTTPException(
                status_code=404,
                detail=f"Student with id {entry.student_id} not found"
            )
        
        # Validate student is enrolled in the class
        if not crud.is_student_enrolled(entry.student_id, entry.class_id):
            raise HTTPException(
                status_code=400,
                detail=f"Student {entry.student_id} is not enrolled in class {entry.class_id}"
            )
    
    # All validations passed, create all records
    entries_data = [entry.model_dump() for entry in bulk_data.entries]
    created_records = crud.create_attendance_bulk(entries_data)
    
    return created_records


@router.get("/class/{class_id}", response_model=List[AttendanceResponse], status_code=200)
async def get_attendance_by_class(
    class_id: str,
    from_date: Optional[str] = Query(None, description="Start date (YYYY-MM-DD)"),
    to_date: Optional[str] = Query(None, description="End date (YYYY-MM-DD)")
):
    """Get attendance records for a specific class, optionally filtered by date range."""
    # Validate class_id exists
    class_item = crud.get_class_by_id(class_id)
    if not class_item:
        raise HTTPException(
            status_code=404,
            detail=f"Class with id {class_id} not found"
        )
    
    attendance_records = crud.get_attendance_by_class(class_id, from_date, to_date)
    return attendance_records

