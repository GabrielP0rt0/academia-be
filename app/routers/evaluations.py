"""
Evaluations routes.

Operations for managing physical evaluations and chart data.
"""
from fastapi import APIRouter, HTTPException
from typing import List
from app.schemas import (
    EvaluationCreate,
    EvaluationResponse,
    ChartDataResponse
)
from app import crud

router = APIRouter(prefix="/api/evaluations", tags=["Evaluations"])


@router.post("", response_model=EvaluationResponse, status_code=201)
async def create_evaluation(evaluation: EvaluationCreate):
    """Create a new physical evaluation."""
    # Validate student_id exists
    student = crud.get_student_by_id(evaluation.student_id)
    if not student:
        raise HTTPException(
            status_code=404,
            detail=f"Student with id {evaluation.student_id} not found"
        )
    
    evaluation_data = evaluation.model_dump()
    new_evaluation = crud.create_evaluation(evaluation_data)
    return new_evaluation


@router.get("/student/{student_id}", response_model=List[EvaluationResponse], status_code=200)
async def get_evaluations_by_student(student_id: str):
    """Get all evaluations for a specific student, ordered by date."""
    # Validate student_id exists
    student = crud.get_student_by_id(student_id)
    if not student:
        raise HTTPException(
            status_code=404,
            detail=f"Student with id {student_id} not found"
        )
    
    evaluations = crud.get_evaluations_by_student(student_id)
    return evaluations


@router.get("/student/{student_id}/chart-data", response_model=ChartDataResponse, status_code=200)
async def get_chart_data(student_id: str):
    """Get chart data for a student's evaluations (labels, weights, IMC)."""
    # Validate student_id exists
    student = crud.get_student_by_id(student_id)
    if not student:
        raise HTTPException(
            status_code=404,
            detail=f"Student with id {student_id} not found"
        )
    
    chart_data = crud.get_chart_data(student_id)
    return chart_data

