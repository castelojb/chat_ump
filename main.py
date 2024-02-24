from dotenv import load_dotenv
import streamlit as st

load_dotenv()

from src.thread.service import (
    get_new_thread,
    add_message_to_thread,
    get_assistant_response,
)


st.title("UMP AI - Seu assistente de mocidade")

# Set a default model
if "openai_model" not in st.session_state:
    st.session_state["openai_model"] = "gpt-3.5-turbo"

# Initialize chat history
if "messages" not in st.session_state:
    st.session_state.messages = []

if "thread" not in st.session_state:
    st.session_state.thread = get_new_thread()

# Display chat messages from history on app rerun
for message in st.session_state.messages:
    with st.chat_message(message["role"]):
        st.markdown(message["content"])

# Accept user input
if prompt := st.chat_input("What is up?"):
    # Add user message to chat history
    st.session_state.messages.append({"role": "user", "content": prompt})
    add_message_to_thread(st.session_state.thread.id, prompt)

    # Display user message in chat message container
    with st.chat_message("user"):
        st.markdown(prompt)

    # Display assistant response in chat message container
    with st.chat_message("assistant"):

        response = get_assistant_response(st.session_state.thread.id)
        st.write(response)

    st.session_state.messages.append({"role": "assistant", "content": response})
