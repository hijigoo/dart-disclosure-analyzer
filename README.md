# DART 공시정보 조회 프로그램

이 프로그램은 DART(전자공시시스템) API를 활용하여 기업의 공시정보를 조회하는 Python 스크립트입니다.

## 소개

이 프로젝트는 OpenDART API를 통해 기업의 다음과 같은 정보를 조회합니다:

1. 최근 공시 목록
2. 상세 공시 정보
3. 재무 하이라이트

## 클래스 다이어그램

- TBD

## 설치 방법

### 필수 요구사항

- Python 3.6 이상
- requests 라이브러리

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
│   ├── api_config.py            # API 키와 회사 코드 설정
│   ├── dart_api.py              # DART API 호출 기본 함수
│   ├── document_downloader.py   # 공시 문서 다운로드 기능
│   └── report_period.py         # 보고서 기간 관리 기능
│
├── display/                      # 표시 관련 모듈
│   ├── __init__.py              # 패키지 초기화 파일
│   └── display.py               # 데이터 표시 및 포맷팅 함수
│
├── utils/                        # 유틸리티 모듈
│   ├── __init__.py              # 패키지 초기화 파일
│   └── date_utils.py            # 날짜 처리 유틸리티
│
├── download/                     # 다운로드된 파일 저장 폴더
│
├── dart_disclosure_details.py # 재무제표 정보 조회 메인 스크립트
└── dart_disclosure_list.py    # 공시 목록 조회 메인 스크립트
```

### 주요 파일
- `dart_disclosure_details.py`: 기업의 재무제표 정보를 조회합니다.
- `dart_disclosure_list.py`: 기업의 최근 공시 목록을 조회합니다.

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

- 기업의 최근 30일간 공시 정보를 조회합니다.
- 각 공시의 제목, 접수일자, 보고서 번호, 상세 URL을 표시합니다.

### dart_disclosure_details.py

- 현재 날짜를 기준으로 가장 최근의 분기 또는 연간 보고서를 자동으로 선택합니다.
- 선택된 보고서에서 주요 재무 정보(매출, 순이익, 자산, 부채, 자본)를 추출하여 표시합니다.

## API 키 관리

- API 키는 `api_config.py` 파일에 저장됩니다.
- 실제 프로덕션 환경에서는 환경 변수나 보안 저장소를 사용하여 API 키를 관리하는 것이 좋습니다.

## 참고사항

- OpenDART API에 대한 자세한 정보는 [OpenDART 웹사이트](https://opendart.fss.or.kr)에서 확인할 수 있습니다.
- 이 프로그램은 OpenDART API의 일일 사용 한도 내에서 사용해야 합니다.

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