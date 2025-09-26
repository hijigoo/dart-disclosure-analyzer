"""
Samsung Electronics DART API Interface

This script provides a simple interface to retrieve and display 
disclosure information for Samsung Electronics from the Korean Financial 
Supervisory Service's DART system.
"""

from datetime import datetime
import json
from pathlib import Path
from config.api_config import SAMSUNG_CORP_CODE
from api import dart_api
from service import dart_service, analysis_service
from utils import date_utils, display, csv_utils, file_utils

def search_and_download_disclosure(start_date, end_date, corp_code, filter_keyword='공급'):
    """
    Main function to demonstrate Samsung Electronics disclosure retrieval
    """
    try:
        print("==== Run DART Disclosure Tool ====\n")
        
        # Validate API key first
        if not dart_api.validate_api_key():
            print("ERROR: Invalid API key or API service unavailable")
            print("Please check your API key in api_config.py")
            return

        print(f"# 공시 리스트 가져오기 - 날짜: {start_date}~{end_date}")
        disclosures = dart_service.get_disclosure_list_by_date_range(
            corp_code=corp_code,
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

        print(f"# 공시 xml 파일을 markdown으로 변경")
        xml_path = xml_files[0]
        markdown_content = analysis_service.convert_to_markdown({'raw_content': read_file_content(xml_path)['content']})

        # 마크다운 파일 경로 생성 및 저장
        markdown_path = xml_path.replace('.xml', '.md')
        save_file_content(markdown_path, markdown_content)

        print(f" - XML path: {xml_path}")
        print(f" - Markdown path: {markdown_path}\n")
        
        print(f"✅ [Tool 1 Success] XML file downloaded at: {xml_path}")
        return {
            "xml_path": xml_path,
            "markdown_path": markdown_path
        }
        
    except dart_api.DartAPIError as e:
        print(f'API Error: {e}')
    except Exception as e:
        print(f'Error: {e}')

def read_file_content(file_path: str) -> str:
    """
    주어진 파일 경로(file_path)에 있는 텍스트 파일의 내용을 읽어서 반환합니다.
    """
    try:
        with open(file_path, 'r', encoding='utf-8') as f:
            content = f.read()
        print(f"✅ [Tool 2 Success] Successfully read file: {file_path}")
        return {"content": content}
    except Exception as e:
        error_message = f"🔥 Error reading file at {file_path}: {e}"
        print(error_message)
        return error_message


def save_file_content(file_path: str, content: str) -> str:
    """
    주어진 내용(content)을 지정된 파일 경로(file_path)에 저장합니다.
    """
    try:
        # 파일의 디렉토리가 존재하는지 확인하고, 없으면 생성합니다.
        directory = Path(file_path).parent
        if not directory.exists():
            directory.mkdir(parents=True, exist_ok=True)

        with open(file_path, 'w', encoding='utf-8') as f:
            f.write(content)
        print(f"✅ [Tool 3 Success] Successfully saved content to file: {file_path}")
        return {"file_path": file_path}
    except Exception as e:
        error_message = f"🔥 Error saving content to file at {file_path}: {e}"
        print(error_message)
        return error_message
    
# if __name__ == "__main__":
#     end_date = date_utils.get_current_date()  # Today
#     start_date = '20250701'
#     search_and_download_disclosure(start_date=start_date, end_date=end_date, corp_code=SAMSUNG_CORP_CODE)