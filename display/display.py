"""
Samsung Display Module

This module provides functions for displaying Samsung Electronics financial 
and disclosure information in a user-friendly format.
"""

import sys
sys.path.append('/Users/kichul/Documents/project/dart-disclosure-viewer')
from api import dart_api, report_period, document_downloader
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

def display_financial_highlights(financial_data):
    """
    Display key financial information from a business report
    
    Args:
        financial_data: List of financial data items
    """
    if not financial_data or not isinstance(financial_data, list):
        print("No financial data available to display")
        return
    
    # Mapping of DART account IDs to display names
    # Adding alternate account IDs to improve matching chances
    key_items = {
        # Revenue/Sales
        'ifrs-full_Revenue': 'Revenue',
        'dart_Revenue': 'Revenue',
        'ifrs_Revenue': 'Revenue',
        'dart_TotalSales': 'Revenue',
        
        # Profits
        'ifrs-full_ProfitLoss': 'Net Income',
        'dart_ProfitLoss': 'Net Income',
        'ifrs_ProfitLoss': 'Net Income',
        'ifrs-full_OperatingProfit': 'Operating Profit',
        'dart_OperatingIncomeLoss': 'Operating Profit',
        'ifrs_OperatingIncomeLoss': 'Operating Profit',
        
        # Assets/Liabilities
        'ifrs-full_Assets': 'Total Assets',
        'dart_Assets': 'Total Assets', 
        'ifrs_Assets': 'Total Assets',
        'ifrs-full_Liabilities': 'Total Liabilities',
        'dart_Liabilities': 'Total Liabilities',
        'ifrs_Liabilities': 'Total Liabilities',
        'ifrs-full_Equity': 'Total Equity',
        'dart_Equity': 'Total Equity',
        'ifrs_Equity': 'Total Equity',
        
        # Per share metrics
        'ifrs-full_BasicEarningsLossPerShare': 'EPS',
        'dart_BasicEarningsLossPerShare': 'EPS',
        'ifrs_BasicEarningsLossPerShare': 'EPS'
    }
    
    # Get report period information
    reprt_code = financial_data[0].get('reprt_code', 'Unknown')
    report_name = report_period.REPORT_CODE_MAP.get(reprt_code, 'Unknown Report')
    
    # Dictionary to store the latest values for each key item
    latest_values = {}
    matched_items = {}
    
    # Process all items and keep only the latest or relevant ones
    for item in financial_data:
        account_id = item.get('account_id', '')
        account_nm = item.get('account_nm', '')
        
        # Try to find the corresponding key item
        if account_id in key_items:
            item_name = key_items[account_id]
            value = item.get('thstrm_amount', '0')
            
            # Store the item for later reference
            if item_name not in matched_items:
                matched_items[item_name] = item
                
            # Convert to int for comparison, handling commas
            try:
                clean_value = value.replace(',', '')
                current_value = int(clean_value) if clean_value else 0
                
                # If we already have this item, only replace if the new value is greater
                if item_name not in latest_values:
                    latest_values[item_name] = value
                else:
                    existing = latest_values[item_name].replace(',', '')
                    existing_value = int(existing) if existing else 0
                    
                    if current_value > existing_value:
                        latest_values[item_name] = value
            except (ValueError, AttributeError):
                # If conversion fails, just use the new value
                latest_values[item_name] = value
    
    # Display the financial highlights
    print(f"\n==== Financial Highlights: {report_name} ====")
    print(f"Report period: {financial_data[0].get('bsns_year', '')}")
    print(f"Currency: KRW")
    print("-" * 30)
    
    # Check if we found any key items
    if not latest_values:
        print("No key financial metrics found in the data")
        
        # Show available account IDs for debugging
        print("\nAvailable account IDs in the data:")
        unique_accounts = {}
        for item in financial_data[:10]:  # Show first 10 for brevity
            acc_id = item.get('account_id', '')
            if acc_id and acc_id not in unique_accounts:
                unique_accounts[acc_id] = item.get('account_nm', '')
        
        for acc_id, acc_name in unique_accounts.items():
            print(f"{acc_id}: {acc_name}")
        return
    
    # Display financial metrics
    for item_name, value in latest_values.items():
        print(f"{item_name}: {format_number(value)} KRW")
    
    # Compare with previous period if available
    print("\n==== Year-over-Year Change ====")
    for item_name in latest_values:
        if item_name in matched_items:
            item = matched_items[item_name]
            
            current = item.get('thstrm_amount', '0')
            previous = item.get('frmtrm_amount', '0')
            
            try:
                current_val = int(current.replace(',', '')) if current else 0
                prev_val = int(previous.replace(',', '')) if previous else 0
                
                if prev_val != 0:
                    change_pct = ((current_val - prev_val) / abs(prev_val)) * 100
                    direction = '↑' if change_pct >= 0 else '↓'
                    print(f"{item_name}: {abs(change_pct):.2f}% {direction}")
                else:
                    print(f"{item_name}: N/A (previous value is zero)")
            except (ValueError, AttributeError):
                print(f"{item_name}: N/A (could not calculate)")
        else:
            print(f"{item_name}: N/A (no matching data)")

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
        print(f"\nAll files were downloaded to: {document_downloader.get_downloads_folder()}")
        print("You can view the disclosures by extracting the downloaded ZIP files.")