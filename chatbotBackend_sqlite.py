from langgraph.graph import StateGraph, START, END
from langgraph.graph.message import add_messages
from langchain_core.messages import BaseMessage, HumanMessage
from langchain_google_genai import ChatGoogleGenerativeAI as ChatOpenAI
from typing import TypedDict, Annotated
from dotenv import load_dotenv


from langgraph.checkpoint.sqlite import SqliteSaver
import sqlite3


load_dotenv()

class chatState(TypedDict):
    messages: Annotated[list[BaseMessage], add_messages]

# **************** sqlite checkpointer ***********************
conn = sqlite3.connect(database='chatbot.db', check_same_thread=False)
checkpointer = SqliteSaver(conn=conn)



graph = StateGraph(chatState)
llm = ChatOpenAI(
    model="gemini-2.5-flash",  # or gemini-2.5-pro
    temperature=0.2
)

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

def retrieveAllThreads():
    all_threads = set()
    for checkpoint in checkpointer.list(None):
        all_threads.add(checkpoint.config['configurable']['thread_id'])

    return list(all_threads)
