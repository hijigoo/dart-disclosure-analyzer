# DART 공시정보 멀티에이전트 분석 시스템

LangGraph 기반의 멀티에이전트 아키텍처를 활용하여 한국 금융감독원 DART(전자공시시스템)의 기업 공시정보를 자동으로 수집, 분석, 요약하는 고급 AI 시스템입니다.

## 주요 특징

- **멀티에이전트 아키텍처**: LangGraph와 LangChain을 기반으로 한 협업형 AI 에이전트 시스템
- **자동화된 공시 수집**: DART API를 통해 지정된 기간과 기업의 공시 문서를 자동으로 검색 및 수집
- **공시 문서 변환**: XML 형식의 원본 공시를 구조화된 마크다운으로 변환하여 가독성 향상
- **지능형 분석**: Claude 3 Sonnet 모델을 활용한 고품질 자연어 이해 및 요약
- **대화형 인터페이스**: 사용자와 대화를 통해 원하는 정보를 쉽게 제공

## 에이전트 구조

이 시스템은 다음과 같은 협업 에이전트들로 구성되어 있습니다:

1. **오케스트레이터 에이전트 (disclosure_agent.py)**
   - 사용자 요청을 이해하고 작업을 조율
   - 다른 특수 에이전트들에게 작업을 할당하고 결과를 종합
   - LangGraph의 상태 관리를 통한 복잡한 워크플로우 처리

2. **문서 검색 및 다운로드 에이전트**
   - `search_and_download_disclosure` 도구를 통해 DART API에 접근
   - 특정 기간, 기업코드, 키워드 기반으로 관련 공시 검색
   - 공시 문서를 다운로드하고 압축 해제하여 XML 파일 제공

3. **문서 변환 에이전트**
   - `convert_xml_to_markdown` 도구를 통해 XML 문서를 마크다운으로 변환
   - Claude 3 모델을 활용한 지능형 문서 구조화 및 포맷팅
   - 중요 정보 강조 및 표 형식 정리

4. **파일 관리 에이전트**
   - `read_file_content` 도구로 파일 내용 읽기
   - `save_file_content` 도구로 처리된 내용을 파일로 저장
   - 디렉토리 생성 및 파일 경로 관리

## 워크플로우

이 시스템의 기본 워크플로우는 다음과 같습니다:

```
사용자 요청
   ↓
오케스트레이터 에이전트 (요청 해석)
   ↓
문서 검색 및 다운로드 에이전트 (공시 검색 및 다운로드)
   ↓
문서 변환 에이전트 (XML → 마크다운 변환)
   ↓
파일 관리 에이전트 (결과 저장)
   ↓
오케스트레이터 에이전트 (최종 응답 생성)
   ↓
사용자에게 결과 제공
```

## 설치 요구사항

- Python 3.8 이상
- LangChain, LangGraph 라이브러리
- Anthropic API 키 (Claude 3.5 Sonnet 사용)
- DART OpenAPI 키
- AWS 계정 (Bedrock API 사용 시)

## 설치 방법

1. 저장소 클론 또는 다운로드:
```bash
git clone https://github.com/yourusername/dart-disclosure-analyzer.git
cd dart-disclosure-analyzer
```

2. 가상환경 생성 및 활성화:
```bash
python -m venv .venv
source .venv/bin/activate  # Linux/Mac
# 또는
.venv\Scripts\activate  # Windows
```

3. 필요 패키지 설치:
```bash
pip install -r requirements.txt
```

4. 환경 설정:
   - `config/api_config.py`에 필요한 API 키 설정
   - ANTHROPIC_API_KEY와 DART_API_KEY 설정 필요

## 사용 방법

### 기본 실행

```bash
cd agents/disclosure_agent
python disclosure_agent.py
```

### 대화 예시

사용자: "삼성전자의 2025년 7월부터 9월까지 공급체결 공시정보 알려줘"

시스템:
1. 해당 기간의 공시 정보 검색 및 다운로드
2. XML 파일 분석 및 마크다운으로 변환
3. 주요 내용 요약 및 제공

## 도구 (Tools)

이 에이전트 시스템은 다음과 같은 도구들을 사용합니다:

1. **search_and_download_disclosure**
   - 특정 기간과 기업의 공시 문서 검색 및 다운로드
   - 매개변수: start_date, end_date, corp_code, filter_keyword

2. **convert_xml_to_markdown**
   - XML 공시 문서를 마크다운으로 변환
   - 매개변수: file_path (XML 파일 경로)

3. **read_file_content**
   - 파일 내용 읽기
   - 매개변수: file_path (읽을 파일 경로)

4. **save_file_content**
   - 콘텐츠를 파일로 저장
   - 매개변수: file_path (저장 경로), content (저장할 내용)

## 시스템 프롬프트

에이전트는 `prompt.md` 파일에서 로드된 시스템 메시지를 사용합니다. 이 프롬프트는:

1. 공시 정보 수집 및 가공의 목적 설명
2. 주요 작업 단계 정의 (다운로드, 추출, 변환, 저장, 출력)
3. 마크다운 변환 요구사항 지정
4. 투자 관점에서의 정보 정리 지침 제공

## 확장 및 커스터마이징

1. **새로운 도구 추가**
   - `tools` 디렉토리에 새로운 도구 함수 구현
   - `disclosure_agent.py`에 도구 등록 및 바인딩

2. **프롬프트 수정**
   - `prompt.md` 파일을 편집하여 에이전트의 동작 방식 조정

3. **모델 변경**
   - 다른 LLM 모델을 사용하려면 `disclosure_agent.py`의 모델 설정 부분 수정

## 주의사항

- DART API는 일일 요청 한도가 있으므로 과도한 사용에 주의
- API 키를 안전하게 관리하고 소스코드에 직접 포함하지 말 것
- 대용량 XML 문서 처리 시 메모리 사용량에 주의

## 기여 방법

1. Fork 저장소
2. 기능 브랜치 생성 (`git checkout -b feature/amazing-feature`)
3. 변경사항 커밋 (`git commit -m 'Add some amazing feature'`)
4. 브랜치에 푸시 (`git push origin feature/amazing-feature`)
5. Pull Request 생성

## 라이선스

이 프로젝트는 MIT 라이선스로 배포됩니다. 자세한 내용은 LICENSE 파일을 참조하세요.