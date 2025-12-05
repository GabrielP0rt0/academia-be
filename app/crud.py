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
        'date': class_data['date'],
        'time': class_data['time'],
        'created_at': utils.get_current_datetime_iso()
    }
    
    classes.append(new_class)
    db.write_json_file('classes.json', classes)
    
    return new_class


def get_classes_by_date_range(from_date: Optional[str] = None, to_date: Optional[str] = None) -> List[Dict[str, Any]]:
    """Get classes filtered by date range."""
    all_classes = get_all_classes()
    
    if not from_date and not to_date:
        return all_classes
    
    filtered_classes = []
    for class_item in all_classes:
        class_date = class_item.get('date')
        if not class_date:
            continue
        
        if from_date and class_date < from_date:
            continue
        if to_date and class_date > to_date:
            continue
        
        filtered_classes.append(class_item)
    
    return filtered_classes


# ============================================================================
# Enrollment CRUD
# ============================================================================

def get_all_enrollments() -> List[Dict[str, Any]]:
    """Get all enrollments."""
    return db.read_json_file('enrollments.json')


def get_enrollments_by_class(class_id: str) -> List[Dict[str, Any]]:
    """Get all enrollments for a specific class."""
    all_enrollments = get_all_enrollments()
    return [
        enrollment for enrollment in all_enrollments
        if enrollment.get('class_id') == class_id
    ]


def get_enrollments_by_student(student_id: str) -> List[Dict[str, Any]]:
    """Get all enrollments for a specific student."""
    all_enrollments = get_all_enrollments()
    return [
        enrollment for enrollment in all_enrollments
        if enrollment.get('student_id') == student_id
    ]


def get_enrolled_students_by_class(class_id: str) -> List[Dict[str, Any]]:
    """Get all students enrolled in a specific class."""
    enrollments = get_enrollments_by_class(class_id)
    students = get_all_students()
    
    enrolled_student_ids = {enrollment.get('student_id') for enrollment in enrollments}
    enrolled_students = [
        student for student in students
        if student.get('id') in enrolled_student_ids
    ]
    
    return enrolled_students


def is_student_enrolled(student_id: str, class_id: str) -> bool:
    """Check if a student is enrolled in a class."""
    enrollments = get_enrollments_by_class(class_id)
    return any(enrollment.get('student_id') == student_id for enrollment in enrollments)


def create_enrollment(enrollment_data: Dict[str, Any]) -> Dict[str, Any]:
    """Create a new enrollment."""
    all_enrollments = get_all_enrollments()
    
    # Check if enrollment already exists
    if is_student_enrolled(enrollment_data['student_id'], enrollment_data['class_id']):
        raise ValueError("Student is already enrolled in this class")
    
    new_enrollment = {
        'id': str(uuid.uuid4()),
        'student_id': enrollment_data['student_id'],
        'class_id': enrollment_data['class_id'],
        'enrolled_at': utils.get_current_datetime_iso()
    }
    
    all_enrollments.append(new_enrollment)
    db.write_json_file('enrollments.json', all_enrollments)
    
    return new_enrollment


def delete_enrollment(enrollment_id: str) -> bool:
    """Delete an enrollment by ID."""
    all_enrollments = get_all_enrollments()
    
    original_count = len(all_enrollments)
    all_enrollments = [
        enrollment for enrollment in all_enrollments
        if enrollment.get('id') != enrollment_id
    ]
    
    if len(all_enrollments) < original_count:
        db.write_json_file('enrollments.json', all_enrollments)
        return True
    
    return False


def delete_enrollment_by_student_and_class(student_id: str, class_id: str) -> bool:
    """Delete an enrollment by student_id and class_id."""
    all_enrollments = get_all_enrollments()
    
    original_count = len(all_enrollments)
    all_enrollments = [
        enrollment for enrollment in all_enrollments
        if not (enrollment.get('student_id') == student_id and enrollment.get('class_id') == class_id)
    ]
    
    if len(all_enrollments) < original_count:
        db.write_json_file('enrollments.json', all_enrollments)
        return True
    
    return False


# ============================================================================
# Attendance CRUD
# ============================================================================

def get_all_attendance() -> List[Dict[str, Any]]:
    """Get all attendance records."""
    return db.read_json_file('attendance.json')


