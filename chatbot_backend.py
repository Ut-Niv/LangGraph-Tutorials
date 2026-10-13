from langgraph.graph import StateGraph, START, END
from langgraph.checkpoint.memory import InMemorySaver
from langgraph.graph.message import add_messages
from langchain_core.messages import BaseMessage, HumanMessage
from langchain_openai import ChatOpenAI

from typing import TypedDict, Annotated
from dotenv import load_dotenv

load_dotenv()

class chatState(TypedDict):
    messages: Annotated[list[BaseMessage], add_messages]

checkpointer = InMemorySaver()
graph = StateGraph(chatState)
llm = ChatOpenAI()

def chatNode(state: chatState):
    # take user query
    # send to LLM
    # response store state
    messages = state['messages']
    resposne = llm.invoke(messages)
    return {'messages': [resposne]}

graph.add_node('chatNode', chatNode)
graph.add_edge(START, 'chatNode')
graph.add_edge('chatNode', END)
workflow = graph.compile(checkpointer=checkpointer)
