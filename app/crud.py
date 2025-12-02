"""
CRUD operations for all resources.

This module provides high-level CRUD functions that use the db.py layer
for reading and writing JSON files.
"""
import uuid
from typing import List, Dict, Any, Optional
from datetime import datetime

from app import db
from app import utils


# ============================================================================
# Students CRUD
# ============================================================================

def get_all_students() -> List[Dict[str, Any]]:
    """Get all students."""
    return db.read_json_file('students.json')


def get_student_by_id(student_id: str) -> Optional[Dict[str, Any]]:
    """Get a student by ID."""
    students = get_all_students()
    for student in students:
        if student.get('id') == student_id:
            return student
    return None


def create_student(student_data: Dict[str, Any]) -> Dict[str, Any]:
    """Create a new student."""
    students = get_all_students()
    
    new_student = {
        'id': str(uuid.uuid4()),
        'name': student_data['name'],
        'birthdate': student_data.get('birthdate'),
        'phone': student_data.get('phone'),
        'created_at': utils.get_current_datetime_iso()
    }
    
    students.append(new_student)
    db.write_json_file('students.json', students)
    
    return new_student


# ============================================================================
# Classes CRUD
# ============================================================================

def get_all_classes() -> List[Dict[str, Any]]:
    """Get all classes."""
    return db.read_json_file('classes.json')


def get_class_by_id(class_id: str) -> Optional[Dict[str, Any]]:
    """Get a class by ID."""
    classes = get_all_classes()
    for class_item in classes:
        if class_item.get('id') == class_id:
            return class_item
    return None


def create_class(class_data: Dict[str, Any]) -> Dict[str, Any]:
    """Create a new class."""
    classes = get_all_classes()
    
    new_class = {
        'id': str(uuid.uuid4()),
        'name': class_data['name'],
        'description': class_data.get('description'),
        'created_at': utils.get_current_datetime_iso()
    }
    
    classes.append(new_class)
    db.write_json_file('classes.json', classes)
    
    return new_class


# ============================================================================
# Attendance CRUD
# ============================================================================

def get_attendance_by_class(
    class_id: str,
    from_date: Optional[str] = None,
    to_date: Optional[str] = None
) -> List[Dict[str, Any]]:
    """Get attendance records for a class, optionally filtered by date range."""
    all_attendance = db.read_json_file('attendance.json')
    
    # Filter by class_id
    class_attendance = [
        record for record in all_attendance
        if record.get('class_id') == class_id
    ]
    
    # Filter by date range if provided
    if from_date or to_date:
        class_attendance = utils.filter_by_date_range(
            class_attendance,
            'date_time',
            from_date,
            to_date
        )
    
    return class_attendance


def create_attendance(attendance_data: Dict[str, Any]) -> Dict[str, Any]:
    """Create a single attendance record."""
    all_attendance = db.read_json_file('attendance.json')
    
    # Use provided date_time or current datetime
    date_time = attendance_data.get('date_time')
    if not date_time:
        date_time = utils.get_current_datetime_iso()
    
    new_attendance = {
        'id': str(uuid.uuid4()),
        'class_id': attendance_data['class_id'],
        'student_id': attendance_data['student_id'],
        'date_time': date_time,
        'status': attendance_data['status'].lower()
    }
    
    all_attendance.append(new_attendance)
    db.write_json_file('attendance.json', all_attendance)
    
    return new_attendance


def create_attendance_bulk(entries: List[Dict[str, Any]]) -> List[Dict[str, Any]]:
    """Create multiple attendance records."""
    all_attendance = db.read_json_file('attendance.json')
    created_records = []
    
    for entry_data in entries:
        date_time = entry_data.get('date_time')
        if not date_time:
            date_time = utils.get_current_datetime_iso()
        
        new_attendance = {
            'id': str(uuid.uuid4()),
            'class_id': entry_data['class_id'],
            'student_id': entry_data['student_id'],
            'date_time': date_time,
            'status': entry_data['status'].lower()
        }
        
        all_attendance.append(new_attendance)
        created_records.append(new_attendance)
    
    db.write_json_file('attendance.json', all_attendance)
    
    return created_records


# ============================================================================
# Evaluations CRUD
# ============================================================================

def get_evaluations_by_student(student_id: str) -> List[Dict[str, Any]]:
    """Get all evaluations for a student, ordered by date."""
    all_evaluations = db.read_json_file('evaluations.json')
    
    student_evaluations = [
        eval_record for eval_record in all_evaluations
        if eval_record.get('student_id') == student_id
    ]
    
    # Sort by date (ascending)
    student_evaluations.sort(key=lambda x: x.get('date', ''))
    
    return student_evaluations


