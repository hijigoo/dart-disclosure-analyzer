"""
AWS Bedrock API 호출 샘플 코드 (Claude 3 전용)

이 모듈은 AWS Bedrock API를 사용하여 Anthropic의 Claude 3 이상 모델에만 
접근하는 다양한 기능을 제공합니다. api_config.py의 설정을 사용합니다.
"""

import json
import boto3
import requests
from config.api_config import (
    AWS_REGION, 
    AWS_BEARER_TOKEN_BEDROCK, 
    ANTHROPIC_MODEL, 
    ANTHROPIC_SMALL_FAST_MODEL
)


def create_bedrock_client():
    """
    AWS Bedrock 클라이언트를 생성합니다.
    
    Returns:
        boto3.client: AWS Bedrock 클라이언트 인스턴스
    """
    return boto3.client(
        service_name='bedrock-runtime',
        region_name=AWS_REGION,
        aws_access_key_id='',  # AWS IAM 사용자 설정이 필요하다면 입력
        aws_secret_access_key='',  # AWS IAM 사용자 설정이 필요하다면 입력
    )


def invoke_claude_with_boto3(prompt, model_id=ANTHROPIC_MODEL, max_tokens=1000, temperature=0.5):
    """
    boto3 클라이언트를 사용하여 Claude 모델을 호출합니다.
    
    Args:
        prompt (str): 모델에게 전달할 프롬프트
        model_id (str): 사용할 Claude 모델 ID
        max_tokens (int): 생성할 최대 토큰 수
        temperature (float): 생성 텍스트의 무작위성 정도 (0.0~1.0)
    
    Returns:
        str: 모델이 생성한 응답
    
    """
    
    client = create_bedrock_client()
    
    # Claude 3 모델용 페이로드
    payload = {
        "anthropic_version": "bedrock-2023-05-31",
        "max_tokens": max_tokens,
        "temperature": temperature,
        "messages": [
            {
                "role": "user",
                "content": prompt
            }
        ]
    }
    
    try:
        # 모델 호출
        response = client.invoke_model(
            modelId=model_id,
            body=json.dumps(payload)
        )
        
        # 응답 처리
        response_body = json.loads(response['body'].read().decode('utf-8'))
        return response_body['content'][0]['text']
    
    except Exception as e:
        print(f"오류 발생: {str(e)}")
        return f"오류: {str(e)}"


def invoke_claude_with_direct_api(prompt, model_id=ANTHROPIC_MODEL, max_tokens=1000, temperature=0.5):
    """
    직접 API 호출을 통해 Claude 모델을 호출합니다.
    
    Args:
        prompt (str): 모델에게 전달할 프롬프트
        model_id (str): 사용할 Claude 모델 ID
        max_tokens (int): 생성할 최대 토큰 수
        temperature (float): 생성 텍스트의 무작위성 정도 (0.0~1.0)
    
    Returns:
        str: 모델이 생성한 응답
    
    """
    
    # API 엔드포인트
    url = f"https://bedrock-runtime.{AWS_REGION}.amazonaws.com/model/{model_id}/invoke"
    
    # 헤더 설정
    headers = {
        "Content-Type": "application/json",
        "Authorization": f"Bearer {AWS_BEARER_TOKEN_BEDROCK}"
    }
    
    # Claude 3 모델용 페이로드
    payload = {
        "anthropic_version": "bedrock-2023-05-31",
        "max_tokens": max_tokens,
        "temperature": temperature,
        "messages": [
            {
                "role": "user",
                "content": prompt
            }
        ]
    }
    
    try:
        # API 호출
        response = requests.post(url, headers=headers, json=payload)
        
        # 응답 처리
        if response.status_code == 200:
            response_json = response.json()
            return response_json['content'][0]['text']
        else:
            return f"오류: {response.status_code} - {response.text}"
    
    except Exception as e:
        print(f"오류 발생: {str(e)}")
        return f"오류: {str(e)}"


