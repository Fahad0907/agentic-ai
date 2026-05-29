import streamlit as st
from chat import show_output
# frontend config
st.title("💬 Chat")

# Initialize session state to hold chat history
if "messages" not in st.session_state:
    st.session_state.messages = []  # list of {"role": ..., "content": ...}

# Render all previous messages on every rerun
for msg in st.session_state.messages:
    with st.chat_message(msg["role"]):
        st.text(msg["content"])

user_input = st.chat_input('Type here')

if user_input:
    st.session_state.messages.append({"role": "user", "content": user_input})
    with st.chat_message('user'):
        st.text(user_input)

    
    with st.chat_message("assistant"):
        response = st.write_stream(show_output(user_input))  
        st.session_state.messages.append({"role": "assistant", "content": response})