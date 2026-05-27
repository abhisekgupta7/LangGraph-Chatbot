from langgraph.graph import StateGraph,START,END
from typing import TypedDict,Annotated
from langchain_core.messages import BaseMessage,HumanMessage
from langgraph.graph.message import add_messages
from langchain_google_genai import ChatGoogleGenerativeAI

from dotenv import load_dotenv
load_dotenv()

from langgraph.prebuilt import ToolNode,tools_condition
from langchain_core.tools import tool
from langchain_mcp_adapters.client import MultiServerMCPClient

import requests
import os
import asyncio

llm = ChatGoogleGenerativeAI(model="gemini-2.5-flash", api_key=os.getenv("GOOGLE_API_KEY"))

client=MultiServerMCPClient(
    {
        "arith":{
            "transport":"stdio",
            "command":"C:/Users/Abish/OneDrive/Desktop/LangGraph Chatbot/venv/Scripts/python.exe",
            "args":["C:/Users/Abish/OneDrive/Desktop/LangGraph Chatbot/server.py"]
        }
    }

)

class ChatState(TypedDict):
    messages:Annotated[list[BaseMessage],add_messages]

async def build_graph():
    tools=await client.get_tools()
    llm_with_tools=llm.bind_tools(tools)

    async def chat_node(state:ChatState):
  
        messages=state["messages"]
        response=await llm_with_tools.ainvoke(messages)
        return{"messages":[response]}

    tool_node=ToolNode(tools=tools)

    graph=StateGraph(ChatState)

    graph.add_node("chat_node",chat_node)
    graph.add_node("tools",tool_node)

    graph.add_edge(START,"chat_node")
    graph.add_conditional_edges("chat_node",tools_condition)

    
    graph.add_edge("tools","chat_node")


    chatbot=graph.compile()
    return chatbot 


async def main():
    load_dotenv()
    chatbot=await build_graph()
    result=await chatbot.ainvoke({"messages":[HumanMessage(content="What is 534365 modulus 57?")]})
    print(result["messages"][-1].content)


if __name__=="__main__":
    asyncio.run(main())
 