def claude_chat(messages, model_id=ANTHROPIC_MODEL, max_tokens=1000, temperature=0.5):
    """
    대화 형식으로 Claude 모델과 상호작용할 수 있는 함수입니다.
    
    Args:
        messages (list): 대화 메시지 목록. 각 메시지는 {'role': 'user'|'assistant', 'content': '내용'} 형식
        model_id (str): 사용할 Claude 모델 ID
        max_tokens (int): 생성할 최대 토큰 수
        temperature (float): 생성 텍스트의 무작위성 정도 (0.0~1.0)
    
    Returns:
        str: 모델이 생성한 응답
        
    Example:
        messages = [
            {"role": "user", "content": "안녕하세요?"},
            {"role": "assistant", "content": "안녕하세요! 어떻게 도와드릴까요?"},
            {"role": "user", "content": "오늘 날씨가 어때요?"}
        ]
        response = claude_chat(messages)
    """
    
    client = create_bedrock_client()
    
    # Claude 3 모델용 페이로드
    payload = {
        "anthropic_version": "bedrock-2023-05-31",
        "max_tokens": max_tokens,
        "temperature": temperature,
        "messages": messages
    }
    
    try:
        # 모델 호출
        response = client.invoke_model(
            modelId=model_id,
            body=json.dumps(payload)
        )
        
        # 응답 처리
        response_body = json.loads(response['body'].read().decode('utf-8'))
        return response_body['content'][0]['text']
    
    except Exception as e:
        print(f"오류 발생: {str(e)}")
        return f"오류: {str(e)}"


def analyze_financial_data(financial_statement, analysis_type="basic"):
    """
    금융 데이터 분석을 위해 Claude 3 모델을 호출하는 샘플 함수
    
    Args:
        financial_statement (str): 분석할 재무제표 데이터
        analysis_type (str): 분석 유형 ('basic', 'detailed', 'investment')
    
    Returns:
        str: 분석 결과
    """
    prompt_templates = {
        "basic": """
        다음 재무제표 데이터를 분석하고 기본적인 재무 상태를 요약해 주세요:
        
        {financial_data}
        
        다음 정보를 포함해 주세요:
        1. 수익성 지표 요약
        2. 유동성 상태
        3. 전반적인 재무 건전성 평가
        """,
        
        "detailed": """
        다음 재무제표 데이터에 대한 상세 분석을 제공해 주세요:
        
        {financial_data}
        
        다음 항목들을 분석해 주세요:
        1. 수익성 비율 (ROI, ROE, 순이익률)
        2. 유동성 비율 (당좌비율, 유동비율)
        3. 레버리지 비율 (부채비율, 이자보상배율)
        4. 효율성 비율 (자산회전율, 재고회전율)
        5. 분기별/연도별 추세 분석
        6. 업계 평균과의 비교 (가능한 경우)
        """,
        
        "investment": """
        다음 재무제표 데이터를 바탕으로 투자 관점에서의 분석을 제공해 주세요:
        
        {financial_data}
        
        다음 정보를 포함해 주세요:
        1. 현재 재무 상태 요약
        2. 주요 투자 지표 분석 (P/E, EPS, PEG 비율 등)
        3. 강점과 위험 요소
        4. 단기 및 장기 투자 전망
        5. 투자 추천 (매수/보유/매도) 및 그 이유
        """
    }
    
    # 선택한 템플릿으로 프롬프트 생성
    prompt = prompt_templates.get(analysis_type, prompt_templates["basic"])
    prompt = prompt.format(financial_data=financial_statement)
    
    # Claude 3 모델 호출 (boto3 방식)
    result = invoke_claude_with_boto3(
        prompt=prompt,
        model_id=ANTHROPIC_MODEL,
        max_tokens=2000,
        temperature=0.2
    )
    
    return result


def summarize_report(report_text, max_length=500):
    """
    긴 보고서를 요약하는 함수
    
    Args:
        report_text (str): 요약할 보고서 텍스트
        max_length (int): 요약문의 최대 길이 (글자 수)
    
    Returns:
        str: 요약된 보고서
    """
    prompt = f"""
    다음 보고서를 간결하게 요약해 주세요. 주요 포인트와 중요한 정보만 포함하세요.
    요약은 최대 {max_length}자 내외로 작성해 주세요.
    
    보고서:
    {report_text}
    """
    
    # 빠른 속도를 위해 작은 모델 사용 (Claude 3 Haiku)
    result = invoke_claude_with_boto3(
        prompt=prompt,
        model_id=ANTHROPIC_SMALL_FAST_MODEL,
        max_tokens=1000,
        temperature=0.3
    )
    
    return result


def generate_investment_recommendation(company_name, financial_data, market_trends):
    """
    투자 추천을 생성하는 함수
    
    Args:
        company_name (str): 회사 이름
        financial_data (str): 재무 데이터
        market_trends (str): 시장 트렌드 정보
    
    Returns:
        str: 투자 추천 결과
    """
    prompt = f"""
    당신은 전문 금융 분석가입니다. 다음 정보를 바탕으로 {company_name}에 대한 
    투자 추천을 제공해 주세요:
    
    ## 재무 데이터
    {financial_data}
    
    ## 시장 트렌드
    {market_trends}
    
    다음 형식으로 응답해 주세요:
    1. 요약 (한 문단)
    2. 핵심 재무 지표 분석
    3. 시장 위치 및 경쟁력
    4. 투자 추천 (매수/보유/매도)
    5. 투자 근거
    6. 주요 위험 요소
    """
    
    result = invoke_claude_with_boto3(
        prompt=prompt,
        model_id=ANTHROPIC_MODEL,
        max_tokens=3000,
        temperature=0.4
    )
    
    return result


