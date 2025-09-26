import os
import sys
from pathlib import Path

from langchain_core.tools import tool
from langgraph.graph import StateGraph, START, END
from langgraph.graph import MessagesState
from langchain_core.messages import SystemMessage, HumanMessage, ToolMessage

# Add the project root to sys.path
sys.path.append(str(Path(__file__).parent.parent.parent))
from agents.disclosure_agent.tools import disclosure_tool

from langchain_anthropic import ChatAnthropic

# LLM Model 세팅
# API 키는 환경 변수나 설정 파일로부터 로드해야 합니다.
# 실제 운영 환경에서는 getpass를 사용하지 않는 것이 좋습니다.

# API 키가 설정되어 있다고 가정
api_key = os.environ.get("ANTHROPIC_API_KEY", "dummy_key_for_testing")
llm = ChatAnthropic(model="claude-3-5-sonnet-latest", api_key=api_key)


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
        Dict containing search results and download information
    """
    return disclosure_tool.search_and_download_disclosure(start_date=start_date, end_date=end_date, corp_code=corp_code, filter_keyword=filter_keyword)


# Tool 로 LLM의 기능 확장
tools = [search_and_download_disclosure]
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
    messages = [HumanMessage(content="Add 3 and 4.")]
    messages = agent.invoke({"messages": messages})
    for m in messages["messages"]:
        m.pretty_print()

        print("\n--- 최종 실행 결과 ---")
        print("실행 완료")