import requests
import json
import time
import os
from pathlib import Path
from datetime import datetime, timedelta
from utils import date_utils
from config.api_config import API_KEY

# OpenDART API status codes
DART_STATUS_CODES = {
    '000': 'Normal',
    '010': 'Invalid API key',
    '011': 'API key usage limit exceeded',
    '013': 'Requested data not found',
    '020': 'Required parameter missing',
    '100': 'Invalid parameter value',
    '800': 'System maintenance',
    '900': 'System error'
}


# DART report code mappings (now imported from report_period module)
from api.report_period import REPORT_CODE_MAP

# Base URL for all API calls
BASE_URL = 'https://opendart.fss.or.kr/api'

class DartAPIError(Exception):
    """Custom exception for OpenDART API errors"""
    pass


# 고유번호 개발가이드
# https://opendart.fss.or.kr/guide/detail.do?apiGrpCd=DS001&apiId=2019018
def validate_api_key():
    """
    Validate that the API key is working correctly
    
    Returns:
        bool: True if API key is valid, False otherwise
    """
    url = f'{BASE_URL}/corpCode.xml'
    
    params = {
        'crtfc_key': API_KEY
    }
    
    try:
        # Print the API key being used (first few and last few characters)
        key_start = API_KEY[:4] 
        key_end = API_KEY[-4:]
        # print(f"Using API key: {key_start}...{key_end}")
        
        # Try a simple API request to validate the key
        response = requests.get(url, params=params, timeout=10)
        # print(f"API response status code: {response.status_code}")
        
        if response.status_code == 200:
            # The corpCode.xml endpoint returns XML data, not JSON
            # Just check if we got a successful response without errors
            return True
            
        return False
    except Exception as e:
        print(f"Error validating API key: {str(e)}")
        return False


# 공시검색 개발가이드
# https://opendart.fss.or.kr/guide/detail.do?apiGrpCd=DS001&apiId=2019001
def get_disclosure_list(corp_code, start_date=20250901, end_date=20250931, page_count=100, pblntf_ty=None):
    """
    Fetch a list of recent disclosures for a specific company
    
    Args:
        corp_code: Company code
        days_back: How many days back to search (default: 30)
        pblntf_ty: 공시 유형
    Returns:
        List of disclosure documents
    """
    url = f'{BASE_URL}/list.json'
    
    # Calculate date range (from X days ago until today)
    # end_date = date_utils.get_current_date()  # Today in YYYYMMDD format
    # start_date = date_utils.get_date_before(days_back)
    
    params = {
        'crtfc_key': API_KEY,
        'corp_code': corp_code,
        'bgn_de': start_date,
        'end_de': end_date,
        'page_count': page_count  # Allow up to 100 results
    }
    
    if pblntf_ty:
        params['pblntf_ty'] = pblntf_ty

    # print(f"Fetching disclosures from {start_date} to {end_date}...")
    
    response = requests.get(url, params=params, timeout=10)
    
    if response.status_code == 200:
        data = response.json()
        if data['status'] == '000':
            if 'list' in data and data['list']:
                return data['list']
            else:
                print("No disclosure documents found in the specified date range.")
                return []
        else:
            error_desc = DART_STATUS_CODES.get(data['status'], 'Unknown error')
            raise DartAPIError(f"API Error [{data['status']}]: {data.get('message', error_desc)}")
    else:
        raise DartAPIError(f'Failed to load disclosure list: {response.status_code}')


