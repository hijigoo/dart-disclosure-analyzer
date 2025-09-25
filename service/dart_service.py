"""
DART API Service Layer

This module provides higher-level services on top of the basic DART API functions,
such as date range based fetching with optimized API calls.
"""

import time
import os
from datetime import datetime, timedelta
from pathlib import Path
from api.dart_api import get_disclosure_list, download_document, DartAPIError

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


def download_disclosure_document(rcept_no, download_dir=None, filename=None):
    """
    Download disclosure document by receipt number with enhanced directory handling.
    This is a service-layer wrapper around the dart_api.download_document function.

    Args:
        rcept_no: Receipt number of the disclosure to download
        download_dir: Custom directory to save the document (optional)
        filename: Custom filename for the downloaded document (optional)

    Returns:
        str: Path to the downloaded file or None if download failed
    """
    try:
        # Create full save_path if both download_dir and filename are provided
        save_path = None

        if download_dir and filename:
            # Create Path object for the download directory
            download_dir_path = Path(download_dir)

            # Create directory if it doesn't exist
            if not download_dir_path.exists():
                download_dir_path.mkdir(parents=True, exist_ok=True)
                # print(f"Created download directory at {download_dir_path}")

            # Combine directory and filename
            save_path = download_dir_path / filename

        elif download_dir:
            # If only directory is provided, let the API function handle the filename
            download_dir_path = Path(download_dir)

            # Create directory if it doesn't exist
            if not download_dir_path.exists():
                download_dir_path.mkdir(parents=True, exist_ok=True)
                # print(f"Created download directory at {download_dir_path}")

            # Create default filename with receipt number
            default_filename = f"disclosure_{rcept_no}.zip"
            save_path = download_dir_path / default_filename

        elif filename:
            # If only filename is provided, use default directory
            save_path = filename

        # Call the API function to download the document
        result = download_document(rcept_no=rcept_no, save_path=save_path)

        if result:
            # print(f"Document downloaded successfully: {result}")
            return result
        else:
            print(f"Failed to download document for receipt number: {rcept_no}")
            return None

    except Exception as e:
        print(f"Error downloading disclosure document: {str(e)}")
        return None