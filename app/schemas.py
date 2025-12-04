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
# Enrollment Schemas
# ============================================================================

class EnrollmentCreate(BaseModel):
    """Schema for enrolling a student in a class."""
    student_id: str = Field(..., description="Student UUID")
    class_id: str = Field(..., description="Class UUID")


class EnrollmentResponse(BaseModel):
    """Schema for enrollment response."""
    id: str = Field(..., description="Enrollment UUID")
    student_id: str = Field(..., description="Student UUID")
    class_id: str = Field(..., description="Class UUID")
    enrolled_at: str = Field(..., description="Enrollment timestamp in ISO8601 format")


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
    height_m: float = Field(..., gt=0, description="Height in meters")
    
    # Health conditions (boolean with optional notes)
    cardiopathy: bool = Field(default=False, description="Has cardiopathy")
    cardiopathy_notes: Optional[str] = Field(None, description="Cardiopathy notes")
    hypertension: bool = Field(default=False, description="Has hypertension")
    hypertension_notes: Optional[str] = Field(None, description="Hypertension notes")
    diabetes: bool = Field(default=False, description="Has diabetes")
    diabetes_notes: Optional[str] = Field(None, description="Diabetes notes")
    
    # Vital signs
    heart_rate_rest: float = Field(..., gt=0, description="Heart rate at rest (bpm)")
    
    # Physical tests
    wells_sit_reach_test: float = Field(..., description="Wells sit and reach test (cm)")
    trunk_flexion_test: float = Field(..., description="Trunk flexion test (cm)")
    
    # Skinfold measurements (mm)
    skinfold_triceps: float = Field(..., gt=0, description="Triceps skinfold (mm)")
    skinfold_subscapular: float = Field(..., gt=0, description="Subscapular skinfold (mm)")
    skinfold_subaxillary: float = Field(..., gt=0, description="Subaxillary skinfold (mm)")
    skinfold_suprailiac: float = Field(..., gt=0, description="Suprailiac skinfold (mm)")
    skinfold_abdominal: float = Field(..., gt=0, description="Abdominal skinfold (mm)")
    skinfold_quadriceps: float = Field(..., gt=0, description="Quadriceps skinfold (mm)")
    skinfold_calf: float = Field(..., gt=0, description="Calf skinfold (mm)")
    
    # Body perimeters (cm)
    perimeter_chest: float = Field(..., gt=0, description="Chest perimeter (cm)")
    perimeter_arm_r: float = Field(..., gt=0, description="Right arm perimeter (cm)")
    perimeter_arm_l: float = Field(..., gt=0, description="Left arm perimeter (cm)")
    perimeter_arm_contracted_r: float = Field(..., gt=0, description="Right arm contracted perimeter (cm)")
    perimeter_arm_contracted_l: float = Field(..., gt=0, description="Left arm contracted perimeter (cm)")
    perimeter_forearm_r: float = Field(..., gt=0, description="Right forearm perimeter (cm)")
    perimeter_forearm_l: float = Field(..., gt=0, description="Left forearm perimeter (cm)")
    perimeter_waist: float = Field(..., gt=0, description="Waist perimeter (cm)")
    perimeter_abdominal: float = Field(..., gt=0, description="Abdominal perimeter (cm)")
    perimeter_hip: float = Field(..., gt=0, description="Hip perimeter (cm)")
    perimeter_thigh_r: float = Field(..., gt=0, description="Right thigh perimeter (cm)")
    perimeter_thigh_l: float = Field(..., gt=0, description="Left thigh perimeter (cm)")
    perimeter_leg_r: float = Field(..., gt=0, description="Right leg perimeter (cm)")
    perimeter_leg_l: float = Field(..., gt=0, description="Left leg perimeter (cm)")
    
    # Optional notes
    notes: Optional[str] = Field(None, description="Additional evaluation notes")


