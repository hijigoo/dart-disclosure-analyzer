"""
Samsung Electronics Financial and Disclosure Information Tool

This script retrieves and displays the latest financial information and 
disclosure documents for Samsung Electronics from the Korean Financial 
Supervisory Service's DART system.
"""

from api.api_config import SAMSUNG_CORP_CODE
from api import dart_api, report_period, document_downloader
from display import display

def main():
    """Main function for Samsung disclosure details tool"""
    try:
        print("==== Samsung Electronics Financial Information Tool ====")
        
        # Check if the API key is valid
        if not dart_api.validate_api_key():
            print("ERROR: Invalid API key or API service unavailable")
            print("Please check your API key in api_config.py")
            return
        
        # Part 1: Fetch financial highlights
        print("\n===== PART 1: FINANCIAL HIGHLIGHTS =====")
        # Get the latest likely available report period
        year, report_code, report_name = report_period.get_latest_available_report_period()
        
        print(f"Fetching {year} {report_name} (code: {report_code}) for Samsung Electronics...")
        
        # Try to fetch the latest report
        financial_data = dart_api.get_financial_statement(SAMSUNG_CORP_CODE, year, report_code)
        display.display_financial_highlights(financial_data)
        
        # Part 2: Fetch recent disclosures
        print("\n===== PART 2: RECENT DISCLOSURES =====")
        recent_disclosures = dart_api.get_disclosure_list(SAMSUNG_CORP_CODE, days_back=30)
        displayed_disclosures = display.display_recent_disclosures(recent_disclosures)
        
        # Part 3: Download all disclosure documents
        if displayed_disclosures and len(displayed_disclosures) > 0:
            print("\n===== PART 3: DOWNLOAD ALL DISCLOSURE DOCUMENTS =====")
            
            # Download all disclosure documents
            downloaded_files, failed_downloads = document_downloader.download_all_company_disclosures(
                SAMSUNG_CORP_CODE, days_back=30
            )
            
            # Show summary of downloads
            display.display_download_summary(
                downloaded_files, 
                failed_downloads, 
                len(displayed_disclosures)
            )
        
    except dart_api.DartAPIError as e:
        print(f'API Error: {e}')
    except Exception as e:
        print(f'Error: {e}')

if __name__ == "__main__":
    main()