def create_evaluation(evaluation_data: Dict[str, Any]) -> Dict[str, Any]:
    """Create a new evaluation."""
    all_evaluations = db.read_json_file('evaluations.json')
    
    # Calculate BMI if height is provided
    height_m = evaluation_data.get('height_m')
    weight_kg = evaluation_data['weight_kg']
    imc = utils.calculate_bmi(weight_kg, height_m)
    
    new_evaluation = {
        'id': str(uuid.uuid4()),
        'student_id': evaluation_data['student_id'],
        'date': utils.format_date_iso(evaluation_data.get('date')),
        'weight_kg': weight_kg,
        'height_m': height_m,
        'measurements': evaluation_data.get('measurements'),
        'notes': evaluation_data.get('notes'),
        'imc': imc
    }
    
    all_evaluations.append(new_evaluation)
    db.write_json_file('evaluations.json', all_evaluations)
    
    return new_evaluation


def get_chart_data(student_id: str) -> Dict[str, Any]:
    """Get chart data for a student's evaluations."""
    evaluations = get_evaluations_by_student(student_id)
    
    labels = []
    weights = []
    imc_values = []
    
    for eval_record in evaluations:
        labels.append(eval_record.get('date', ''))
        weights.append(eval_record.get('weight_kg', 0))
        imc_values.append(eval_record.get('imc'))
    
    return {
        'labels': labels,
        'weights': weights,
        'imc': imc_values
    }


# ============================================================================
# Finance CRUD
# ============================================================================

def get_finance_by_date(target_date: Optional[str] = None) -> List[Dict[str, Any]]:
    """Get finance entries for a specific date."""
    if not target_date:
        target_date = utils.get_current_date_iso()
    else:
        target_date = utils.format_date_iso(target_date)
    
    all_finance = db.read_json_file('finance.json')
    
    # Filter entries by date
    filtered_entries = []
    for entry in all_finance:
        entry_date = entry.get('date_time', '')
        # Extract date part from ISO8601 datetime
        if 'T' in entry_date:
            entry_date = entry_date.split('T')[0]
        
        if entry_date == target_date:
            filtered_entries.append(entry)
    
    return filtered_entries


def create_finance_entry(finance_data: Dict[str, Any]) -> Dict[str, Any]:
    """Create a new finance entry."""
    all_finance = db.read_json_file('finance.json')
    
    # Use provided date_time or current datetime
    date_time = finance_data.get('date_time')
    if not date_time:
        date_time = utils.get_current_datetime_iso()
    
    new_entry = {
        'id': str(uuid.uuid4()),
        'date_time': date_time,
        'type': finance_data['type'].lower(),
        'amount': float(finance_data['amount']),
        'category': finance_data.get('category'),
        'description': finance_data.get('description'),
        'created_by': finance_data.get('created_by')
    }
    
    all_finance.append(new_entry)
    db.write_json_file('finance.json', all_finance)
    
    return new_entry


# ============================================================================
# Dashboard CRUD
# ============================================================================

def get_dashboard_summary(target_date: Optional[str] = None) -> Dict[str, Any]:
    """Get dashboard summary for a specific date."""
    if not target_date:
        target_date = utils.get_current_date_iso()
    else:
        target_date = utils.format_date_iso(target_date)
    
    # Count active students (students with at least one attendance record)
    all_students = get_all_students()
    all_attendance = db.read_json_file('attendance.json')
    
    active_student_ids = set()
    for attendance in all_attendance:
        active_student_ids.add(attendance.get('student_id'))
    
    active_students = len([
        student for student in all_students
        if student.get('id') in active_student_ids
    ])
    
    # Count today's classes (classes with attendance records today)
    today_classes_set = set()
    for attendance in all_attendance:
        attendance_date = attendance.get('date_time', '')
        if 'T' in attendance_date:
            attendance_date = attendance_date.split('T')[0]
        
        if attendance_date == target_date:
            today_classes_set.add(attendance.get('class_id'))
    
    today_classes = len(today_classes_set)
    
    # Get finance totals for the date
    finance_entries = get_finance_by_date(target_date)
    finance_summary = utils.aggregate_finance_by_date(finance_entries, target_date)
    
    return {
        'active_students': active_students,
        'today_classes': today_classes,
        'total_income_today': finance_summary['total_income'],
        'total_expense_today': finance_summary['total_expense']
    }
