"""
Samsung Electronics DART API Interface

This script provides a simple interface to retrieve and display 
disclosure information for Samsung Electronics from the Korean Financial 
Supervisory Service's DART system.
"""

from api.api_config import SAMSUNG_CORP_CODE
from api import dart_api
from display import display
from utils import date_utils

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
        disclosures = dart_api.get_disclosure_list(SAMSUNG_CORP_CODE, 30)
        
        # Display the results using the display module
        display.display_recent_disclosures(disclosures)
        
    except dart_api.DartAPIError as e:
        print(f'API Error: {e}')
    except Exception as e:
        print(f'Error: {e}')

if __name__ == "__main__":
    main()