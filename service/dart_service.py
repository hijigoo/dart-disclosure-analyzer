"""
DART API Service Layer

This module provides higher-level services on top of the basic DART API functions,
such as date range based fetching with optimized API calls.
"""

import time
from datetime import datetime, timedelta
from api.dart_api import get_disclosure_list, DartAPIError

def get_disclosure_list_by_date_range(corp_code, start_date, end_date, page_count=100, pblntf_ty=None):
    """
    Fetch a list of disclosures for a specific company over a date range,
    collecting them week by week to ensure comprehensive results.

    Args:
        corp_code: Company code
        start_date: Start date in YYYYMMDD format
        end_date: End date in YYYYMMDD format
        page_count: Maximum number of results per week (default: 100)

    Returns:
        List of all disclosure documents from start_date to end_date
    """
    # Convert date strings to datetime objects for iteration
    start_dt = datetime.strptime(str(start_date), '%Y%m%d')
    end_dt = datetime.strptime(str(end_date), '%Y%m%d')

    # Initialize list to collect all disclosures
    all_disclosures = []

    # Create a timedelta of 7 days (one week) to iterate through each week
    one_week = timedelta(days=7)
    current_dt = start_dt

    print(f"Fetching disclosures from {start_date} to {end_date} week by week...")

    # Iterate through the date range by weekly chunks
    while current_dt <= end_dt:
        # Calculate end date for this week (either 7 days later or the final end date, whichever is sooner)
        week_end_dt = min(current_dt + one_week - timedelta(days=1), end_dt)

        # Format dates to YYYYMMDD string format
        week_start_str = current_dt.strftime('%Y%m%d')
        week_end_str = week_end_dt.strftime('%Y%m%d')

        try:
            # Fetch disclosures for this specific week
            print(f"Fetching disclosures for week {week_start_str} to {week_end_str}...")

            weekly_disclosures = get_disclosure_list(
                corp_code=corp_code,
                start_date=week_start_str,
                end_date=week_end_str,
                page_count=page_count,
                pblntf_ty=pblntf_ty
            )

            # If we got any results, add them to our collection
            if weekly_disclosures:
                print(f"Found {len(weekly_disclosures)} disclosures for week {week_start_str} to {week_end_str}")
                all_disclosures.extend(weekly_disclosures)
            else:
                print(f"No disclosures found for week {week_start_str} to {week_end_str}")

            # Add a small delay to avoid hitting API rate limits
            time.sleep(0.5)

        except DartAPIError as e:
            print(f"Error fetching disclosures for week {week_start_str} to {week_end_str}: {str(e)}")
            # Continue to the next week even if there's an error

        # Move to the next week
        current_dt += one_week

    print(f"Total disclosures collected: {len(all_disclosures)}")
    return all_disclosures