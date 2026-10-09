import json
from typing import List

from langchain_community.tools.tavily_search import TavilySearchResults
from langchain_core.messages import BaseMessage, ToolMessage

from .config import MAX_SEARCH_RESULTS

_tavily_tool = None


def get_search_tool() -> TavilySearchResults:
    global _tavily_tool
    if _tavily_tool is None:
        _tavily_tool = TavilySearchResults(max_results=MAX_SEARCH_RESULTS)
    return _tavily_tool


def execute_tools(state: List[BaseMessage]) -> List[BaseMessage]:
    tavily_tool = get_search_tool()
    last_ai_message = state[-1]
    tool_messages = []
    for tool_call in last_ai_message.tool_calls:
        if tool_call["name"] in ["AnswerQuestion", "ReviseAnswer"]:
            call_id = tool_call["id"]
            search_queries = tool_call["args"].get("search_queries", [])
            query_results = {}
            for query in search_queries:
                result = tavily_tool.invoke(query)
                query_results[query] = result
            tool_messages.append(ToolMessage(
                content=json.dumps(query_results),
                tool_call_id=call_id)
            )
    return tool_messages
