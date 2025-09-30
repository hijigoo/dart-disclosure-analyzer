# DART 공시정보 분석 에이전트 시스템

이 시스템은 LangGraph 기반의 멀티에이전트 아키텍처를 활용하여 DART(전자공시시스템) API를 통해 기업의 공시정보를 자동으로 수집, 분석, 요약하는 AI 시스템입니다.

## 소개

이 프로젝트는 LangGraph와 LangChain 기반의 지능형 에이전트 시스템을 통해 다음과 같은 기능을 제공합니다:

1. 특정 기간, 기업코드, 키워드 기반 공시 정보 자동 검색
2. XML 형식의 공시 문서를 구조화된 마크다운으로 변환
3. Claude 3.5 Sonnet 모델을 활용한 공시 내용 분석 및 요약

## 클래스 다이어그램

- 프로젝트가 발전함에 따라 향후 추가 예정

## 설치 방법

### 필수 요구사항

- Python 3.8 이상
- langchain, langchain_core, langchain_anthropic 라이브러리
- langgraph 라이브러리
- requests 라이브러리
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
├── agents/                       # 에이전트 관련 모듈
│   └── disclosure_agent/        # 공시 정보 처리 에이전트
│       ├── api/                 # API 관련 모듈
│       │   ├── bedrock_api.py   # AWS Bedrock API 연동 기능
│       │   └── dart_api.py      # DART API 호출 기본 함수
│       ├── service/             # 서비스 계층 모듈
│       │   ├── analysis_service.py  # 공시 문서 분석 및 변환 서비스
│       │   └── dart_service.py  # DART API 서비스 래퍼 기능
│       ├── tools/               # 에이전트 도구 모듈
│       │   └── disclosure_tool.py  # 공시 검색, 변환, 파일 관리 도구
│       ├── utils/               # 유틸리티 모듈
│       │   ├── csv_utils.py     # CSV 파일 처리 유틸리티
│       │   ├── date_utils.py    # 날짜 처리 유틸리티
│       │   ├── display.py       # 데이터 표시 및 포맷팅 함수
│       │   ├── file_utils.py    # 파일 및 압축 처리 유틸리티
│       │   └── path_utils.py    # 경로 처리 유틸리티
│       ├── download/            # 다운로드된 파일 저장 폴더
│       ├── prompt.md            # 에이전트 시스템 프롬프트
│       └── disclosure_agent.py  # 에이전트 메인 스크립트
│
├── config/                       # 설정 관련 모듈
│   └── api_config.py            # API 키와 회사 코드 설정
│
└── requirements.txt              # 필수 패키지 리스트
```

### 주요 파일
- `agents/disclosure_agent/disclosure_agent.py`: LangGraph 기반 에이전트 메인 스크립트입니다.
- `agents/disclosure_agent/tools/disclosure_tool.py`: 공시 검색, 다운로드, 변환, 파일 관리 도구 함수를 제공합니다.
- `agents/disclosure_agent/prompt.md`: 에이전트의 동작을 정의하는 시스템 프롬프트입니다.
- `agents/disclosure_agent/api/dart_api.py`: DART API를 호출하는 기본 함수를 제공합니다.
- `agents/disclosure_agent/service/analysis_service.py`: 공시 XML 문서를 읽고 Markdown으로 변환하는 기능을 제공합니다.

## 실행 방법

### 가상환경 사용 (권장)

먼저 가상환경을 생성하고 활성화합니다:

```bash
# 가상환경 생성
python -m venv .venv

# Linux/Mac 활성화
source .venv/bin/activate

# Windows 활성화
.venv\Scripts\activate

