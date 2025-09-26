"""
Analysis Service Module

이 모듈은 XML 공시 문서를 읽고 분석하여 보기 편한 Markdown 형식으로 변환하는 기능을 제공합니다.
AWS Bedrock의 Claude 모델을 사용하여 XML을 해석하고 중요 내용을 Markdown으로 요약합니다.
"""

import os
import xml.etree.ElementTree as ET
from pathlib import Path
import re
import sys

# Add project root to path to ensure modules can be imported
sys.path.insert(0, str(Path(__file__).parent.parent))

from api import bedrock_api


def read_xml_file(file_path):
    """
    XML 파일을 읽어 내용을 텍스트로 반환합니다.

    Args:
        file_path (str): XML 파일 경로

    Returns:
        str: XML 파일의 내용
    """
    try:
        # XML 파일 경로를 Path 객체로 변환
        xml_path = Path(file_path)

        # 파일 존재 여부 확인
        if not xml_path.exists():
            raise FileNotFoundError(f"XML 파일을 찾을 수 없습니다: {file_path}")

        # XML 파일 내용 읽기
        with open(xml_path, 'r', encoding='utf-8') as f:
            xml_content = f.read()

        return xml_content

    except Exception as e:
        print(f"XML 파일을 읽는 중 오류 발생: {str(e)}")
        return None



def convert_to_markdown(xml_data, prompt_template=None):
    """
    XML 데이터를 Bedrock API를 통해 Markdown으로 변환합니다.

    Args:
        xml_data (dict or str): 변환할 XML 데이터
        prompt_template (str, optional): 사용자 정의 프롬프트 템플릿

    Returns:
        str: Markdown 형식의 문서
    """
    # XML 데이터가 딕셔너리인 경우 문자열로 변환
    if isinstance(xml_data, dict):
        if 'raw_content' in xml_data:
            xml_content = xml_data['raw_content']
        else:
            # 딕셔너리를 문자열로 변환 (간소화된 형태)
            xml_content = str(xml_data)
    else:
        xml_content = xml_data

    # 너무 긴 컨텐츠는 잘라내기 (Claude의 토큰 제한 고려)
    # if len(xml_content) > 20000:
    #     xml_content = xml_content[:20000] + "\n\n... (이하 내용 생략) ..."

    # 기본 프롬프트 템플릿
    if prompt_template is None:
        prompt_template = """
        당신은 전문적인 금융 문서 분석가입니다.
        아래 제공된 XML 형식의 공시 문서를 분석하고 모든 내용을 추출하여
        체계적인 마크다운 형식으로 정리해 주세요.

        # 분석 요구사항
        1. 문서의 제목, 공시 일자, 공시 주체 등 기본 정보를 포함할 것
        2. 주요 재무 데이터는 표 형식으로 정리할 것
        3. 공시의 중요 포인트를 강조할 것
        4. 모든 내용이 포함될 것
        5. 적절한 마크다운 형식(제목, 목록, 표, 코드 블록 등)을 사용하여 가독성 높게 구성할 것

        # XML 문서:
        ```xml
        {xml_content}
        ```

        마크다운 형식으로 정리된 문서를 제공해 주세요. 분석 과정이나 설명은 필요 없습니다.
        바로 마크다운 내용만 작성해 주세요.
        """

    # 실제 XML 내용을 프롬프트에 삽입
    formatted_prompt = prompt_template.format(xml_content=xml_content)

    # Bedrock API를 사용하여 변환
    try:
        markdown_content = bedrock_api.invoke_claude_with_boto3(
            prompt=formatted_prompt,
            max_tokens=8000,
            temperature=0.2
        )
        return markdown_content
    except Exception as e:
        print(f"Markdown 변환 중 오류 발생: {str(e)}")
        return f"# 변환 오류\n\n오류가 발생했습니다: {str(e)}"


def save_markdown_file(markdown_content, source_xml_path, output_dir=None):
    """
    Markdown 내용을 파일로 저장합니다.

    Args:
        markdown_content (str): 저장할 Markdown 내용
        source_xml_path (str): 원본 XML 파일 경로
        output_dir (str, optional): 결과물을 저장할 디렉토리 경로

    Returns:
        str: 저장된 Markdown 파일 경로
    """
    try:
        # 소스 XML 경로를 Path 객체로 변환
        source_path = Path(source_xml_path)

        # 출력 디렉토리 설정
        if output_dir is None:
            # 기본값으로 원본 XML과 같은 디렉토리 사용
            output_directory = source_path.parent
        else:
            output_directory = Path(output_dir)
            # 디렉토리가 없으면 생성
            if not output_directory.exists():
                output_directory.mkdir(parents=True, exist_ok=True)

        # 출력 파일명 생성 (원본 XML 파일명에서 .xml 확장자를 .md로 변경)
        output_filename = source_path.stem + '.md'
        output_path = output_directory / output_filename

        # Markdown 파일 저장
        with open(output_path, 'w', encoding='utf-8') as f:
            f.write(markdown_content)

        # print(f"Markdown 파일이 저장되었습니다: {output_path}")
        return str(output_path)

    except Exception as e:
        print(f"Markdown 파일 저장 중 오류 발생: {str(e)}")
        return None


def xml_to_markdown(xml_path, output_dir=None):
    """
    단일 XML 파일 또는 디렉토리의 XML 파일들을 Markdown으로 변환합니다.

    Args:
        xml_path (str): XML 파일 또는 디렉토리 경로
        output_dir (str, optional): Markdown 파일을 저장할 디렉토리 경로

    Returns:
        str or list: 변환된 Markdown 파일 경로 또는 경로 목록
    """
    try:
        # 입력 경로를 Path 객체로 변환
        path = Path(xml_path)

        # 경로가 파일인 경우
        if path.is_file() and path.suffix.lower() == '.xml':
            xml_content = read_xml_file(path)
            if xml_content is None:
                return None

            markdown_content = convert_to_markdown({'raw_content': xml_content})
            return save_markdown_file(markdown_content, path, output_dir)

        else:
            raise ValueError(f"유효한 XML 파일 또는 디렉토리가 아닙니다: {xml_path}")

    except Exception as e:
        print(f"XML 변환 중 오류 발생: {str(e)}")
        return None