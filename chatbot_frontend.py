import streamlit as st
from chatbot_backend import workflow
from langchain_core.messages import HumanMessage

CONFIG = {'configurable': {'thread_id': 'thread_1'}}

# use sesstion_state to save the past message
if 'message_history' not in st.session_state:
    st.session_state['message_history'] = []

for messages in st.session_state['message_history']:
    with st.chat_message(messages['role']):
        st.text(messages['content'])

user_input = st.chat_input("Type here!!")
if user_input:
    # fist add the message to history
    st.session_state['message_history'].append({'role': 'user', 'content': user_input})
    with st.chat_message('user'):
        st.text(user_input)

    resposne = workflow.invoke({'messages': HumanMessage(content=user_input)}, config=CONFIG)
    content = resposne['messages'][-1].content

    # fist add the message to history
    st.session_state['message_history'].append({'role': 'assistant', 'content': content})
    with st.chat_message('assistant'):
        st.text(content)



