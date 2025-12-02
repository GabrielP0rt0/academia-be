"""
Pydantic schemas for request/response validation.

All schemas follow the data models specified in the project documentation.
"""
from typing import Optional, List, Dict, Any
from datetime import datetime
from pydantic import BaseModel, Field, field_validator


# ============================================================================
# Authentication Schemas
# ============================================================================

class LoginRequest(BaseModel):
    """Login request schema."""
    email: str = Field(..., description="User email")
    password: str = Field(..., description="User password")


class LoginResponse(BaseModel):
    """Login response schema."""
    token: str = Field(..., description="Authentication token")
    message: str = Field(default="Login successful", description="Response message")


# ============================================================================
# Student Schemas
# ============================================================================

class StudentCreate(BaseModel):
    """Schema for creating a new student."""
    name: str = Field(..., min_length=1, description="Student full name")
    birthdate: Optional[str] = Field(None, description="Birthdate in YYYY-MM-DD format")
    phone: Optional[str] = Field(None, description="Phone number")


class StudentResponse(BaseModel):
    """Schema for student response."""
    id: str = Field(..., description="Student UUID")
    name: str = Field(..., description="Student full name")
    birthdate: Optional[str] = Field(None, description="Birthdate in YYYY-MM-DD format")
    phone: Optional[str] = Field(None, description="Phone number")
    created_at: str = Field(..., description="Creation timestamp in ISO8601 format")


# ============================================================================
# Class Schemas
# ============================================================================

class ClassCreate(BaseModel):
    """Schema for creating a new class."""
    name: str = Field(..., min_length=1, description="Class name")
    description: Optional[str] = Field(None, description="Class description")


class ClassResponse(BaseModel):
    """Schema for class response."""
    id: str = Field(..., description="Class UUID")
    name: str = Field(..., description="Class name")
    description: Optional[str] = Field(None, description="Class description")
    created_at: str = Field(..., description="Creation timestamp in ISO8601 format")


# ============================================================================
# Attendance Schemas
# ============================================================================

class AttendanceCreate(BaseModel):
    """Schema for creating a single attendance record."""
    class_id: str = Field(..., description="Class UUID")
    student_id: str = Field(..., description="Student UUID")
    date_time: Optional[str] = Field(None, description="Date and time in ISO8601 format")
    status: str = Field(..., description="Attendance status: 'present' or 'absent'")
    
    @field_validator('status')
    @classmethod
    def validate_status(cls, v: str) -> str:
        """Validate status is either 'present' or 'absent'."""
        if v.lower() not in ['present', 'absent']:
            raise ValueError("Status must be 'present' or 'absent'")
        return v.lower()


class AttendanceBulkCreate(BaseModel):
    """Schema for creating multiple attendance records."""
    entries: List[AttendanceCreate] = Field(..., description="List of attendance records")


class AttendanceResponse(BaseModel):
    """Schema for attendance response."""
    id: str = Field(..., description="Attendance record UUID")
    class_id: str = Field(..., description="Class UUID")
    student_id: str = Field(..., description="Student UUID")
    date_time: str = Field(..., description="Date and time in ISO8601 format")
    status: str = Field(..., description="Attendance status: 'present' or 'absent'")


# ============================================================================
# Evaluation Schemas
# ============================================================================

class EvaluationCreate(BaseModel):
    """Schema for creating a new evaluation."""
    student_id: str = Field(..., description="Student UUID")
    date: str = Field(..., description="Evaluation date in YYYY-MM-DD format")
    weight_kg: float = Field(..., gt=0, description="Weight in kilograms")
    height_m: Optional[float] = Field(None, gt=0, description="Height in meters")
    measurements: Optional[Dict[str, Any]] = Field(None, description="Additional measurements")
    notes: Optional[str] = Field(None, description="Evaluation notes")


class EvaluationResponse(BaseModel):
    """Schema for evaluation response."""
    id: str = Field(..., description="Evaluation UUID")
    student_id: str = Field(..., description="Student UUID")
    date: str = Field(..., description="Evaluation date in YYYY-MM-DD format")
    weight_kg: float = Field(..., description="Weight in kilograms")
    height_m: Optional[float] = Field(None, description="Height in meters")
    measurements: Optional[Dict[str, Any]] = Field(None, description="Additional measurements")
    notes: Optional[str] = Field(None, description="Evaluation notes")
    imc: Optional[float] = Field(None, description="Calculated BMI (IMC)")


class ChartDataResponse(BaseModel):
    """Schema for chart data response."""
    labels: List[str] = Field(..., description="Date labels for chart")
    weights: List[float] = Field(..., description="Weight values")
    imc: List[Optional[float]] = Field(..., description="BMI values (can be None)")


# ============================================================================
# Finance Schemas
# ============================================================================

class FinanceEntryCreate(BaseModel):
    """Schema for creating a finance entry."""
    type: str = Field(..., description="Entry type: 'income' or 'expense'")
    amount: float = Field(..., gt=0, description="Amount (must be positive)")
    category: Optional[str] = Field(None, description="Category name")
    description: Optional[str] = Field(None, description="Entry description")
    date_time: Optional[str] = Field(None, description="Date and time in ISO8601 format")
    
    @field_validator('type')
    @classmethod
    def validate_type(cls, v: str) -> str:
        """Validate type is either 'income' or 'expense'."""
        if v.lower() not in ['income', 'expense']:
            raise ValueError("Type must be 'income' or 'expense'")
        return v.lower()


class FinanceEntryResponse(BaseModel):
    """Schema for finance entry response."""
    id: str = Field(..., description="Finance entry UUID")
    date_time: str = Field(..., description="Date and time in ISO8601 format")
    type: str = Field(..., description="Entry type: 'income' or 'expense'")
    amount: float = Field(..., description="Amount")
    category: Optional[str] = Field(None, description="Category name")
    description: Optional[str] = Field(None, description="Entry description")
    created_by: Optional[str] = Field(None, description="User who created the entry")


class FinanceSummaryResponse(BaseModel):
    """Schema for finance summary response."""
    entries: List[FinanceEntryResponse] = Field(..., description="List of finance entries")
    total_income: float = Field(..., description="Total income for the date")
    total_expense: float = Field(..., description="Total expense for the date")
    balance: float = Field(..., description="Balance (income - expense)")


# ============================================================================
# Dashboard Schemas
# ============================================================================

class DashboardSummaryResponse(BaseModel):
    """Schema for dashboard summary response."""
    active_students: int = Field(..., description="Number of active students")
    today_classes: int = Field(..., description="Number of classes today")
    total_income_today: float = Field(..., description="Total income for today")
    total_expense_today: float = Field(..., description="Total expense for today")