# 필요 패키지 설치
pip install -r requirements.txt
```

### 에이전트 실행

다음 명령을 실행하여 공시 정보 분석 에이전트를 실행할 수 있습니다:

```bash
# 가상환경 활성화 상태에서
cd agents/disclosure_agent
python disclosure_agent.py
```

기본적으로 에이전트는 다음과 같은 예시 요청으로 실행됩니다:
"삼성전자의 2025년 7월 부터 9월까지 공급체결 공시정보 알려줘"

## 에이전트 구조 및 주요 기능

### 에이전트 구조

이 시스템은 LangGraph를 기반으로 한 상태 관리 에이전트로 다음과 같은 협업 기능을 수행합니다:

1. **오케스트레이터 에이전트 (disclosure_agent.py)**
   - 사용자 요청을 이해하고 작업을 조율
   - 도구 호출을 통해 복잡한 작업을 수행
   - LangGraph의 상태 관리로 작업 흐름 제어

2. **도구 (Tools)**
   - `search_and_download_disclosure`: 특정 기간, 기업코드, 키워드 기반 공시 검색 및 다운로드
   - `convert_xml_to_markdown`: XML 공시를 구조화된 마크다운으로 변환
   - `read_file_content`: 파일 내용 읽기
   - `save_file_content`: 처리된 내용을 파일로 저장

### 워크플로우

```
사용자 요청
   ↓
요청 해석 및 도구 선택
   ↓
공시 검색 및 다운로드 (search_and_download_disclosure)
   ↓
XML → 마크다운 변환 (convert_xml_to_markdown)
   ↓
마크다운 파일 읽기 (read_file_content)
   ↓
결과 정리 및 사용자 응답 생성
```

## 설정 및 API 키 관리

- API 키는 `config/api_config.py` 파일에 저장됩니다.
- 다음 API 키가 필요합니다:
  - DART_API_KEY: OpenDART API 키
  - ANTHROPIC_API_KEY: Claude 모델 사용을 위한 Anthropic API 키
- 실제 프로덕션 환경에서는 환경 변수나 보안 저장소를 사용하여 API 키를 관리하는 것이 좋습니다.

```python
# config/api_config.py 예시
DART_API_KEY = "YOUR_DART_API_KEY"
ANTHROPIC_API_KEY = "YOUR_ANTHROPIC_API_KEY"
SAMSUNG_CORP_CODE = "00126380"  # 삼성전자 고유번호
```

## 확장 및 커스터마이징

### 시스템 프롬프트 수정

에이전트의 동작은 `agents/disclosure_agent/prompt.md` 파일에 정의된 시스템 프롬프트로 제어됩니다. 이 파일을 수정하여 에이전트의 작업 지침, 출력 형식, 분석 방향 등을 변경할 수 있습니다.

### 새로운 도구 추가

1. `agents/disclosure_agent/tools` 디렉토리에 새 도구 함수 구현
2. `disclosure_agent.py`에 도구 등록 및 바인딩

## 참고사항

- OpenDART API에 대한 자세한 정보는 [OpenDART 웹사이트](https://opendart.fss.or.kr)에서 확인할 수 있습니다.
- 이 프로그램은 OpenDART API의 일일 사용 한도 내에서 사용해야 합니다.
- Claude 3.5 Sonnet 모델을 사용하여 높은 품질의 공시 분석을 제공합니다.
- 상세한 에이전트 설명은 `agents/disclosure_agent/README.md`에서 확인할 수 있습니다.

### 회사 고유번호 정보

OpenDART API는 종목코드가 아닌 8자리 고유번호를 사용합니다. `config/api_config.py` 파일에 필요한 회사의 고유번호를 추가하여 사용할 수 있습니다. 현재 기본 설정은 삼성전자(00126380)로 되어 있습니다.

## 에이전트 사용 예시

### 기본 에이전트 실행

```python
from agents.disclosure_agent.disclosure_agent import llm_call, tool_node, should_continue
from langgraph.graph import StateGraph, START, END
from langgraph.graph import MessagesState
from langchain_core.messages import HumanMessage

# 에이전트 그래프 빌드
agent_builder = StateGraph(MessagesState)
agent_builder.add_node("llm_call", llm_call)
agent_builder.add_node("tool_node", tool_node)
agent_builder.add_edge(START, "llm_call")
agent_builder.add_conditional_edges("llm_call", should_continue, ["tool_node", END])
agent_builder.add_edge("tool_node", "llm_call")
agent = agent_builder.compile()

# 에이전트 실행
messages = [HumanMessage(content="삼성전자의 2025년 7월부터 9월까지 공급체결 공시정보 알려줘")]
result = agent.invoke({"messages": messages})

# 결과 출력
for m in result["messages"]:
    print(m.content)
```

변환된 Markdown 파일은 원본 XML과 동일한 이름(확장자만 .md로 변경)으로 저장되며, `agents/disclosure_agent/download` 폴더에서 확인할 수 있습니다.