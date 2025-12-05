"""
Classes routes.

CRUD operations for classes management.
"""
from fastapi import APIRouter, HTTPException, Query
from fastapi.responses import Response
from typing import List, Optional
from app.schemas import ClassCreate, ClassResponse
from app import crud
from app.utils_excel import generate_classes_attendance_xlsx

router = APIRouter(prefix="/api/classes", tags=["Classes"])


@router.get("", response_model=List[ClassResponse], status_code=200)
async def get_classes(
    from_date: Optional[str] = Query(None, description="Filter from date (YYYY-MM-DD)"),
    to_date: Optional[str] = Query(None, description="Filter to date (YYYY-MM-DD)")
):
    """Get all classes, optionally filtered by date range."""
    if from_date or to_date:
        classes = crud.get_classes_by_date_range(from_date, to_date)
    else:
        classes = crud.get_all_classes()
    return classes


@router.post("", response_model=ClassResponse, status_code=201)
async def create_class(class_data: ClassCreate):
    """Create a new class."""
    class_dict = class_data.model_dump()
    new_class = crud.create_class(class_dict)
    return new_class


@router.get("/export/xlsx", status_code=200)
async def export_classes_attendance_xlsx(
    from_date: Optional[str] = Query(None, description="Filter from date (YYYY-MM-DD)"),
    to_date: Optional[str] = Query(None, description="Filter to date (YYYY-MM-DD)")
):
    """Export classes and attendance records to Excel filtered by date range."""
    if not from_date or not to_date:
        raise HTTPException(
            status_code=400,
            detail="Both 'from_date' and 'to_date' query parameters are required"
        )
    
    # Get filtered classes
    classes = crud.get_classes_by_date_range(from_date, to_date)
    
    # Get all attendance records for these classes
    all_attendance = crud.get_all_attendance()
    class_ids = {cls['id'] for cls in classes}
    filtered_attendance = [
        att for att in all_attendance
        if att.get('class_id') in class_ids
    ]
    
    # Filter attendance by date range
    from app import utils
    filtered_attendance = utils.filter_by_date_range(
        filtered_attendance,
        'date_time',
        from_date,
        to_date
    )
    
    # Generate Excel file
    excel_bytes = generate_classes_attendance_xlsx(classes, filtered_attendance, from_date, to_date)
    
    # Return file as response
    filename = f"aulas_presenca_{from_date}_a_{to_date}.xlsx"
    return Response(
        content=excel_bytes,
        media_type="application/vnd.openxmlformats-officedocument.spreadsheetml.sheet",
        headers={"Content-Disposition": f"attachment; filename={filename}"}
    )