class EvaluationResponse(BaseModel):
    """Schema for evaluation response."""
    id: str = Field(..., description="Evaluation UUID")
    student_id: str = Field(..., description="Student UUID")
    date: str = Field(..., description="Evaluation date in YYYY-MM-DD format")
    age: int = Field(..., description="Student age at evaluation date")
    weight_kg: float = Field(..., description="Weight in kilograms")
    height_m: float = Field(..., description="Height in meters")
    
    # Health conditions
    cardiopathy: bool = Field(..., description="Has cardiopathy")
    cardiopathy_notes: Optional[str] = Field(None, description="Cardiopathy notes")
    hypertension: bool = Field(..., description="Has hypertension")
    hypertension_notes: Optional[str] = Field(None, description="Hypertension notes")
    diabetes: bool = Field(..., description="Has diabetes")
    diabetes_notes: Optional[str] = Field(None, description="Diabetes notes")
    
    # Vital signs
    heart_rate_rest: float = Field(..., description="Heart rate at rest (bpm)")
    
    # Physical tests
    wells_sit_reach_test: float = Field(..., description="Wells sit and reach test (cm)")
    trunk_flexion_test: float = Field(..., description="Trunk flexion test (cm)")
    
    # Skinfold measurements
    skinfold_triceps: float = Field(..., description="Triceps skinfold (mm)")
    skinfold_subscapular: float = Field(..., description="Subscapular skinfold (mm)")
    skinfold_subaxillary: float = Field(..., description="Subaxillary skinfold (mm)")
    skinfold_suprailiac: float = Field(..., description="Suprailiac skinfold (mm)")
    skinfold_abdominal: float = Field(..., description="Abdominal skinfold (mm)")
    skinfold_quadriceps: float = Field(..., description="Quadriceps skinfold (mm)")
    skinfold_calf: float = Field(..., description="Calf skinfold (mm)")
    
    # Body perimeters
    perimeter_chest: float = Field(..., description="Chest perimeter (cm)")
    perimeter_arm_r: float = Field(..., description="Right arm perimeter (cm)")
    perimeter_arm_l: float = Field(..., description="Left arm perimeter (cm)")
    perimeter_arm_contracted_r: float = Field(..., description="Right arm contracted perimeter (cm)")
    perimeter_arm_contracted_l: float = Field(..., description="Left arm contracted perimeter (cm)")
    perimeter_forearm_r: float = Field(..., description="Right forearm perimeter (cm)")
    perimeter_forearm_l: float = Field(..., description="Left forearm perimeter (cm)")
    perimeter_waist: float = Field(..., description="Waist perimeter (cm)")
    perimeter_abdominal: float = Field(..., description="Abdominal perimeter (cm)")
    perimeter_hip: float = Field(..., description="Hip perimeter (cm)")
    perimeter_thigh_r: float = Field(..., description="Right thigh perimeter (cm)")
    perimeter_thigh_l: float = Field(..., description="Left thigh perimeter (cm)")
    perimeter_leg_r: float = Field(..., description="Right leg perimeter (cm)")
    perimeter_leg_l: float = Field(..., description="Left leg perimeter (cm)")
    
    # Calculated values
    imc: float = Field(..., description="Calculated BMI (IMC)")
    basal_metabolism: float = Field(..., description="Basal metabolism (kcal)")
    body_age: float = Field(..., description="Body age (years)")
    visceral_fat: float = Field(..., description="Visceral fat (level)")
    estimated_height: Optional[float] = Field(None, description="Estimated height (m)")
    fat_weight: float = Field(..., description="Fat weight (kg)")
    lean_weight: float = Field(..., description="Lean weight (kg)")
    fat_percentage: float = Field(..., description="Body fat percentage (%)")
    lean_mass_percentage: float = Field(..., description="Lean mass percentage (%)")
    
    notes: Optional[str] = Field(None, description="Additional evaluation notes")


class ChartDataResponse(BaseModel):
    """Schema for chart data response."""
    labels: List[str] = Field(..., description="Date labels for chart")
    weights: List[float] = Field(..., description="Weight values")
    imc: List[Optional[float]] = Field(..., description="BMI values (can be None)")


class EvaluationReportResponse(BaseModel):
    """Schema for comprehensive evaluation report."""
    evaluation: EvaluationResponse = Field(..., description="Full evaluation data")
    student: StudentResponse = Field(..., description="Student information")
    summary: Dict[str, Any] = Field(..., description="Summary of key metrics and comparisons")


# ============================================================================
# Finance Schemas
# ============================================================================

class FinanceEntryCreate(BaseModel):
    """Schema for creating a finance entry."""
    type: str = Field(..., description="Entry type: 'income' or 'expense'")
    amount: float = Field(..., gt=0, description="Amount (must be positive)")
    payment_method: str = Field(..., description="Payment method: 'credit', 'debit', 'pix', 'cash', 'other'")
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
    
    @field_validator('payment_method')
    @classmethod
    def validate_payment_method(cls, v: str) -> str:
        """Validate payment method."""
        valid_methods = ['credit', 'debit', 'pix', 'cash', 'other']
        if v.lower() not in valid_methods:
            raise ValueError(f"Payment method must be one of: {', '.join(valid_methods)}")
        return v.lower()


class FinanceEntryResponse(BaseModel):
    """Schema for finance entry response."""
    id: str = Field(..., description="Finance entry UUID")
    date_time: str = Field(..., description="Date and time in ISO8601 format")
    type: str = Field(..., description="Entry type: 'income' or 'expense'")
    amount: float = Field(..., description="Amount")
    payment_method: str = Field(..., description="Payment method")
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