def get_attendance_by_class(
    class_id: str,
    from_date: Optional[str] = None,
    to_date: Optional[str] = None
) -> List[Dict[str, Any]]:
    """Get attendance records for a class, optionally filtered by date range."""
    all_attendance = get_all_attendance()
    
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

def get_all_evaluations() -> List[Dict[str, Any]]:
    """Get all evaluations."""
    return db.read_json_file('evaluations.json')


def get_evaluation_by_id(evaluation_id: str) -> Optional[Dict[str, Any]]:
    """Get an evaluation by ID."""
    all_evaluations = get_all_evaluations()
    for evaluation in all_evaluations:
        if evaluation.get('id') == evaluation_id:
            return evaluation
    return None


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
    """Create a new evaluation with all calculations."""
    all_evaluations = db.read_json_file('evaluations.json')
    
    # Get student data to calculate age and determine gender
    student = get_student_by_id(evaluation_data['student_id'])
    if not student:
        raise ValueError("Student not found")
    
    birthdate = student.get('birthdate')
    if not birthdate:
        raise ValueError("Student birthdate is required for evaluation")
    
    evaluation_date = utils.format_date_iso(evaluation_data.get('date'))
    age = utils.calculate_age(birthdate, evaluation_date)
    
    # For now, assume male (can be extended later with gender field in student)
    is_male = True
    
    # Extract all required fields
    weight_kg = evaluation_data['weight_kg']
    height_m = evaluation_data['height_m']
    
    # Calculate all metrics
    calculated_metrics = utils.calculate_all_evaluation_metrics(
        weight_kg=weight_kg,
        height_m=height_m,
        age=age,
        is_male=is_male,
        skinfold_triceps=evaluation_data['skinfold_triceps'],
        skinfold_subscapular=evaluation_data['skinfold_subscapular'],
        skinfold_subaxillary=evaluation_data['skinfold_subaxillary'],
        skinfold_suprailiac=evaluation_data['skinfold_suprailiac'],
        skinfold_abdominal=evaluation_data['skinfold_abdominal'],
        skinfold_quadriceps=evaluation_data['skinfold_quadriceps'],
        skinfold_calf=evaluation_data['skinfold_calf'],
        waist_perimeter=evaluation_data['perimeter_waist']
    )
    
    new_evaluation = {
        'id': str(uuid.uuid4()),
        'student_id': evaluation_data['student_id'],
        'date': evaluation_date,
        'age': age,
        'weight_kg': weight_kg,
        'height_m': height_m,
        
        # Health conditions
        'cardiopathy': evaluation_data.get('cardiopathy', False),
        'cardiopathy_notes': evaluation_data.get('cardiopathy_notes'),
        'hypertension': evaluation_data.get('hypertension', False),
        'hypertension_notes': evaluation_data.get('hypertension_notes'),
        'diabetes': evaluation_data.get('diabetes', False),
        'diabetes_notes': evaluation_data.get('diabetes_notes'),
        
        # Vital signs
        'heart_rate_rest': evaluation_data['heart_rate_rest'],
        
        # Physical tests
        'wells_sit_reach_test': evaluation_data['wells_sit_reach_test'],
        'trunk_flexion_test': evaluation_data['trunk_flexion_test'],
        
        # Skinfold measurements
        'skinfold_triceps': evaluation_data['skinfold_triceps'],
        'skinfold_subscapular': evaluation_data['skinfold_subscapular'],
        'skinfold_subaxillary': evaluation_data['skinfold_subaxillary'],
        'skinfold_suprailiac': evaluation_data['skinfold_suprailiac'],
        'skinfold_abdominal': evaluation_data['skinfold_abdominal'],
        'skinfold_quadriceps': evaluation_data['skinfold_quadriceps'],
        'skinfold_calf': evaluation_data['skinfold_calf'],
        
        # Body perimeters
        'perimeter_chest': evaluation_data['perimeter_chest'],
        'perimeter_arm_r': evaluation_data['perimeter_arm_r'],
        'perimeter_arm_l': evaluation_data['perimeter_arm_l'],
        'perimeter_arm_contracted_r': evaluation_data['perimeter_arm_contracted_r'],
        'perimeter_arm_contracted_l': evaluation_data['perimeter_arm_contracted_l'],
        'perimeter_forearm_r': evaluation_data['perimeter_forearm_r'],
        'perimeter_forearm_l': evaluation_data['perimeter_forearm_l'],
        'perimeter_waist': evaluation_data['perimeter_waist'],
        'perimeter_abdominal': evaluation_data['perimeter_abdominal'],
        'perimeter_hip': evaluation_data['perimeter_hip'],
        'perimeter_thigh_r': evaluation_data['perimeter_thigh_r'],
        'perimeter_thigh_l': evaluation_data['perimeter_thigh_l'],
        'perimeter_leg_r': evaluation_data['perimeter_leg_r'],
        'perimeter_leg_l': evaluation_data['perimeter_leg_l'],
        
        # Calculated values
        'imc': calculated_metrics['imc'],
        'basal_metabolism': calculated_metrics['basal_metabolism'],
        'body_age': calculated_metrics['body_age'],
        'visceral_fat': calculated_metrics['visceral_fat'],
        'estimated_height': calculated_metrics['estimated_height'],
        'fat_weight': calculated_metrics['fat_weight'],
        'lean_weight': calculated_metrics['lean_weight'],
        'fat_percentage': calculated_metrics['fat_percentage'],
        'lean_mass_percentage': calculated_metrics['lean_mass_percentage'],
        
        'notes': evaluation_data.get('notes')
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
        'payment_method': finance_data['payment_method'].lower(),
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


# ============================================================================
# Evaluation Report Functions
# ============================================================================

def get_student_response(student: Dict[str, Any]) -> Dict[str, Any]:
    """Convert student dict to StudentResponse format."""
    from app.schemas import StudentResponse
    return StudentResponse(**student).model_dump()


def generate_evaluation_summary(
    current_evaluation: Dict[str, Any],
    all_evaluations: List[Dict[str, Any]]
) -> Dict[str, Any]:
    """
    Generate summary and comparison data for evaluation report.
    
    Args:
        current_evaluation: The evaluation to generate report for
        all_evaluations: All evaluations for the student (for comparison)
    
    Returns:
        Dictionary with summary metrics and comparisons
    """
    # Find previous evaluation
    current_date = current_evaluation.get('date', '')
    previous_evaluation = None
    
    for eval_record in sorted(all_evaluations, key=lambda x: x.get('date', ''), reverse=True):
        if eval_record.get('date', '') < current_date:
            previous_evaluation = eval_record
            break
    
    summary = {
        'current_date': current_evaluation.get('date'),
        'evaluation_number': len([e for e in all_evaluations if e.get('date', '') <= current_date]),
        'total_evaluations': len(all_evaluations),
        'key_metrics': {
            'weight_kg': current_evaluation.get('weight_kg'),
            'height_m': current_evaluation.get('height_m'),
            'imc': current_evaluation.get('imc'),
            'fat_percentage': current_evaluation.get('fat_percentage'),
            'lean_mass_percentage': current_evaluation.get('lean_mass_percentage'),
            'basal_metabolism': current_evaluation.get('basal_metabolism'),
            'body_age': current_evaluation.get('body_age'),
            'visceral_fat': current_evaluation.get('visceral_fat')
        },
        'health_conditions': {
            'cardiopathy': current_evaluation.get('cardiopathy', False),
            'hypertension': current_evaluation.get('hypertension', False),
            'diabetes': current_evaluation.get('diabetes', False)
        },
        'comparison_with_previous': {}
    }
    
    # Add comparisons if previous evaluation exists
    if previous_evaluation:
        weight_change = current_evaluation.get('weight_kg', 0) - previous_evaluation.get('weight_kg', 0)
        imc_change = current_evaluation.get('imc', 0) - previous_evaluation.get('imc', 0)
        fat_change = current_evaluation.get('fat_percentage', 0) - previous_evaluation.get('fat_percentage', 0)
        
        summary['comparison_with_previous'] = {
            'previous_date': previous_evaluation.get('date'),
            'weight_change_kg': round(weight_change, 2),
            'imc_change': round(imc_change, 2),
            'fat_percentage_change': round(fat_change, 2),
            'trend': 'improving' if fat_change < 0 and weight_change <= 0 else 'maintaining' if abs(fat_change) < 1 else 'needs_attention'
        }
    
    return summary