def process_financial_document(document_text, task="extract"):
    """
    재무 문서를 처리하는 함수
    
    Args:
        document_text (str): 처리할 문서 텍스트
        task (str): 수행할 작업 유형 ('extract', 'analyze', 'summarize')
    
    Returns:
        dict: 처리 결과
    """
    task_prompts = {
        "extract": f"""
        다음 재무 문서에서 핵심 재무 정보를 추출하세요.
        추출된 정보를 다음 카테고리로 분류해 주세요:
        - 매출 정보
        - 이익 정보
        - 자산 및 부채
        - 현금 흐름
        - 주요 재무 비율
        
        문서:
        {document_text}
        """,
        
        "analyze": f"""
        다음 재무 문서를 분석하고 주요 재무적 강점과 약점을 도출하세요.
        
        문서:
        {document_text}
        """,
        
        "summarize": f"""
        다음 재무 문서의 핵심 내용을 300단어 이내로 요약하세요.
        
        문서:
        {document_text}
        """
    }
    
    # 작업 선택
    prompt = task_prompts.get(task, task_prompts["extract"])
    
    # 챗 형식으로 요청
    messages = [
        {
            "role": "user",
            "content": prompt
        }
    ]
    
    # Claude 3 모델로 처리
    response = claude_chat(
        messages=messages,
        model_id=ANTHROPIC_MODEL,
        max_tokens=2000,
        temperature=0.1
    )
    
    return {
        "task": task,
        "result": response
    }


def main():
    """
    샘플 함수들을 테스트하는 메인 함수
    """
    print("=== AWS Bedrock을 통한 Claude 3 모델 API 테스트 ===\n")
    
    # 간단한 프롬프트로 테스트
    test_prompt = "한국의 경제 상황을 간략히 요약해 주세요."
    print(f"프롬프트: {test_prompt}\n")
    
    print("1. boto3 클라이언트를 통한 호출:")
    response1 = invoke_claude_with_boto3(test_prompt, max_tokens=300)
    print(response1)
    print("\n" + "-"*50 + "\n")
    
    print("2. 직접 API 호출:")
    response2 = invoke_claude_with_direct_api(test_prompt, max_tokens=300)
    print(response2)
    print("\n" + "-"*50 + "\n")
    
    # 챗 형식 테스트
    print("3. 챗 형식으로 호출:")
    chat_messages = [
        {"role": "user", "content": "안녕하세요, 오늘 날씨가 어때요?"},
        {"role": "assistant", "content": "안녕하세요! 저는 AI 어시스턴트라서 실시간 날씨 정보에 접근할 수 없어요. 제가 도와드릴 다른 일이 있을까요?"},
        {"role": "user", "content": "그렇다면 한국 경제에 대해 간략히 설명해주세요."}
    ]
    response3 = claude_chat(chat_messages, max_tokens=300)
    print(response3)
    print("\n" + "-"*50 + "\n")
    
    # 금융 데이터 분석 예제
    sample_financial_data = """
    삼성전자 2024년 Q2 재무제표 요약:
    
    손익계산서:
    - 매출: 74조 2,300억원 (전년 동기 대비 15.2% 증가)
    - 영업이익: 10조 4,500억원 (전년 동기 대비 232.1% 증가)
    - 당기순이익: 9조 2,200억원 (전년 동기 대비 185.7% 증가)
    
    재무상태표:
    - 자산 총계: 502조 1,700억원
    - 부채 총계: 131조 5,200억원
    - 자본 총계: 370조 6,500억원
    - 부채비율: 35.5%
    
    현금흐름:
    - 영업활동 현금흐름: 18조 3,400억원
    - 투자활동 현금흐름: -12조 1,200억원
    - 재무활동 현금흐름: -5조 9,800억원
    - 기말 현금 및 현금성자산: 42조 1,500억원
    """
    
    print("4. 금융 데이터 분석 예제:")
    finance_analysis = analyze_financial_data(sample_financial_data, "investment")
    print(finance_analysis)


if __name__ == "__main__":
    main()