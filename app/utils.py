"""
Utility functions for business logic and data formatting.

Includes BMI calculation, financial aggregations, and date formatting utilities.
"""
from typing import List, Dict, Any, Optional
from datetime import datetime, date


def calculate_bmi(weight_kg: float, height_m: Optional[float]) -> Optional[float]:
    """
    Calculate BMI (Body Mass Index) / IMC.
    
    Formula: weight_kg / (height_m ** 2)
    
    Args:
        weight_kg: Weight in kilograms
        height_m: Height in meters (optional)
    
    Returns:
        BMI value rounded to 2 decimal places, or None if height is not provided
    """
    if height_m is None or height_m <= 0:
        return None
    
    if weight_kg <= 0:
        return None
    
    bmi = weight_kg / (height_m ** 2)
    return round(bmi, 2)


def aggregate_finance_by_date(
    entries: List[Dict[str, Any]], 
    target_date: str
) -> Dict[str, float]:
    """
    Aggregate finance entries by date.
    
    Args:
        entries: List of finance entry dictionaries
        target_date: Target date in YYYY-MM-DD format
    
    Returns:
        Dictionary with total_income, total_expense, and balance
    """
    total_income = 0.0
    total_expense = 0.0
    
    for entry in entries:
        entry_date = entry.get('date_time', '')
        # Extract date part (YYYY-MM-DD) from ISO8601 datetime
        if 'T' in entry_date:
            entry_date = entry_date.split('T')[0]
        
        if entry_date == target_date:
            entry_type = entry.get('type', '').lower()
            amount = float(entry.get('amount', 0))
            
            if entry_type == 'income':
                total_income += amount
            elif entry_type == 'expense':
                total_expense += amount
    
    balance = total_income - total_expense
    
    return {
        'total_income': round(total_income, 2),
        'total_expense': round(total_expense, 2),
        'balance': round(balance, 2)
    }


def format_date_iso(date_string: Optional[str]) -> str:
    """
    Normalize date string to YYYY-MM-DD format.
    
    Args:
        date_string: Date string in various formats
    
    Returns:
        Normalized date string in YYYY-MM-DD format
    """
    if not date_string:
        return get_current_date_iso()
    
    # If already in YYYY-MM-DD format, return as is
    if len(date_string) == 10 and date_string.count('-') == 2:
        try:
            # Validate it's a valid date
            datetime.strptime(date_string, '%Y-%m-%d')
            return date_string
        except ValueError:
            pass
    
    # Try to parse various formats
    formats = [
        '%Y-%m-%d',
        '%Y/%m/%d',
        '%d/%m/%Y',
        '%d-%m-%Y',
        '%Y-%m-%dT%H:%M:%S',
        '%Y-%m-%dT%H:%M:%S.%f',
    ]
    
    for fmt in formats:
        try:
            dt = datetime.strptime(date_string, fmt)
            return dt.strftime('%Y-%m-%d')
        except ValueError:
            continue
    
    # If all parsing fails, return current date
    return get_current_date_iso()


def get_current_datetime_iso() -> str:
    """
    Get current date and time in ISO8601 format.
    
    Returns:
        Current datetime string in ISO8601 format (e.g., '2025-01-12T20:30:45')
    """
    return datetime.now().isoformat()


def get_current_date_iso() -> str:
    """
    Get current date in YYYY-MM-DD format.
    
    Returns:
        Current date string in YYYY-MM-DD format (e.g., '2025-01-12')
    """
    return datetime.now().strftime('%Y-%m-%d')


def parse_date_from_iso(iso_string: str) -> Optional[date]:
    """
    Parse ISO8601 datetime string to date object.
    
    Args:
        iso_string: ISO8601 datetime string
    
    Returns:
        date object or None if parsing fails
    """
    try:
        # Handle both date-only and datetime formats
        if 'T' in iso_string:
            dt = datetime.fromisoformat(iso_string.replace('Z', '+00:00'))
            return dt.date()
        else:
            return datetime.strptime(iso_string, '%Y-%m-%d').date()
    except (ValueError, AttributeError):
        return None


def filter_by_date_range(
    items: List[Dict[str, Any]],
    date_field: str,
    from_date: Optional[str] = None,
    to_date: Optional[str] = None
) -> List[Dict[str, Any]]:
    """
    Filter items by date range.
    
    Args:
        items: List of dictionaries with date fields
        date_field: Name of the date field in the dictionaries
        from_date: Start date in YYYY-MM-DD format (inclusive)
        to_date: End date in YYYY-MM-DD format (inclusive)
    
    Returns:
        Filtered list of items
    """
    if not from_date and not to_date:
        return items
    
    filtered = []
    
    for item in items:
        item_date_str = item.get(date_field, '')
        if not item_date_str:
            continue
        
        # Extract date part if it's a datetime string
        if 'T' in item_date_str:
            item_date_str = item_date_str.split('T')[0]
        
        item_date = parse_date_from_iso(item_date_str)
        if not item_date:
            continue
        
        # Check date range
        if from_date:
            from_date_obj = parse_date_from_iso(from_date)
            if from_date_obj and item_date < from_date_obj:
                continue
        
        if to_date:
            to_date_obj = parse_date_from_iso(to_date)
            if to_date_obj and item_date > to_date_obj:
                continue
        
        filtered.append(item)
    
    return filtered


