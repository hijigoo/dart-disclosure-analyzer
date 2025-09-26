# DART 공시정보 조회 프로그램

이 프로그램은 DART(전자공시시스템) API를 활용하여 기업의 공시정보를 조회하는 Python 스크립트입니다.

## 소개

이 프로젝트는 OpenDART API를 통해 기업의 다음과 같은 정보를 조회합니다:

1. 최근 공시 목록
2. 상세 공시 정보
3. 재무 하이라이트

## 클래스 다이어그램

- 프로젝트가 발전함에 따라 향후 추가 예정

## 설치 방법

### 필수 요구사항

- Python 3.6 이상
- requests 라이브러리
- langchain 라이브러리
- boto3 (AWS Bedrock API 연동용)
- zipfile (공시 문서 압축 해제용)

### 설치

#### 가상환경 사용 (권장)

1. 이 저장소를 클론하거나 다운로드합니다.
2. 가상환경을 생성하고 활성화합니다:

```bash
# 가상환경 생성
python3 -m venv .venv

# 가상환경 활성화 (Linux/Mac)
source .venv/bin/activate

# 가상환경 활성화 (Windows)
.venv\Scripts\activate
```

3. 필요한 패키지를 설치합니다:

```bash
pip install -r requirements.txt
```

#### 전역 설치

필요한 패키지를 전역으로 설치:

```bash
pip install requests
```

## 파일 구성

### 패키지 구조
```
.
├── api/                          # API 관련 모듈
│   ├── __init__.py              # 패키지 초기화 파일
│   ├── bedrock_api.py           # AWS Bedrock API 연동 기능
│   ├── dart_api.py              # DART API 호출 기본 함수
│   ├── document_downloader.py   # 공시 문서 다운로드 기능
│   └── report_period.py         # 보고서 기간 관리 기능
│
├── config/                       # 설정 관련 모듈
│   ├── __init__.py              # 패키지 초기화 파일
│   └── api_config.py            # API 키와 회사 코드 설정
│
├── service/                      # 서비스 계층 모듈
│   ├── __init__.py              # 패키지 초기화 파일
│   ├── analysis_service.py      # 공시 문서 분석 및 변환 서비스
│   └── dart_service.py          # DART API 서비스 래퍼 기능
│
├── utils/                        # 유틸리티 모듈
│   ├── __init__.py              # 패키지 초기화 파일
│   ├── csv_utils.py             # CSV 파일 처리 유틸리티
│   ├── date_utils.py            # 날짜 처리 유틸리티
│   ├── display.py               # 데이터 표시 및 포맷팅 함수
│   └── file_utils.py            # 파일 및 압축 처리 유틸리티
│
├── download/                     # 다운로드된 파일 저장 폴더
│
├── data/                         # 데이터 저장 폴더
│
├── dart_disclosure_details.py    # 재무제표 정보 조회 메인 스크립트
└── dart_disclosure_list.py       # 공시 목록 조회 메인 스크립트
```

### 주요 파일
- `dart_disclosure_details.py`: 기업의 재무제표 정보를 조회합니다.
- `dart_disclosure_list.py`: 기업의 최근 공시 목록을 조회하고, 원하는 공시의 원본 문서를 다운로드 및 분석합니다.
- `api/bedrock_api.py`: AWS Bedrock을 통해 Claude 모델을 활용하는 기능을 제공합니다.
- `service/analysis_service.py`: 공시 XML 문서를 읽고 Markdown으로 변환하는 기능을 제공합니다.
- `utils/file_utils.py`: ZIP 파일 압축 해제 및 파일 처리 유틸리티 함수를 제공합니다.

## 실행 방법

### 가상환경 사용 (권장)

먼저 가상환경을 활성화합니다:

```bash
# Linux/Mac
source .venv/bin/activate

# Windows
.venv\Scripts\activate
```

### 최근 공시 목록 조회

다음 명령을 실행하여 기업의 최근 30일간 공시 목록을 조회할 수 있습니다:

