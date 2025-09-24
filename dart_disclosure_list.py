"""
Samsung Electronics DART API Interface

This script provides a simple interface to retrieve and display 
disclosure information for Samsung Electronics from the Korean Financial 
Supervisory Service's DART system.
"""

from config.api_config import SAMSUNG_CORP_CODE
from api import dart_api
from service import dart_service
from utils import date_utils, display, csv_utils

def main():
    """
    Main function to demonstrate Samsung Electronics disclosure retrieval
    """
    try:
        print("==== Samsung Electronics DART Disclosure Tool ====\n")
        
        # Validate API key first
        if not dart_api.validate_api_key():
            print("ERROR: Invalid API key or API service unavailable")
            print("Please check your API key in api_config.py")
            return
            
        # Fetch Samsung disclosures from the last 30 days
        print("Fetching recent disclosures for Samsung Electronics...")

        end_date = date_utils.get_current_date()  # Today
        start_date = date_utils.get_january_first()  # Start Date

        disclosures = dart_service.get_disclosure_list_by_date_range(
            corp_code=SAMSUNG_CORP_CODE,
            start_date=start_date,
            end_date=end_date,
            page_count=100,
            pblntf_ty='I'
        )
        
        # Display the results using the display module
        display.display_recent_disclosures(disclosures)
        # Download the results using the csv module
        csv_utils.save_disclosures_to_csv(disclosures=disclosures)

    except dart_api.DartAPIError as e:
        print(f'API Error: {e}')
    except Exception as e:
        print(f'Error: {e}')

if __name__ == "__main__":
    main()