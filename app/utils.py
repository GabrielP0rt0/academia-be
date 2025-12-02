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
