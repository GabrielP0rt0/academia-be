"""
Database layer - JSON file operations with locks and backups.

This module provides thread-safe read/write operations for JSON files,
with automatic backups and atomic writes to prevent data corruption.
"""
import json
import os
import shutil
import threading
from pathlib import Path
from typing import Any, List, Dict
from datetime import datetime


# Base directory for data files
BASE_DIR = Path(__file__).parent
DATA_DIR = BASE_DIR / "data"
BACKUPS_DIR = DATA_DIR / "backups"

# Ensure directories exist
DATA_DIR.mkdir(parents=True, exist_ok=True)
BACKUPS_DIR.mkdir(parents=True, exist_ok=True)

# Dictionary to store locks for each file
_file_locks: Dict[str, threading.Lock] = {}
_locks_lock = threading.Lock()


def _get_lock(filepath: str) -> threading.Lock:
    """Get or create a lock for a specific file."""
    with _locks_lock:
        if filepath not in _file_locks:
            _file_locks[filepath] = threading.Lock()
        return _file_locks[filepath]


def _get_file_path(filename: str) -> Path:
    """Get full path for a data file."""
    return DATA_DIR / filename


def _get_backup_path(filename: str) -> Path:
    """Get backup file path (.bak)."""
    return DATA_DIR / f"{filename}.bak"


def _create_timestamped_backup(filename: str) -> Path:
    """Create a timestamped backup in backups directory."""
    timestamp = datetime.now().strftime("%Y%m%d_%H%M%S")
    backup_name = f"{filename}.{timestamp}.bak"
    return BACKUPS_DIR / backup_name


def read_json_file(filename: str) -> List[Dict[str, Any]]:
    """
    Read JSON file with lock protection.
    
    Returns empty list if file doesn't exist or is corrupted.
    Attempts to restore from .bak if main file is corrupted.
    """
    filepath = _get_file_path(filename)
    lock = _get_lock(str(filepath))
    
    with lock:
        # If file doesn't exist, return empty list
        if not filepath.exists():
            return []
        
        try:
            with open(filepath, 'r', encoding='utf-8') as f:
                data = json.load(f)
                # Ensure it's a list
                if not isinstance(data, list):
                    return []
                return data
        except (json.JSONDecodeError, IOError) as e:
            # Try to restore from backup
            backup_path = _get_backup_path(filename)
            if backup_path.exists():
                try:
                    with open(backup_path, 'r', encoding='utf-8') as f:
                        data = json.load(f)
                        # Restore the backup
                        with open(filepath, 'w', encoding='utf-8') as out:
                            json.dump(data, out, ensure_ascii=False, indent=2)
                        return data if isinstance(data, list) else []
                except Exception:
                    pass
            
            # If all fails, return empty list
            return []


def write_json_file(filename: str, data: List[Dict[str, Any]]) -> None:
    """
    Write JSON file atomically with lock protection and automatic backup.
    
    Process:
    1. Create backup of current file (.bak)
    2. Create timestamped backup in backups/ directory
    3. Write to temporary file
    4. Rename temp file to final file (atomic operation)
    """
    filepath = _get_file_path(filename)
    lock = _get_lock(str(filepath))
    
    with lock:
        # Validate data is a list
        if not isinstance(data, list):
            raise ValueError("Data must be a list")
        
        # Create backup if file exists
        if filepath.exists():
            backup_path = _get_backup_path(filename)
            try:
                shutil.copy2(filepath, backup_path)
            except Exception:
                pass  # Continue even if backup fails
            
            # Create timestamped backup
            try:
                timestamped_backup = _create_timestamped_backup(filename)
                shutil.copy2(filepath, timestamped_backup)
            except Exception:
                pass  # Continue even if timestamped backup fails
        
        # Write to temporary file first
        temp_filepath = filepath.with_suffix(filepath.suffix + '.tmp')
        
        try:
            with open(temp_filepath, 'w', encoding='utf-8') as f:
                json.dump(data, f, ensure_ascii=False, indent=2)
            
            # Atomic rename (works on most systems)
            temp_filepath.replace(filepath)
        except Exception as e:
            # Clean up temp file if something went wrong
            if temp_filepath.exists():
                try:
                    temp_filepath.unlink()
                except Exception:
                    pass
            raise


def restore_from_backup(filename: str) -> bool:
    """
    Manually restore a file from its .bak backup.
    
    Returns True if restoration was successful, False otherwise.
    """
    filepath = _get_file_path(filename)
    backup_path = _get_backup_path(filename)
    lock = _get_lock(str(filepath))
    
    with lock:
        if not backup_path.exists():
            return False
        
        try:
            # Validate backup file is valid JSON
            with open(backup_path, 'r', encoding='utf-8') as f:
                data = json.load(f)
            
            # Restore the backup
            with open(filepath, 'w', encoding='utf-8') as out:
                json.dump(data, out, ensure_ascii=False, indent=2)
            return True
        except Exception:
            return False


def ensure_file_exists(filename: str) -> None:
    """Ensure a JSON file exists with empty list if it doesn't."""
    filepath = _get_file_path(filename)
    if not filepath.exists():
        write_json_file(filename, [])
