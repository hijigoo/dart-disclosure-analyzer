"""
Samsung Electronics DART API Interface

This script provides a simple interface to retrieve and display 
disclosure information for Samsung Electronics from the Korean Financial 
Supervisory Service's DART system.
"""

from datetime import datetime
import json
from config.api_config import SAMSUNG_CORP_CODE
from api import dart_api
from service import dart_service, analysis_service
from utils import date_utils, display, csv_utils, file_utils

def find_and_download_disclosure(start_date, end_date, filter_keyword='공급'):
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
        # print("Fetching recent disclosures for Samsung Electronics...")

        # end_date = date_utils.get_current_date()  # Today
        # start_date = date_utils.get_january_first()  # Start Date
        # start_date = '20250701'


        print(f"# 공시 리스트 가져오기 - 날짜: {start_date}~{end_date}")
        disclosures = dart_service.get_disclosure_list_by_date_range(
            corp_code=SAMSUNG_CORP_CODE,
            start_date=start_date,
            end_date=end_date,
            page_count=100,
            pblntf_ty='I'
        )
        print()
        
        # Display the results using the display module
        print(f"# 공시 리스트 출력")
        display.display_recent_disclosures(disclosures)
        print()

        # Download the results using the csv module
        current_time = datetime.now().strftime("%Y%m%d")
        filename = f"disclosures_{current_time}_{start_date}_{end_date}"
        disc_list_file_path = csv_utils.save_disclosures_to_csv(disclosures=disclosures, filename=filename)

        # Get filtered row 
        filter_column_name = 'report_nm'
        # filter_keyword = '공급'
        filtered_disc=csv_utils.read_csv_filter_to_json(
            file_path=disc_list_file_path,
            column_name=filter_column_name,
            keyword=filter_keyword)
        
        # Get latest row
        latest_disc = csv_utils.get_latest_by_rcept_dt(data=filtered_disc)

        # Print JSON with nice formatting (indent=2)
        print(f"# 최신 공시 출력 - 날짜: {start_date}~{end_date}, 키워드: {filter_keyword} ")
        print(json.dumps(latest_disc, indent=2, ensure_ascii=False))
        print()

        rcept_no = latest_disc['rcept_no']
        print(f"# 공시 번호")
        print(f" - rcept_no: {rcept_no}\n")

        print(f"# 공시 다운로드 ")
        saved_path = dart_service.download_disclosure_document(rcept_no=rcept_no)
        print(f" - path: {saved_path}\n")

        # 기본 사용법 (압축 해제 후 추출된 파일 위치 반환)
        print(f"# 공시 압축 해제 ")
        extracted_dir = file_utils.extract_zip_file(saved_path, delete_zip=True)
        xml_files = file_utils.list_extracted_files(extract_path=extracted_dir, extensions=['.xml'])
        print(f" - path: {xml_files[0]}\n")

        print(f"# 공시 xml 파일을 markdown으로 변경 ")
        xml_file_path = xml_files[0]
        markdown_path = analysis_service.xml_to_markdown(xml_file_path)
        print(f" - markdown path: {markdown_path}\n")


    except dart_api.DartAPIError as e:
        print(f'API Error: {e}')
    except Exception as e:
        print(f'Error: {e}')

if __name__ == "__main__":
    end_date = date_utils.get_current_date()  # Today
    start_date = '20250701'
    find_and_download_disclosure(start_date=start_date, end_date=end_date)