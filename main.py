from dotenv import load_dotenv
import streamlit as st

load_dotenv()


from src.common.gemini_api import gemini_model, history_preset


st.title("UMP AI - Seu assistente de mocidade")

# Initialize chat history
if "messages" not in st.session_state:
    st.session_state.messages = []

if "convo" not in st.session_state:
    st.session_state.convo = gemini_model.start_chat(history=history_preset)
    # st.session_state.convo.send_message(history_preset)
# Display chat messages from history on app rerun
for message in st.session_state.messages:
    with st.chat_message(message["role"]):
        st.markdown(message["content"])

# Accept user input
if prompt := st.chat_input("Manda a braba"):
    # Add user message to chat history
    st.session_state.messages.append({"role": "user", "content": prompt})

    # Display user message in chat message container
    with st.chat_message("user"):
        st.markdown(prompt)

    # Display assistant response in chat message container
    with st.chat_message("assistant"):
        st.session_state.convo.send_message(prompt, stream=False)
        response = st.session_state.convo.last.text
        st.markdown(response)

    st.session_state.messages.append({"role": "assistant", "content": response})
