import streamlit as st
from langgraph_database_backend import chatbot, model,retrieve_all_threads
from langchain_core.messages import HumanMessage
import uuid 

def generate_thread_id():
    thread_id = str(uuid.uuid4())
    return thread_id

def reset_chat():
    thread_id = generate_thread_id()
    st.session_state["thread_id"] = thread_id
    st.session_state["message_history"] = []

def add_thread(thread_id):
    if thread_id not in st.session_state["chat_threads"]:
        st.session_state["chat_threads"].append(thread_id)

def generate_title(text: str):

    title_prompt = f"""
         Generate a short conversation title (max 6 words)
          for this message:

         {text}
              """
    title = model.invoke(title_prompt)
    return title.content.strip('"').strip("'").strip()

def load_message_history(thread_id):

    state = chatbot.get_state(config={'configurable': {'thread_id': thread_id}})
    return state.values.get("messages") or []

if "message_history" not in st.session_state:
    st.session_state["message_history"] = []

if "thread_id" not in st.session_state:
    st.session_state["thread_id"] = generate_thread_id()

if "chat_threads" not in st.session_state:
    st.session_state["chat_threads"] = retrieve_all_threads()

if "chat_titles" not in st.session_state:
    st.session_state["chat_titles"] = {}

add_thread(st.session_state["thread_id"])

message_history = st.session_state["message_history"]

st.sidebar.title("LangGraph Chatbot")

if st.sidebar.button("New Chat"):
    reset_chat()
    message_history = st.session_state["message_history"]

st.sidebar.header("My Conversations")

for thread_id in st.session_state["chat_threads"][::-1]:
    label = st.session_state["chat_titles"].get(thread_id, "New Chat")

    if st.sidebar.button(label,key=thread_id):
        st.session_state["thread_id"] = thread_id
        messages=load_message_history(thread_id)
        st.session_state["chat_titles"][thread_id] = generate_title(messages[-1].content) if messages else "New Chat"
        temp_messsage=[]
        for message in messages:
            if isinstance(message, HumanMessage):
                role="user"
            else:
                role="assistant"
            temp_messsage.append({"role":role,"content":message.content})
        st.session_state["message_history"] = temp_messsage
        message_history = st.session_state["message_history"]

    
#CONFIG = {'configurable': {'thread_id': st.session_state['thread_id']}}

    CONFIG = {
        "configurable": {"thread_id": st.session_state["thread_id"]},
        "metadata": {
            "thread_id": st.session_state["thread_id"]
        },
        "run_name": "chat_turn",
    }
    
for message in message_history:
    with st.chat_message(message["role"]):
        st.text(message["content"])

user_input = st.chat_input("Type your message here...")

if user_input:

    message_history.append({"role": "user", "content": user_input})
    with st.chat_message("user"):
        st.text(user_input)
    



    with st.chat_message("assistant"):
        ai_message = st.write_stream(
            message_chunk.content for message_chunk,metadata in chatbot.stream(
                {"messages": [HumanMessage(content=user_input)]},
                config=CONFIG,
                stream_mode="messages"
            )
        )
    message_history.append({"role": "assistant", "content": ai_message})

    if st.session_state["thread_id"] not in st.session_state["chat_titles"] or st.session_state["chat_titles"][st.session_state["thread_id"]] == "New Chat":
        st.session_state["chat_titles"][st.session_state["thread_id"]] = generate_title(user_input)

