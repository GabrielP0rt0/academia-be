"""
Dashboard routes.

Operations for dashboard summary data.
"""
from fastapi import APIRouter, Query
from typing import Optional
from app.schemas import DashboardSummaryResponse
from app import crud
from app import utils

router = APIRouter(prefix="/api/dashboard", tags=["Dashboard"])


@router.get("/summary", response_model=DashboardSummaryResponse, status_code=200)
async def get_dashboard_summary(
    date: Optional[str] = Query(None, description="Date in YYYY-MM-DD format (defaults to today)")
):
    """Get dashboard summary for a specific date."""
    # Use provided date or current date
    target_date = date if date else utils.get_current_date_iso()
    target_date = utils.format_date_iso(target_date)
    
    summary = crud.get_dashboard_summary(target_date)
    
    return DashboardSummaryResponse(**summary)

