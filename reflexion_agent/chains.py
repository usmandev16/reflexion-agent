from langchain_openai import ChatOpenAI

from .config import MODEL_NAME
from .prompts import first_responder_prompt, revisor_prompt
from .schemas import AnswerQuestion, ReviseAnswer


def build_llm() -> ChatOpenAI:
    return ChatOpenAI(model=MODEL_NAME)


def build_chains(llm: ChatOpenAI):
    initial_chain = first_responder_prompt | llm.bind_tools(tools=[AnswerQuestion])
    revisor_chain = revisor_prompt | llm.bind_tools(tools=[ReviseAnswer])
    return initial_chain, revisor_chain