```bash
# 가상환경 활성화 상태에서
python dart_disclosure_list.py

# 또는 가상환경 활성화 없이
.venv/bin/python dart_disclosure_list.py  # Linux/Mac
.venv\Scripts\python dart_disclosure_list.py  # Windows
```

### 재무 하이라이트 조회

다음 명령을 실행하여 기업의 최근 분기 또는 연간 보고서의 재무 하이라이트를 조회할 수 있습니다:

```bash
# 가상환경 활성화 상태에서
python dart_disclosure_details.py

# 또는 가상환경 활성화 없이
.venv/bin/python dart_disclosure_details.py  # Linux/Mac
.venv\Scripts\python dart_disclosure_details.py  # Windows
```

## 주요 기능

### dart_disclosure_list.py

- 기업의 특정 기간 공시 정보를 조회합니다.
- 각 공시의 제목, 접수일자, 보고서 번호, 상세 URL을 표시합니다.
- 특정 키워드(예: "공급")가 포함된 공시를 필터링합니다.
- 가장 최신 공시를 CSV 파일로 저장합니다.
- 공시 원본 문서를 다운로드하고 압축을 해제합니다.
- XML 형식의 공시 문서를 Markdown 형식으로 변환하여 가독성을 높입니다.

### dart_disclosure_details.py

- 현재 날짜를 기준으로 가장 최근의 분기 또는 연간 보고서를 자동으로 선택합니다.
- 선택된 보고서에서 주요 재무 정보(매출, 순이익, 자산, 부채, 자본)를 추출하여 표시합니다.

### analysis_service.py

- 공시 XML 문서를 읽고 AWS Bedrock API의 Claude 모델을 활용하여 분석합니다.
- 분석 결과를 가독성 높은 Markdown 형식으로 변환합니다.
- 단일 XML 파일 또는 디렉토리 전체의 XML 파일을 일괄 처리할 수 있습니다.

## API 키 관리

- API 키는 `config/api_config.py` 파일에 저장됩니다.
- OpenDART API 키와 AWS Bedrock API 키를 모두 관리합니다.
- 실제 프로덕션 환경에서는 환경 변수나 보안 저장소를 사용하여 API 키를 관리하는 것이 좋습니다.

## 참고사항

- OpenDART API에 대한 자세한 정보는 [OpenDART 웹사이트](https://opendart.fss.or.kr)에서 확인할 수 있습니다.
- 이 프로그램은 OpenDART API의 일일 사용 한도 내에서 사용해야 합니다.
- AWS Bedrock API는 별도의 AWS 계정이 필요하며, API 키와 리전 설정이 필요합니다.
- XML 문서 분석에는 Claude 3 모델을 사용하여 높은 품질의 Markdown 변환을 제공합니다.

### 회사 고유번호 조회

OpenDART API는 종목코드가 아닌 8자리 고유번호를 사용합니다. 회사 고유번호를 조회하려면 다음과 같이 실행하세요:

```bash
# 가상환경 활성화 상태에서
python get_company_codes.py

# 또는 가상환경 활성화 없이
.venv/bin/python get_company_codes.py  # Linux/Mac
.venv\Scripts\python get_company_codes.py  # Windows
```

이 스크립트는 OpenDART API에서 모든 회사의 고유번호 목록을 다운로드하고 해당 기업의 고유번호를 찾아 표시합니다.

## 공시 문서 분석 및 변환

XML 형식의 공시 문서를 읽고 Markdown으로 변환하는 기능을 사용하려면:

```python
from service import analysis_service

# 단일 XML 파일 변환
markdown_path = analysis_service.xml_to_markdown("path/to/disclosure.xml")

# 특정 디렉토리의 모든 XML 파일 변환
markdown_paths = analysis_service.xml_to_markdown("path/to/directory/with/xmls")

# 출력 디렉토리 지정
markdown_path = analysis_service.xml_to_markdown("path/to/disclosure.xml", output_dir="path/to/output")
```

변환된 Markdown 파일은 원본 XML과 동일한 이름(확장자만 .md로 변경)으로 저장됩니다.