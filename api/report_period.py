"""
Report Period Module

This module provides functions for determining and managing report periods
for financial statement data from DART.
"""

from utils import date_utils

# DART report code mappings
REPORT_CODE_MAP = {
    '11011': 'Annual Report',
    '11012': 'Half-yearly Report',
    '11013': 'Q1 Report',
    '11014': 'Q3 Report'
}

def get_latest_available_report_period():
    """
    Determine the latest available financial report period
    
    Returns:
        Tuple of (year, report_code, report_name)
    """
    # Get current date in YYYYMMDD format
    current_date_str = date_utils.get_current_date()
    
    # Extract year and month
    year_month_day = date_utils.get_year_month_day(current_date_str)
    if not year_month_day:
        # Fallback if parsing fails
        from datetime import datetime
        current_date = datetime.now()
        current_year = current_date.year
        current_month = current_date.month
    else:
        current_year, current_month, _ = year_month_day
    
    # Determine the latest likely available report based on the current date
    # Financial reports are typically released with some delay after the period ends
    
    # Annual reports (사업보고서) are typically available by March of the following year
    if current_month >= 3:
        # After March, annual report from previous year should be available
        return str(current_year - 1), '11011', 'Annual Report'
    elif current_month >= 11:
        # Q3 report (3분기보고서) typically available by November
        return str(current_year), '11014', 'Q3 Report'
    elif current_month >= 8:
        # Half-yearly report (반기보고서) typically available by August
        return str(current_year), '11012', 'Half-yearly Report'
    elif current_month >= 5:
        # Q1 report (1분기보고서) typically available by May
        return str(current_year), '11013', 'Q1 Report'
    else:
        # Default to previous year's annual report if early in the year
        return str(current_year - 1), '11011', 'Annual Report'