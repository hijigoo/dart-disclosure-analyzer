"""
Date Utility Functions

This module provides utility functions for date handling and formatting,
specifically for use with the DART API which uses YYYYMMDD date format.
"""

from datetime import datetime, timedelta

def get_current_date():
    """
    Get current date in YYYYMMDD format
    
    Returns:
        String: Current date in YYYYMMDD format
    """
    now = datetime.now()
    return now.strftime('%Y%m%d')

def get_date_before(days):
    """
    Get date N days before in YYYYMMDD format
    
    Args:
        days: Number of days to go back
        
    Returns:
        String: Date in YYYYMMDD format
    """
    date = datetime.now() - timedelta(days=days)
    return date.strftime('%Y%m%d')

def format_date(date_str):
    """
    Format YYYYMMDD to YYYY-MM-DD
    
    Args:
        date_str: Date in YYYYMMDD format
        
    Returns:
        String: Date in YYYY-MM-DD format
    """
    if len(date_str) == 8:
        return f"{date_str[0:4]}-{date_str[4:6]}-{date_str[6:8]}"
    return date_str

def get_year_month_day(date_str):
    """
    Extract year, month, day from YYYYMMDD format
    
    Args:
        date_str: Date in YYYYMMDD format
        
    Returns:
        Tuple: (year, month, day) as integers
    """
    if len(date_str) == 8:
        year = int(date_str[0:4])
        month = int(date_str[4:6])
        day = int(date_str[6:8])
        return year, month, day
    return None

def is_date_between(date_str, start_date_str, end_date_str):
    """
    Check if a date is between two dates
    
    Args:
        date_str: Date to check in YYYYMMDD format
        start_date_str: Start date in YYYYMMDD format
        end_date_str: End date in YYYYMMDD format
        
    Returns:
        Boolean: True if date is between start and end dates
    """
    try:
        date = datetime.strptime(date_str, '%Y%m%d')
        start_date = datetime.strptime(start_date_str, '%Y%m%d')
        end_date = datetime.strptime(end_date_str, '%Y%m%d')
        return start_date <= date <= end_date
    except ValueError:
        return False