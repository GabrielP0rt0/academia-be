"""
Classes routes.

CRUD operations for classes management.
"""
from fastapi import APIRouter, HTTPException
from typing import List
from app.schemas import ClassCreate, ClassResponse
from app import crud

router = APIRouter(prefix="/api/classes", tags=["Classes"])


@router.get("", response_model=List[ClassResponse], status_code=200)
async def get_classes():
    """Get all classes."""
    classes = crud.get_all_classes()
    return classes


@router.post("", response_model=ClassResponse, status_code=201)
async def create_class(class_data: ClassCreate):
    """Create a new class."""
    class_dict = class_data.model_dump()
    new_class = crud.create_class(class_dict)
    return new_class

