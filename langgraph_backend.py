from langgraph.graph import StateGraph,START,END
from typing import TypedDict,Annotated,Literal
from langchain_ollama import ChatOllama
from langchain_core.messages import SystemMessage, HumanMessage, AIMessage,BaseMessage
from langgraph.graph import add_messages
from langgraph.checkpoint.memory import MemorySaver

class ChatState(TypedDict):
    messages: Annotated[list[BaseMessage], add_messages]

graph = StateGraph(ChatState)

model=ChatOllama(model="llama3.1:8b")

def chat_node(state:ChatState):
    messages = state['messages']
    response = model.invoke(messages)
    return {'messages': [response]}

checkpointer = MemorySaver()

graph.add_node('chat-node', chat_node)

graph.add_edge(START, 'chat-node')
graph.add_edge('chat-node', END)

chatbot = graph.compile(checkpointer=checkpointer)