# ============================================================================
# Evaluation Calculation Functions
# ============================================================================

def calculate_age(birthdate: str, evaluation_date: str) -> int:
    """
    Calculate age from birthdate to evaluation date.
    
    Args:
        birthdate: Birthdate in YYYY-MM-DD format
        evaluation_date: Evaluation date in YYYY-MM-DD format
    
    Returns:
        Age in years
    """
    try:
        birth = parse_date_from_iso(birthdate)
        eval_date = parse_date_from_iso(evaluation_date)
        
        if not birth or not eval_date:
            return 0
        
        age = eval_date.year - birth.year
        if (eval_date.month, eval_date.day) < (birth.month, birth.day):
            age -= 1
        
        return max(0, age)
    except (ValueError, AttributeError):
        return 0


def calculate_basal_metabolism(weight_kg: float, height_m: float, age: int, is_male: bool = True) -> float:
    """
    Calculate basal metabolic rate using Harris-Benedict equation.
    
    Args:
        weight_kg: Weight in kilograms
        height_m: Height in meters
        age: Age in years
        is_male: True for male, False for female
    
    Returns:
        Basal metabolism in kcal/day, rounded to 2 decimal places
    """
    height_cm = height_m * 100
    
    if is_male:
        # Harris-Benedict equation for men
        bmr = 88.362 + (13.397 * weight_kg) + (4.799 * height_cm) - (5.677 * age)
    else:
        # Harris-Benedict equation for women
        bmr = 447.593 + (9.247 * weight_kg) + (3.098 * height_cm) - (4.330 * age)
    
    return round(bmr, 2)


def calculate_body_fat_percentage(
    age: int,
    is_male: bool,
    skinfold_triceps: float,
    skinfold_subscapular: float,
    skinfold_subaxillary: float,
    skinfold_suprailiac: float,
    skinfold_abdominal: float,
    skinfold_quadriceps: float,
    skinfold_calf: float
) -> float:
    """
    Calculate body fat percentage using Jackson-Pollock 7-site skinfold method.
    
    Args:
        age: Age in years
        is_male: True for male, False for female
        skinfold_*: Skinfold measurements in mm
    
    Returns:
        Body fat percentage, rounded to 2 decimal places
    """
    # Sum of all 7 skinfolds
    sum_skinfolds = (
        skinfold_triceps +
        skinfold_subscapular +
        skinfold_subaxillary +
        skinfold_suprailiac +
        skinfold_abdominal +
        skinfold_quadriceps +
        skinfold_calf
    )
    
    # Jackson-Pollock 7-site formula
    if is_male:
        # Men: BD = 1.112 - (0.00043499 × S) + (0.00000055 × S²) - (0.00028826 × age)
        body_density = 1.112 - (0.00043499 * sum_skinfolds) + (0.00000055 * (sum_skinfolds ** 2)) - (0.00028826 * age)
    else:
        # Women: BD = 1.097 - (0.00046971 × S) + (0.00000056 × S²) - (0.00012828 × age)
        body_density = 1.097 - (0.00046971 * sum_skinfolds) + (0.00000056 * (sum_skinfolds ** 2)) - (0.00012828 * age)
    
    # Convert body density to body fat percentage using Siri equation
    body_fat_percentage = ((4.95 / body_density) - 4.5) * 100
    
    # Ensure reasonable bounds
    body_fat_percentage = max(5.0, min(50.0, body_fat_percentage))
    
    return round(body_fat_percentage, 2)


def calculate_fat_and_lean_weight(weight_kg: float, fat_percentage: float) -> Dict[str, float]:
    """
    Calculate fat weight and lean weight from total weight and fat percentage.
    
    Args:
        weight_kg: Total weight in kilograms
        fat_percentage: Body fat percentage
    
    Returns:
        Dictionary with 'fat_weight' and 'lean_weight' in kg
    """
    fat_weight = (weight_kg * fat_percentage) / 100
    lean_weight = weight_kg - fat_weight
    
    return {
        'fat_weight': round(fat_weight, 2),
        'lean_weight': round(lean_weight, 2)
    }


