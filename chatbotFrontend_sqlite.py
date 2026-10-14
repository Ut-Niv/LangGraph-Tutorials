import streamlit as st
from chatbotWithDatabase.chatbotBackend_sqlite import workflow, retrieveAllThreads
from langchain_core.messages import HumanMessage
import uuid


# Utility function
def generate_thread_id():
    return uuid.uuid4()

def resetChat():
    thread_id = uuid.uuid4()
    st.session_state['thread_id'] = thread_id
    addThread(st.session_state['thread_id'])
    st.session_state['message_history'] = []

def addThread(thread_id):
    if thread_id not in st.session_state['past_threads']:
        st.session_state['past_threads'].append(thread_id)

def loadConversation(thread_id):
    return workflow.get_state(
        config = {'configurable': {'thread_id': thread_id}}
    ).values.get('messages', {})


# ****************** Session Setup **************
if 'message_history' not in st.session_state:
    st.session_state['message_history'] = []

if 'thread_id' not in st.session_state:
    st.session_state['thread_id'] = generate_thread_id()

if 'past_threads' not in st.session_state:
    st.session_state['past_threads'] = retrieveAllThreads()

addThread(st.session_state['thread_id'])


# **************** Sidebar UI *****************
st.sidebar.title('CHATBOT')
if st.sidebar.button('Start New Conversation'):
    resetChat()

st.sidebar.header('Your history')
for thread in st.session_state['past_threads']:
    if st.sidebar.button(str(thread)):
        st.session_state['thread_id'] = thread
        messages = loadConversation(thread)

        temp = []
        for message in messages:
            if isinstance(message, HumanMessage):
                role='user'
            else: role='assistant'
            temp.append({'role': role, 'content': message.content})

        st.session_state['message_history'] = temp



# ****************** Main UI **************
# Loading conversation history
for messages in st.session_state['message_history']:
    with st.chat_message(messages['role']):
        st.text(messages['content'])

user_input = st.chat_input("Ask Anything to me !")
if user_input:
    # fist add the message to history
    st.session_state['message_history'].append({'role': 'user', 'content': user_input})
    with st.chat_message('user'):
        st.text(user_input)

    CONFIG = {'configurable': {'thread_id': st.session_state['thread_id']}}
    
    with st.chat_message('assistant'):
        ai_message = st.write_stream(
            message_chunk.content for message_chunk, metadata in workflow.stream(
                {
                    'messages': [HumanMessage(content=user_input)]
                },
                config=CONFIG,
                stream_mode='messages'
            )
        )
    st.session_state['message_history'].append({'role': 'assistant', 'content': ai_message})
