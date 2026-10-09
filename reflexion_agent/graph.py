from typing import List

from langchain_core.messages import BaseMessage, ToolMessage
from langgraph.graph import END, MessageGraph

from .chains import build_chains, build_llm
from .config import MAX_ITERATIONS
from .tools import execute_tools


def event_loop(state: List[BaseMessage]) -> str:
    count_tool_visits = sum(isinstance(item, ToolMessage) for item in state)
    num_iterations = count_tool_visits
    if num_iterations >= MAX_ITERATIONS:
        return END
    return "execute_tools"


def build_graph():
    initial_chain, revisor_chain = build_chains(build_llm())

    graph = MessageGraph()

    graph.add_node("respond", initial_chain)
    graph.add_node("execute_tools", execute_tools)
    graph.add_node("revisor", revisor_chain)

    graph.add_edge("respond", "execute_tools")
    graph.add_edge("execute_tools", "revisor")

    graph.add_conditional_edges("revisor", event_loop)
    graph.set_entry_point("respond")

    return graph.compile()
