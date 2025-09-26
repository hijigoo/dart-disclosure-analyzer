"""
Display Utility Module

This module provides functions for displaying Samsung Electronics financial
and disclosure information in a user-friendly format.
"""

from utils import date_utils

def format_number(number_str):
    """
    Format large numbers with commas for readability

    Args:
        number_str: Number as a string, possibly with existing commas

    Returns:
        Formatted number with commas as thousands separators
    """
    try:
        # Remove any existing commas before converting to int
        clean_str = number_str.replace(',', '')
        return f"{int(clean_str):,}"
    except (ValueError, TypeError):
        return number_str

def display_recent_disclosures(disclosures):
    """
    Display a list of recent disclosures

    Args:
        disclosures: List of disclosure document metadata

    Returns:
        The same disclosure list for chaining
    """
    if not disclosures:
        print("No recent disclosures found.")
        return []

    print("\n==== Recent Disclosure Documents ====")
    for idx, doc in enumerate(disclosures, 1):
        corp_name = doc.get('corp_name', 'N/A')
        report_nm = doc.get('report_nm', 'N/A')
        rcept_dt = doc.get('rcept_dt', 'N/A')
        rcept_no = doc.get('rcept_no', 'N/A')

        print(f"\n{idx}. {report_nm}")
        print(f"   Company: {corp_name}")
        print(f"   Date: {date_utils.format_date(rcept_dt)}")
        print(f"   Receipt No: {rcept_no}")

    return disclosures

def display_download_summary(downloaded_files, failed_downloads, total_count):
    """
    Display a summary of downloaded disclosure documents

    Args:
        downloaded_files: List of tuples (report_name, file_path) for successful downloads
        failed_downloads: List of tuples (report_name, rcept_no) for failed downloads
        total_count: Total number of attempted downloads
    """
    print("\n===== DOWNLOAD SUMMARY =====")
    print(f"Successfully downloaded: {len(downloaded_files)}/{total_count}")

    if downloaded_files:
        print("\nDownloaded files:")
        for name, path in downloaded_files:
            print(f"  - {name}: {path}")

    if failed_downloads:
        print("\nFailed downloads:")
        for name, rcept_no in failed_downloads:
            print(f"  - {name} (Receipt #{rcept_no})")

    if downloaded_files:
        print("You can view the disclosures by extracting the downloaded ZIP files.")