def calculate_lean_mass_percentage(fat_percentage: float) -> float:
    """
    Calculate lean mass percentage from fat percentage.
    
    Args:
        fat_percentage: Body fat percentage
    
    Returns:
        Lean mass percentage, rounded to 2 decimal places
    """
    lean_percentage = 100 - fat_percentage
    return round(lean_percentage, 2)


def calculate_visceral_fat(waist_perimeter: float, height_m: float, age: int, is_male: bool) -> float:
    """
    Calculate visceral fat level using waist-to-height ratio and age.
    
    Args:
        waist_perimeter: Waist perimeter in cm
        height_m: Height in meters
        age: Age in years
        is_male: True for male, False for female
    
    Returns:
        Visceral fat level (0-59 scale), rounded to 2 decimal places
    """
    height_cm = height_m * 100
    waist_to_height_ratio = waist_perimeter / height_cm
    
    # Base calculation
    if is_male:
        visceral_fat = (waist_perimeter - (0.082 * height_cm)) * 1.18
    else:
        visceral_fat = (waist_perimeter - (0.082 * height_cm)) * 1.18
    
    # Adjust for age
    age_factor = age * 0.1
    visceral_fat += age_factor
    
    # Normalize to 0-59 scale (typical visceral fat range)
    visceral_fat = max(0.0, min(59.0, visceral_fat))
    
    return round(visceral_fat, 2)


def calculate_body_age(
    age: int,
    bmi: float,
    fat_percentage: float,
    visceral_fat: float,
    is_male: bool
) -> float:
    """
    Calculate body age based on body composition metrics.
    
    Args:
        age: Chronological age in years
        bmi: Body Mass Index
        fat_percentage: Body fat percentage
        visceral_fat: Visceral fat level
        is_male: True for male, False for female
    
    Returns:
        Estimated body age in years, rounded to 1 decimal place
    """
    # Base body age starts at chronological age
    body_age = float(age)
    
    # Adjust based on BMI
    if bmi < 18.5:
        body_age += 2.0  # Underweight adds age
    elif bmi > 25.0:
        body_age += (bmi - 25.0) * 0.5  # Overweight adds age
    
    # Adjust based on body fat percentage
    if is_male:
        if fat_percentage > 25.0:
            body_age += (fat_percentage - 25.0) * 0.3
        elif fat_percentage < 10.0:
            body_age += 1.0
    else:
        if fat_percentage > 32.0:
            body_age += (fat_percentage - 32.0) * 0.3
        elif fat_percentage < 16.0:
            body_age += 1.0
    
    # Adjust based on visceral fat
    if visceral_fat > 10.0:
        body_age += (visceral_fat - 10.0) * 0.2
    
    return round(body_age, 1)


def calculate_all_evaluation_metrics(
    weight_kg: float,
    height_m: float,
    age: int,
    is_male: bool,
    skinfold_triceps: float,
    skinfold_subscapular: float,
    skinfold_subaxillary: float,
    skinfold_suprailiac: float,
    skinfold_abdominal: float,
    skinfold_quadriceps: float,
    skinfold_calf: float,
    waist_perimeter: float
) -> Dict[str, float]:
    """
    Calculate all evaluation metrics at once.
    
    Args:
        weight_kg: Weight in kilograms
        height_m: Height in meters
        age: Age in years
        is_male: True for male, False for female
        skinfold_*: All skinfold measurements in mm
        waist_perimeter: Waist perimeter in cm
    
    Returns:
        Dictionary with all calculated metrics
    """
    # Basic calculations
    bmi = calculate_bmi(weight_kg, height_m) or 0.0
    
    # Body composition
    fat_percentage = calculate_body_fat_percentage(
        age, is_male,
        skinfold_triceps, skinfold_subscapular, skinfold_subaxillary,
        skinfold_suprailiac, skinfold_abdominal, skinfold_quadriceps, skinfold_calf
    )
    
    fat_lean = calculate_fat_and_lean_weight(weight_kg, fat_percentage)
    lean_percentage = calculate_lean_mass_percentage(fat_percentage)
    
    # Advanced calculations
    basal_metabolism = calculate_basal_metabolism(weight_kg, height_m, age, is_male)
    visceral_fat = calculate_visceral_fat(waist_perimeter, height_m, age, is_male)
    body_age = calculate_body_age(age, bmi, fat_percentage, visceral_fat, is_male)
    
    return {
        'imc': bmi,
        'basal_metabolism': basal_metabolism,
        'body_age': body_age,
        'visceral_fat': visceral_fat,
        'estimated_height': height_m,  # Already have height, but keeping for consistency
        'fat_weight': fat_lean['fat_weight'],
        'lean_weight': fat_lean['lean_weight'],
        'fat_percentage': fat_percentage,
        'lean_mass_percentage': lean_percentage
    }