# 단일회사 전체 재무제표 개발가이드
# https://opendart.fss.or.kr/guide/detail.do?apiGrpCd=DS003&apiId=2019020
def get_financial_statement(corp_code, bsns_year, reprt_code, fs_div='CFS', max_retries=3):
    """
    Fetch financial statement information for a company
    
    Args:
        corp_code: Company code
        bsns_year: Business year (e.g., '2023')
        reprt_code: Report code
            - '11011': Annual report
            - '11012': Half-yearly report
            - '11013': Q1 report
            - '11014': Q3 report
        fs_div: Financial statement division (default: 'CFS')
            - CFS: Consolidated Financial Statement (연결재무제표)
            - OFS: Separate Financial Statement (별도재무제표)
        max_retries: Maximum number of retry attempts (default: 3)
        
    Returns:
        Dictionary containing financial statement information
    """
    url = f'{BASE_URL}/fnlttSinglAcntAll.json'
    
    # Map report codes to correct values according to API documentation
    report_code_mapping = {
        # Original code: API expected code
        '11011': '11011',  # Annual report
        '11012': '11012',  # Half-yearly report
        '11013': '11013',  # Q1 report
        '11014': '11014',  # Q3 report
    }
    
    # Use the mapped report code if available, otherwise use the original
    api_reprt_code = report_code_mapping.get(reprt_code, reprt_code)
    
    params = {
        'crtfc_key': API_KEY,
        'corp_code': corp_code,
        'bsns_year': bsns_year,
        'reprt_code': api_reprt_code,
        'fs_div': fs_div
    }
    
    # Print request details for debugging
    print(f"Request URL: {url}")
    print(f"Parameters: corp_code={corp_code}, year={bsns_year}, report_code={api_reprt_code}, fs_div={fs_div}")
    
    # Retry mechanism for temporary failures
    retries = 0
    while retries < max_retries:
        try:
            response = requests.get(url, params=params, timeout=10)
            
            if response.status_code == 200:
                data = response.json()
                if data['status'] == '000':
                    if 'list' not in data or not data['list']:
                        raise DartAPIError("API returned empty result set")
                    return data['list']
                else:
                    # Get more descriptive error message based on status code
                    error_desc = DART_STATUS_CODES.get(data['status'], 'Unknown error')
                    error_msg = data.get('message', error_desc)
                    raise DartAPIError(f"API Error [{data['status']}]: {error_msg}")
            elif response.status_code == 429:  # Too Many Requests
                retries += 1
                if retries < max_retries:
                    # Exponential backoff (wait 1s, then 2s, then 4s, etc.)
                    wait_time = 2 ** (retries - 1)
                    print(f"Rate limit reached, retrying in {wait_time} seconds...")
                    time.sleep(wait_time)
                    continue
                else:
                    raise DartAPIError(f"API rate limit exceeded after {max_retries} attempts")
            else:
                raise DartAPIError(f"HTTP Error: {response.status_code}")
        except requests.exceptions.RequestException as e:
            retries += 1
            if retries < max_retries:
                wait_time = 2 ** (retries - 1)
                print(f"Network error, retrying in {wait_time} seconds... Error: {str(e)}")
                time.sleep(wait_time)
            else:
                raise DartAPIError(f"Network error after {max_retries} attempts: {str(e)}")
    
    raise DartAPIError(f"Failed to load business report after {max_retries} attempts")



def download_document(rcept_no, save_path=None):
    """
    Download the original disclosure document as a zip file

    Args:
        rcept_no: The receipt number of the disclosure document
        save_path: Path to save the downloaded file (optional)

    Returns:
        Path to the saved file or None if download failed
    """
    from api.document_downloader import get_downloads_folder
    url = f'{BASE_URL}/document.xml'
    
    params = {
        'crtfc_key': API_KEY,
        'rcept_no': rcept_no
    }
    
    try:
        response = requests.get(url, params=params, timeout=30, stream=True)
        
        if response.status_code == 200:
            # Create a default filename if not provided
            if not save_path:
                download_dir = get_downloads_folder()
                filename = f"disclosure_{rcept_no}.zip"
                save_path = download_dir / filename
            else:
                # If save_path is provided but it's just a filename, add Downloads path
                save_path = Path(save_path)
                if not save_path.is_absolute():
                    save_path = get_downloads_folder() / save_path
            
            # Create parent directories if they don't exist
            save_path.parent.mkdir(parents=True, exist_ok=True)
                
            # Save the file
            with open(save_path, 'wb') as f:
                for chunk in response.iter_content(chunk_size=8192):
                    if chunk:
                        f.write(chunk)
                        
            # print(f"Document successfully downloaded to: {save_path}")
            return str(save_path)
        else:
            print(f"Failed to download document: HTTP {response.status_code}")
            return None
    except Exception as e:
        print(f"Error downloading document: {str(e)}")
        return None
