"""
Finance routes.

Operations for managing financial entries and daily closing.
"""
from fastapi import APIRouter, HTTPException, Query
from typing import Optional
from app.schemas import (
    FinanceEntryCreate,
    FinanceEntryResponse,
    FinanceSummaryResponse
)
from app import crud
from app import utils

router = APIRouter(prefix="/api/finance", tags=["Finance"])


@router.post("", response_model=FinanceEntryResponse, status_code=201)
async def create_finance_entry(entry: FinanceEntryCreate):
    """Create a new finance entry (income or expense)."""
    entry_data = entry.model_dump()
    new_entry = crud.create_finance_entry(entry_data)
    return new_entry


@router.get("", response_model=FinanceSummaryResponse, status_code=200)
async def get_finance_summary(
    date: Optional[str] = Query(None, description="Date in YYYY-MM-DD format (defaults to today)")
):
    """Get finance entries for a specific date with aggregated totals."""
    # Use provided date or current date
    target_date = date if date else utils.get_current_date_iso()
    target_date = utils.format_date_iso(target_date)
    
    # Get entries for the date
    entries = crud.get_finance_by_date(target_date)
    
    # Aggregate totals
    summary = utils.aggregate_finance_by_date(entries, target_date)
    
    # Convert entries to response format
    entry_responses = [
        FinanceEntryResponse(**entry) for entry in entries
    ]
    
    return FinanceSummaryResponse(
        entries=entry_responses,
        total_income=summary['total_income'],
        total_expense=summary['total_expense'],
        balance=summary['balance']
    )

