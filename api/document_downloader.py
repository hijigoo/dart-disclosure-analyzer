"""
Document Downloader Module

This module provides functions for downloading disclosure documents 
from the DART system.
"""

import time
from pathlib import Path
from api import dart_api

def get_downloads_folder():
    """
    Get the path to the project's download folder
    
    Returns:
        Path object representing the project's download folder
    """
    # Get the current working directory (project directory)
    project_dir = Path.cwd()
    
    # Create a 'download' folder in the project directory
    downloads_dir = project_dir / "download"
    
    # Check if download folder exists, if not create it
    if not downloads_dir.exists():
        try:
            downloads_dir.mkdir(parents=True, exist_ok=True)
            print(f"Created download directory in the project folder: {downloads_dir}")
        except Exception as e:
            print(f"Could not create download directory: {e}")
            # Fallback to current directory if folder creation fails
            downloads_dir = project_dir
            print(f"Using current directory instead: {downloads_dir}")
            
    return downloads_dir

def download_all_company_disclosures(corp_code, days_back=30):
    """
    Download all recent disclosure documents for a company
    
    Args:
        corp_code: Company code
        days_back: How many days back to search (default: 30)
        
    Returns:
        Tuple of (successful_downloads, failed_downloads)
    """
    # Get list of recent disclosures
    disclosures = dart_api.get_disclosure_list(corp_code, days_back)
    
    if not disclosures:
        print("No disclosure documents found.")
        return [], []
    
    print(f"\nDownloading {len(disclosures)} disclosure documents...")
    
    # Track downloads
    successful = []
    failed = []
    
    # Download each disclosure document
    for i, disclosure in enumerate(disclosures, 1):
        rcept_no = disclosure.get('rcept_no')
        report_name = disclosure.get('report_nm', '').strip()
        
        print(f"\n[{i}/{len(disclosures)}] Downloading: {report_name} (Receipt #{rcept_no})")
        
        try:
            # Add a short delay between downloads to avoid rate limiting
            if i > 1:
                time.sleep(1)
                
            download_path = dart_api.download_document(rcept_no)
            if download_path:
                successful.append((report_name, download_path))
            else:
                failed.append((report_name, rcept_no))
        except Exception as e:
            print(f"Error downloading document: {e}")
            failed.append((report_name, rcept_no))
    
    return successful, failed