from pathlib import Path
from langchain_core.tools import tool
from langgraph.graph import StateGraph, START, END
from langgraph.graph import MessagesState
from langchain_core.messages import SystemMessage, HumanMessage, ToolMessage
from agents.disclosure_agent.tools import disclosure_tool
from langchain_anthropic import ChatAnthropic
from config.api_config import ANTHROPIC_API_KEY

# LLM Model 세팅
llm = ChatAnthropic(model="claude-3-5-sonnet-latest", api_key=ANTHROPIC_API_KEY)


# Tool 정의
@tool
def search_and_download_disclosure(start_date, end_date, corp_code, filter_keyword):
    """
    Search for and download disclosure documents based on parameters

    Args:
        start_date: Start date for search range
        end_date: End date for search range
        corp_code: Corporation code
        filter_keyword: Keyword to filter results

    Returns:
        다운로드 받은 공시 xml 파일을 json 형태로 반환합니다.
    """
    return disclosure_tool.search_and_download_disclosure(start_date=start_date, end_date=end_date, corp_code=corp_code, filter_keyword=filter_keyword)


@tool
def read_file_content(file_path: str) -> str:
    """
    파일 경로를 입력받아 파일의 전체 내용을 텍스트로 읽어옵니다.

    Args:
        file_path: 파일 경로

    Returns:
        주어진 파일 경로(file_path)에 있는 텍스트 파일의 내용을 읽어서 반환합니다.
    """
    return disclosure_tool.read_file_content(file_path)


@tool
def save_file_content(file_path: str, content: str) -> str:
    """
    지정된 경로에 파일을 저장합니다.

    Args:
        file_path: 저장할 파일의 경로
        content: 저장할 파일의 내용 텍스트

    Returns:
        저장 성공 여부 메시지를 반환합니다.
    """
    return disclosure_tool.save_file_content(file_path, content)


# Tool 로 LLM의 기능 확장
tools = [search_and_download_disclosure, read_file_content, save_file_content]
tools_by_name = {tool.name: tool for tool in tools}
llm_with_tools = llm.bind_tools(tools)

# LLM 호출 노드 정의
def load_prompt_from_file(file_path):
    """Load prompt content from a markdown file"""
    try:
        with open(file_path, 'r', encoding='utf-8') as file:
            return file.read()
    except Exception as e:
        print(f"Error loading prompt file: {e}")
        return "You are a helpful assistant tasked with performing arithmetic on a set of inputs."


def llm_call(state: MessagesState):
    """LLM decides whether to call a tool or not"""

    # Load prompt from file
    prompt_path = Path(__file__).parent / "prompt.md"
    prompt_content = load_prompt_from_file(prompt_path)

    return {
        "messages": [
            llm_with_tools.invoke(
                [
                    SystemMessage(
                        content=prompt_content
                    )
                ]
                + state["messages"]
            )
        ]
    }


def tool_node(state: dict):
    """Performs the tool call"""

    result = []
    for tool_call in state["messages"][-1].tool_calls:
        tool = tools_by_name[tool_call["name"]]
        observation = tool.invoke(tool_call["args"])
        result.append(ToolMessage(content=observation, tool_call_id=tool_call["id"]))
    return {"messages": result}


# Conditional edge function to route to the tool node or end based upon whether the LLM made a tool call
def should_continue(state: MessagesState) -> str:
    """Decide if we should continue the loop or stop based upon whether the LLM made a tool call"""

    messages = state["messages"]
    last_message = messages[-1]
    # If the LLM makes a tool call, then perform an action
    if last_message.tool_calls:
        return "tool_node"
    # Otherwise, we stop (reply to the user)
    return END


# 4. 에이전트 실행
if __name__ == "__main__":
    print("===== LangGraph 기반 DART 공시 정보 취합 에이전트 =====")
    
    # Build workflow
    agent_builder = StateGraph(MessagesState)

    # Add nodes
    agent_builder.add_node("llm_call", llm_call)
    agent_builder.add_node("tool_node", tool_node)

    # Add edges to connect nodes
    agent_builder.add_edge(START, "llm_call")
    agent_builder.add_conditional_edges(
        "llm_call",
        should_continue,
        ["tool_node", END]
    )
    agent_builder.add_edge("tool_node", "llm_call")

    # Compile the agent
    agent = agent_builder.compile()

    # Show the agent
    print("Agent graph compiled successfully.")

    # Invoke
    messages = [HumanMessage(content="삼성전자의 2025년 7월 부터 9월까지 공급체결 공시정보 알려줘")]
    messages = agent.invoke({"messages": messages})
    for m in messages["messages"]:
        print("\n--- 최종 실행 결과 ---\n")
        m.pretty_print()
    print("\n\n--- 실행 완료 ---")