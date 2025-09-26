"""
AWS Bedrock API 호출 샘플 코드 (Claude 3 전용)

이 모듈은 AWS Bedrock API를 사용하여 Anthropic의 Claude 3 이상 모델에만 
접근하는 다양한 기능을 제공합니다. api_config.py의 설정을 사용합니다.
"""

import json
import boto3
import requests
import sys
import os
from pathlib import Path

# Add project root to path for imports
sys.path.insert(0, str(Path(__file__).parent.parent))

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



# def main():
#     """
#     샘플 함수들을 테스트하는 메인 함수
#     """
#     print("=== AWS Bedrock을 통한 Claude 3 모델 API 테스트 ===\n")
    
#     # 간단한 프롬프트로 테스트
#     test_prompt = "한국의 경제 상황을 간략히 요약해 주세요."
#     print(f"프롬프트: {test_prompt}\n")
    
#     print("1. boto3 클라이언트를 통한 호출:")
#     response1 = invoke_claude_with_boto3(test_prompt, max_tokens=300)
#     print(response1)
#     print("\n" + "-"*50 + "\n")
    
#     print("2. 직접 API 호출:")
#     response2 = invoke_claude_with_direct_api(test_prompt, max_tokens=300)
#     print(response2)
#     print("\n" + "-"*50 + "\n")
    
#     # 챗 형식 테스트
#     print("3. 챗 형식으로 호출:")
#     chat_messages = [
#         {"role": "user", "content": "안녕하세요, 오늘 날씨가 어때요?"},
#         {"role": "assistant", "content": "안녕하세요! 저는 AI 어시스턴트라서 실시간 날씨 정보에 접근할 수 없어요. 제가 도와드릴 다른 일이 있을까요?"},
#         {"role": "user", "content": "그렇다면 한국 경제에 대해 간략히 설명해주세요."}
#     ]
#     response3 = claude_chat(chat_messages, max_tokens=300)
#     print(response3)


# if __name__ == "__main__":
#     main()