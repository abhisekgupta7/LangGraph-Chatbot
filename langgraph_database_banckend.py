from langgraph.graph import StateGraph,START,END
from typing import TypedDict,Annotated,Literal
from langchain_ollama import ChatOllama
from langchain_core.messages import SystemMessage, HumanMessage, AIMessage,BaseMessage
from langgraph.graph import add_messages
from langgraph.checkpoint.sqlite import SqliteSaver
import sqlite3

# Create a SQLite connection
conn = sqlite3.connect('chatbot.db',check_same_thread=False)
checkpointer = SqliteSaver(conn=conn)


class ChatState(TypedDict):
    messages: Annotated[list[BaseMessage], add_messages]

graph = StateGraph(ChatState)

model=ChatOllama(model="llama3.1:8b")

def chat_node(state:ChatState):
    messages = state['messages']
    response = model.invoke(messages)
    return {'messages': [response]}


graph.add_node('chat-node', chat_node)

graph.add_edge(START, 'chat-node')
graph.add_edge('chat-node', END)

chatbot = graph.compile(checkpointer=checkpointer)



def retrieve_all_threads():
    all_threads=set()
    for checkpoint in checkpointer.list(None):
        all_threads.add(checkpoint.config['configurable']['thread_id'])
    return list(all_threads)
